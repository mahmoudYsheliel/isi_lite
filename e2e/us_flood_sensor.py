from selenium import webdriver
from selenium.webdriver.common.by import By
from e2e.e2e_utils import *
import time


MODULE_ID = 'e2e.us_flood_sensor'


def us_view_flood_notification(driver:webdriver.Chrome)->int:
    '''
    3- The app displays a notification if water detected
    '''
    
    func_id = MODULE_ID + '.us_view_flood_notification'
    #   log in and save data in local storage
    save_username_pass_local_storage(driver)
    
    #go to living room
    is_living_room = go_to_living_room(driver)
    if not is_living_room:
        return 1
    
    # cancel connected dialog
    try :
        alert = driver.find_element(By.XPATH, '//*[@role="alert"]')
        alert.find_element(By.CSS_SELECTOR,'button').click()
    except:
        pass    
    
    mqtt_send_notification_simulation('FLOOD')
    
    # find flood notification
    try:
        time.sleep(0.5)
        alert = driver.find_element(By.XPATH, '//*[@role="alert"]')
        header = alert.find_element(By.CSS_SELECTOR,'.p-toast-message-text>:first-child')
        message = alert.find_element(By.CSS_SELECTOR,'.p-toast-message-text>:last-child')
        if header.text != 'Room: Living Room \n Device: Flood Sensor' or message.text != 'Flood Detected':
            return 1
        alert.find_element(By.CSS_SELECTOR,'button').click()
    except:
        return 1
    return 0
