from selenium import webdriver
from selenium.webdriver.common.by import By
from e2e.e2e_utils import *


MODULE_ID = 'e2e.us_main_switch'

def us_control_main_switch(driver: webdriver.Chrome) -> int:
    '''
    3- User able to toggle room switch by clicking on the device power button
    4- User able to see device's real state
    '''
    func_id = MODULE_ID + '.us_control_main_switch'
    # go to living room
    is_living_room = go_to_living_room(driver)
    if not is_living_room:
        return 1
    
    

    # turn on the lamp and off 4 times
    try:
        main_switch = get_device_by_name(driver, 'Main Switch')
        buttons = main_switch.find_elements(By.CSS_SELECTOR, 'button')
        state = main_switch.find_element(By.CSS_SELECTOR, '.device_state')
        for i in range(4):
            if state.text == 'OFF':
                buttons[1].click()
                if state.text != 'ON':
                    return 1

            elif state.text == 'ON':
                buttons[1].click()
                if state.text != 'OFF':
                    return 1
    except:
        return 1
    
    return 0