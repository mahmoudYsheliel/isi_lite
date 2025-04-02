from selenium import webdriver
from selenium.webdriver.common.by import By
from e2e.e2e_utils import *
import time

MODULE_ID = 'e2e.us_main_switch_panel'


def us_toggle_all_switches(driver: webdriver.Chrome) -> int:
    '''
    3- User able to toggle all room switches by clicking on the device power button
    4- User able to see device's real state
    '''
    func_id = MODULE_ID + '.us_toggle_all_switches'

    # go to living room
    is_living_room = go_to_living_room(driver)
    if not is_living_room:
        return 1

    # check header and check state in case of 'OFF' state
    try:
        main_switch = get_device_by_name(driver, 'Main Switch Panel')
        buttons = main_switch.find_elements(By.CSS_SELECTOR, 'button')
        state = main_switch.find_element(By.CSS_SELECTOR, '.device_state')
        #   turn all buttons off
        if state.text == 'ON':
            buttons[1].click()
        if state.text != 'OFF':
            return 1

        # popup dialog
        buttons[0].click()
        # check number of buttons and their states
        switches_4 = driver.find_elements(By.CSS_SELECTOR, '#switch_4ch_btns_cont button')
        if len(switches_4) != 4:
            return 1
        time.sleep(0.1)
        header = try_get_elem_txt(driver,'.p-dialog-header')
        if header != 'Main Switch Panel':
            return 1
        for btn in switches_4:
            if check_class(btn, 'switch_4ch_btn_active'):
                return 1
        remove_dialog(driver)
    except:
        return 1
    # check in case of 'ON' state
    try:
        # turn all lights on
        buttons[1].click()
        # check state
        if state.text != 'ON':
            return 1

        # popup dialog and check state
        buttons[0].click()
        switches_4 = driver.find_elements(By.CSS_SELECTOR, '#switch_4ch_btns_cont button')

        for btn in switches_4:
            if not check_class(btn, 'switch_4ch_btn_active'):
                return 1
        remove_dialog(driver)
    except:
        return 1

    return 0


def us_toggle_each_switch(driver: webdriver.Chrome) -> int:
    '''
    4- User able to see device's real state
    5- User able to view each switch state
    6- User able to control each switch state alone
    '''
    func_id = MODULE_ID + '.us_toggle_each_switch'

    # go to living room
    is_living_room = go_to_living_room(driver)
    if not is_living_room:
        return 1

    #grap elements
    try:
        main_switch = get_device_by_name(driver, 'Main Switch Panel')
        buttons = main_switch.find_elements(By.CSS_SELECTOR, 'button')
        state = main_switch.find_element(By.CSS_SELECTOR, '.device_state')
    except:
        return 1
    
    # check all conditions and its corresponding states of toggle buttons
    try:
        for i in range(2**4):
            # turn all switches off
            if state.text == 'ON':
                buttons[1].click()
            # open control panel and turn on corresponding lights
            buttons[0].click()
            switches_4 = driver.find_elements(By.CSS_SELECTOR, '#switch_4ch_btns_cont button')
            switches_states = get_binary_string_specific_length(i, 4)

            for j, s in enumerate(switches_states):
                if s == '1':
                    switches_4[j].click()
                    time.sleep(0.1) #to ensure element has changed
                    if not check_class(switches_4[j], 'switch_4ch_btn_active'):
                        return 1

            remove_dialog(driver)
            if state.text == 'ON' and i == 0:
                return 1
            if state.text == 'OFF' and i != 0:
                return 1
            
            # check if states are sent by invoked correctly 
            buttons[0].click()
            switches_4 = driver.find_elements(By.CSS_SELECTOR, '#switch_4ch_btns_cont button')
            switches_states = get_binary_string_specific_length(i, 4)

            for j, s in enumerate(switches_states):
                if s == '1':
                    if not check_class(switches_4[j], 'switch_4ch_btn_active'):
                        return 1
                else:
                    if check_class(switches_4[j], 'switch_4ch_btn_active'):
                        return 1

            remove_dialog(driver)

    except:
        return 1

    return 0
