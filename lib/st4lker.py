import os
import time
import json
import lib.utils
import graphviz as gv
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# GLOBAL CONSTANTS ------------------------- #

ATTRB_CLASS = 'g47SY'
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
            
def get_followers(driver, uname, flim):
    try:
        fcount = driver.find_elements_by_class_name(ATTRB_CLASS)[1].text
        if (int(fcount) > flim):
            return []
    except Exception:
        return []

    try:
        followers_e = driver.find_element_by_css_selector('a[href="/{}/followers/"]'.format(uname))
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

def get_following(driver, uname, flim):
    try:
        fcount = driver.find_elements_by_class_name(ATTRB_CLASS)[2].text
        if (int(fcount) > flim):
            return []
    except Exception:
        return []

    try:
        following_e = driver.find_element_by_css_selector('a[href="/{}/following/"]'.format(uname))
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

def draw_conns(uname, followers, following, users, edges):
    for u in set([*followers, *following]):
        users.add(u)
        
    for u in followers:
        edges.append(make_edge(u, uname, color=dict(color='#3066BE')))
    for u in following:
        edges.append(make_edge(uname, u, color=dict(color='#119DA4')))
        
def rec_st4lk(driver, fols, depth, max_depth, flim, users, edges):
    if depth > max_depth:
        return
    
    for f in fols:
        if not f in users:
            driver.get('https://www.instagram.com/{}'.format(f))
            fole = get_followers(driver, f, flim)
            foli = get_following(driver, f, flim)        
            draw_conns(f, fole, foli, users, edges)
        
        rec_st4lk(driver, fole, depth+1, max_depth, flim, users, edges)
        rec_st4lk(driver, foli, depth+1, max_depth, flim, users, edges)

def make_node(uname, **kwargs):
    d = {k: v for k, v in kwargs.items()}
    d['id'] = uname
    d['label'] = uname
    return d

def make_edge(u1, u2, **kwargs):
    d = {k: v for k, v in kwargs.items()}
    d['from'] = u1
    d['to'] = u2
    return d
        
def st4lk(driver, uname, dest_folder=None, depth=0, flim=500):
    lib.utils.prompt_login(driver)
    
    if not dest_folder:
        dest_folder = './results/'
    
    dest_folder = os.path.join(dest_folder, uname)
    if not os.path.isdir(dest_folder):
        os.mkdir(dest_folder)
        
    users = set()
    edges = list()
    
    driver.get('https://instagram.com/{}'.format(uname))
    followers = get_followers(driver, uname, flim)
    following = get_following(driver, uname, flim)
    
    users.add(uname)
    draw_conns(uname, followers, following, users, edges)
    
    rec_st4lk(driver, followers, 1, depth, flim, users, edges)
    rec_st4lk(driver, following, 1, depth, flim, users, edges)

    print('[*] Creating JSON ... ')
    jsonf = {
        'nodes': list(map(lambda u: make_node(u, color=dict(background='#AEECEF', border='#83B1B3')), users)),
        'edges': edges
    }    

    with open(os.path.join(dest_folder, uname + '.json'), 'w') as f:
        print('[*] Writing JSON ... ')
        json.dump(jsonf, f)