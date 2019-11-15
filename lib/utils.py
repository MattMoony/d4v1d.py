def prompt_login(driver):
    url = 'https://www.instagram.com/accounts/login/'
    driver.get(url)
    
    while driver.current_url == url:
        input('Press any key to continue ... ')
        
