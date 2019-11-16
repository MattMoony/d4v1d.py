import os
import time
import json
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
        
def rec_st4lk(driver, d, fols, depth, max_depth, u_crw):
    if depth > max_depth:
        return
    
    for f in fols:
        if not f in u_crw.keys():
            driver.get('https://www.instagram.com/{}'.format(f))
            fole = get_followers(driver, f)
            foli = get_following(driver, f)        
            draw_conns(d, f, fole, foli)
            u_crw[f] = dict(fole=fole, foli=foli)
        
        rec_st4lk(driver, d, u_crw['fole'], depth+1, max_depth)
        rec_st4lk(driver, d, u_crw['foli'], depth+1, max_depth)
        
def st4lk(uname, dest_folder=None, depth=0):
    driver = webdriver.Chrome()
    lib.utils.prompt_login(driver)
    
    if not dest_folder:
        dest_folder = './results/'
    
    dest_folder = os.path.join(dest_folder, uname)
    if not os.path.isdir(dest_folder):
        os.mkdir(dest_folder)
        
    u_crw = dict()
    
    driver.get('https://instagram.com/{}'.format(uname))
    followers = get_followers(driver, uname)
    following = get_following(driver, uname)
        
    fname = os.path.join(dest_folder, '{}.dot'.format(uname))
    d = gv.Digraph(comment='{}\'s relations'.format(uname),
                   format='svg', filename=fname)
    d.attr('node', shape='circle')
    d.attr('graph', pad='0.5', nodesep='1', ranksep='2')
    draw_conns(d, uname, followers, following)
    
    u_crw[uname] = dict(fole=followers, foli=following)
    
    rec_st4lk(driver, d, followers, 1, depth, u_crw)
    rec_st4lk(driver, d, following, 1, depth, u_crw)

    print('[*] Creating graph ... ')
    d.render(d.filename, view=True)
    
    with open(os.path.join(dest_folder, uname + '.json'), 'w') as f:
        print('[*] Creating JSON ... ')
        json.dump(u_crw, f)