import os
import requests as req
import dateutil.parser
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# GLOBAL CONSTANTS ------------------------- #

POPUP_CLASS = '_97aPb'
POPUP_IMG_CLASS = 'kPFhm'
POPUP_SLIDES_CLASS = 'YlNGR'
POPUP_VIDEO_CLASS = '_5wCQW'
POPUP_CLOSE_CLASS = 'ckWGn'
POPUP_TIME_CLASS = '_1o9PC'

# ------------------------------------------ #

def get_img_src(pop):
    img = pop.find_element_by_tag_name('img')
    return img.get_attribute('srcset').split(',')[-1].split(' ')[0]

def get_vid_src(pop):
    video = pop.find_element_by_tag_name('video')
    return video.get_attribute('src')

def get_img_srcs(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, POPUP_CLASS)),
        )
        
        try:
            ul = driver.find_element_by_class_name(POPUP_SLIDES_CLASS)
            srcs = set()
            goon = True
            while goon:
                try:
                    for img in ul.find_elements_by_tag_name('img'):
                        url = img.get_attribute('srcset').split(',')[-1].split(' ')[0]
                        if url.strip() != '':
                            srcs.add(url)
                    for vid in ul.find_elements_by_tag_name('video'):
                        url = vid.get_attribute('src')
                        if url.strip() != '':
                            srcs.add(url)
                    chev = driver.find_element_by_class_name('coreSpriteRightChevron')
                    chev.click()
                except:
                    goon = False
            return list(srcs)
        except:
            try:
                pop = driver.find_element_by_class_name(POPUP_VIDEO_CLASS)
                return [get_vid_src(pop)]
            except:
                try:
                    pop = driver.find_element_by_class_name(POPUP_IMG_CLASS)
                    return [get_img_src(pop)]
                except: 
                    print('[Image]: Unknown format!')
    except TimeoutException:
        print('[Image]: Timed out ... ')
                
        
def get_img_time(driver):
    time_e = driver.find_element_by_class_name(POPUP_TIME_CLASS)
    return dateutil.parser.parse(time_e.get_attribute('datetime'))

def save_img(url, dest):
    with open(dest, 'wb') as f:
        f.write(req.get(url).content)

def close_popup(driver):
    driver.find_element_by_class_name(POPUP_CLOSE_CLASS).click()

def get_imgs(driver, dest_folder):
    try:
        imgs = driver.find_elements_by_css_selector('a[href*="/p/"]')
    except Exception:
        return []    
    
    for im in imgs:
        im.click()
        
        srcs = get_img_srcs(driver)
        if srcs:
            for i, s in enumerate(srcs):
                time = get_img_time(driver)
        
                fname = '{:04d}{:02d}{:02d}-{:02d}{:02d}{:02d}-{:03d}.{:}'.format(
                            time.year, time.month, time.day, 
                            time.hour, time.minute, time.second, 
                            i, 'jpg' if '.jpg' in s else 'mp4')
                save_img(s, os.path.join(dest_folder, fname))
                print('[*] Saved {:} ... '.format(fname))

        close_popup(driver)

def scr4p3(uname, dest_folder=None):
    driver = webdriver.Chrome()
    driver.get('https://instagram.com/{}'.format(uname))

    if not dest_folder:
        dest_folder = './imgs/{:}'.format(uname)
        
    if not os.path.isdir(dest_folder):
        os.mkdir(dest_folder)

    get_imgs(driver, dest_folder)