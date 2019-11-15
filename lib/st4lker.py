import time
import lib.utils
import graphviz as gv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# GLOBAL CONSTANTS ------------------------- #

POPUP_CLASS = 'PZuss'
POPUP_EXIT_CLASS = 'wpO6b'
USERNAME_CLASS = '_0imsa'

# ------------------------------------------ #

def scroll_popup(driver, target, scroll_timeout=2, scroll_err_limit=5):
    box = driver.find_element_by_class_name(target)
    sh = -1
    ex = 0
    
    while ex < scroll_err_limit:
        try:
            driver.execute_script("document.getElementsByClassName('{}')[0].scrollIntoView(false)".format(target));
            time.sleep(scroll_timeout)
            
            if sh == driver.execute_script("return document.getElementsByClassName('{}')[0].scrollHeight".format(target)):
                ex += 1
                print('at bottom')
            else:
                ex = 0
            sh = driver.execute_script("return document.getElementsByClassName('{}')[0].scrollHeight".format(target))
        except KeyboardInterrupt as e:
            print('[*] Stopping ... ')
            break
        except Exception as e:
            ex += 1
            print(e)
            time.sleep(scroll_timeout)
            
def get_followers(driver, uname):
    try:
        followers_e = driver.find_element_by_css_selector('a[href*="/{}/followers"]'.format(uname))
    except Exception:
        return []
    followers = []
    
    followers_e.click()
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, POPUP_CLASS))
        )
        scroll_popup(driver, POPUP_CLASS)
        
        followers = list(map(lambda e: e.text, driver.find_elements_by_class_name(USERNAME_CLASS)))
    except TimeoutException:
        print('[-] Followers: Timed out ... ')
        
    driver.find_element_by_class_name(POPUP_EXIT_CLASS).click()
    return followers

def get_following(driver, uname):
    try:
        following_e = driver.find_element_by_css_selector('a[href*="/{}/following"]'.format(uname))
    except Exception:
        return []
    following = []
        
    following_e.click()
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, POPUP_CLASS))
        )
        scroll_popup(driver, POPUP_CLASS)
        
        following = list(map(lambda e: e.text, driver.find_elements_by_class_name(USERNAME_CLASS)))
    except TimeoutException:
        print('[-] Following: Timed out ... ')
        
    driver.find_element_by_class_name(POPUP_EXIT_CLASS).click()
    return following

def draw_conns(d, uname, followers, following):
    for u in set([*followers, *following]):
        d.node(u)
        
    for u in followers:
        d.edge(u, uname)
    for u in following:
        d.edge(uname, u)
        
def st4lk(uname):
    driver = webdriver.Chrome()
    lib.utils.prompt_login(driver)
    
    driver.get('https://instagram.com/{}'.format(uname))
    followers = get_followers(driver, uname)
    following = get_following(driver, uname)
        
    d = gv.Digraph(comment='{}\'s relations'.format(uname),
                   format='svg', filename='results/{}.dot'.format(uname))
    d.node(uname)
    draw_conns(d, uname, followers, following)

    for f in followers:
        driver.get('https://www.instagram.com/{}'.format(f))
        fole = get_followers(driver, f)
        foli = get_following(driver, f)        
        draw_conns(d, f, fole, foli)

    d.render(d.filename, view=True)