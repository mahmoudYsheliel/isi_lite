from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from e2e.e2e_utils import *
import time
true_data = ['isi_lite', server_ip, mqtt_user_name, mqtt_password]
MODULE_ID = 'e2e.us_login_logout'
'''
    1- Home page opens if user has active network profile
    2- if there is no active network profile, user goes to network profile page
    3- loging out deletes the credintials and moves to network profile page untill netwok is selected
'''


def add_data_to_input_fields(fields: list[WebElement], data: list[str]) -> bool:
    if len(fields) != 4 or len(data) != 4:
        return
    # clear fields first
    for i, field in enumerate(fields):
        field.find_element(By.CSS_SELECTOR, 'input').send_keys(Keys.CONTROL + "a")
        field.find_element(By.CSS_SELECTOR, 'input').send_keys(Keys.DELETE)
        field.find_element(By.CSS_SELECTOR, 'input').send_keys(data[i])
    return True

def connect_profile(driver: webdriver.Chrome, profile: WebElement, expected_success: bool) -> bool:
    connect_button = profile.find_elements(By.CSS_SELECTOR, '.field_actions>button')[0]
    if not connect_button.is_enabled():
        return False
    try:
        alert = driver.find_element(By.XPATH, '//*[@role="alert"]')
        remove_alert(driver)
    except:
        pass
    connect_button.click()
    time.sleep(1)  # wait untill connnected

    alert = driver.find_element(By.XPATH, '//*[@role="alert"]')
    if alert.text != 'Connected\nConnected to ISI Device Network':
        return False
    remove_alert(driver)
    return True



def move_to_notwork_profile(driver:webdriver.Chrome)->bool:
    try:
        bottom_bar_options = driver.find_elements(By.CSS_SELECTOR, '#bottom_bar_cont>div')
        bottom_bar_options[3].click()
        return True
    except:
        return False
    

def logout(driver:webdriver.Chrome)->bool:
    try:
        logout_button = driver.find_elements(By.CSS_SELECTOR,'#bottom_bar_cont>div')[4]
        logout_button.click()
        time.sleep(0.5)
        alert = driver.find_element(By.XPATH, '//*[@role="alert"]')
        if alert.text != "Diconnected\nCan not Connect to ISI Device Network":
            return False
        remove_alert(driver)
        return True
    except:
        return False
    
def add_connect_network_profile(driver:webdriver.Chrome)->bool:
    if not move_to_notwork_profile(driver):
        return False
    add_button = driver.find_element(By.CSS_SELECTOR, '.add_button')
    add_button.click()
    netwok_field = driver.find_element(By.CSS_SELECTOR, '.ISInetwork_profile>*')
    text_input_fields = netwok_field.find_elements(By.CSS_SELECTOR, '.element')
    if not add_data_to_input_fields(text_input_fields,true_data):
        return False
    if not connect_profile(driver,netwok_field,true_data):
        return False
    return True
    
    
def move_while_logout(driver:webdriver.Chrome)->bool:
    bottom_bar_options = driver.find_elements(By.CSS_SELECTOR, '#bottom_bar_cont>div')
    for i in range(3):
        bottom_bar_options[i].click()
        time.sleep(0.5)
        alert = driver.find_element(By.XPATH, '//*[@role="alert"]')
        if alert.text != "Not Connected\nConnect to ISI Device Network First":
            return False
        remove_alert(driver)
    return True
    
    
    
def us_login_logout(driver:webdriver.Chrome)->int:
    try:
        alert = driver.find_element(By.XPATH, '//*[@role="alert"]')
        remove_alert(driver)
    except:
        pass
    
    if not add_connect_network_profile(driver):
        return 1
    if not logout(driver):
        return 1
    if not move_while_logout(driver):
        return 1
    
    netwok_field = driver.find_element(By.CSS_SELECTOR, '.ISInetwork_profile>*')
    if not connect_profile(driver,netwok_field,true_data):
        return 1
    
    
    return 0
    
    
    
    