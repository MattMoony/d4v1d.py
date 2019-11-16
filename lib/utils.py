from getpass import getpass
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

# GLOBAL CONSTANTS ------------------------- #

INPUT_CLASS = '_2hvTZ'
SUBMIT_CLASS = 'L3NKy'

# ------------------------------------------ #

def login(driver, uname, pwd):
    curl = driver.current_url
    inps = driver.find_elements_by_class_name(INPUT_CLASS)
    subb = driver.find_element_by_class_name(SUBMIT_CLASS)
    
    inps[0].send_keys(uname)
    inps[1].send_keys(pwd)
    try:
        subb.click()
    except:
        return False
    
    try:
        WebDriverWait(driver, 10).until(lambda driver: driver.current_url != curl)
        return True
    except TimeoutException:
        return False

def prompt_login(driver):
    url = 'https://www.instagram.com/accounts/login/'
    driver.get(url)
    
    try:
        WebDriverWait(driver, 10).until(lambda driver: driver.current_url != url)
    except TimeoutException:
        while True:
            if login(driver, input('Enter username: '), getpass('Enter password: ')):
                break
            print('[*] Please try again!')