from selenium import webdriver
from selenium.webdriver.common.by import By
from e2e.e2e_utils import *
import time


MODULE_ID = 'e2e.us_main_dimmer_panel'


def us_toggle_all_buttons(driver: webdriver.Chrome) -> int:
    '''    
    3- User able to turn off room dimmer by clicking on device power button
    4- User able to view dimmer controls modal when clicking on card body
    '''

    func_id = MODULE_ID + '.us_toggle_all_buttons'

    # go to living room
    is_living_room = go_to_living_room(driver)
    if not is_living_room:
        return 1
   
    # check header and check state in case of 'OFF' state
    try:
        main_Dimmer = get_device_by_name(driver, 'Main Dimmer Panel')
        buttons = main_Dimmer.find_elements(By.CSS_SELECTOR, 'button')
        state = main_Dimmer.find_element(By.CSS_SELECTOR, '.device_state')
        # turn off dimmer 
        if state.text == 'ON':
            buttons[1].click()
        if state.text != 'OFF':
            return 1
        
        
         # popup dialog
        try_click(buttons[0])
        header = driver.find_element(By.CSS_SELECTOR, '.p-dialog-header')
        time.sleep(0.1)
        if header.text != 'Main Dimmer Panel':
            return 1
        
        dimmers_modules_container = driver.find_elements(By.CSS_SELECTOR, '.dimmer_module_container')

        
        # check number of buttons and their states
        if len(dimmers_modules_container) != 4:
            return 1
        
        
        for dimmer_module in dimmers_modules_container:
            light_intensity = dimmer_module.find_element(By.CSS_SELECTOR, '.dimmer_state_view')
            if extract_numbers(light_intensity.text)[0] != '0':
                return 1
            
        dimmer_module_container1 = dimmers_modules_container[0]
        dimmer_module_container2 = dimmers_modules_container[1]
        dimmer_module_container3 = dimmers_modules_container[2]
        dimmer_module_container4 = dimmers_modules_container[3]
        
        dimmer_module_container1_btns = dimmer_module_container1.find_elements(By.CSS_SELECTOR, '.dimmer_btns_cont>button')
        dimmer_module_container2_btns = dimmer_module_container2.find_elements(By.CSS_SELECTOR, '.dimmer_btns_cont>button')
        dimmer_module_container3_btns = dimmer_module_container3.find_elements(By.CSS_SELECTOR, '.dimmer_btns_cont>button')
        dimmer_module_container4_btns = dimmer_module_container4.find_elements(By.CSS_SELECTOR, '.dimmer_btns_cont>button')

        # check all buttins states
        for btn in range(4):

            if check_class(dimmer_module_container1_btns[btn], 'dimmer_btn_active') and btn != 0:
                return 1
            if not check_class(dimmer_module_container1_btns[btn], 'dimmer_btn_active') and btn == 0:
                return 1
            if check_class(dimmer_module_container2_btns[btn], 'dimmer_btn_active') and btn != 0:
                return 1
            if not check_class(dimmer_module_container2_btns[btn], 'dimmer_btn_active') and btn == 0:
                return 1
            if check_class(dimmer_module_container2_btns[btn], 'dimmer_btn_active') and btn != 0:
                return 1
            if not check_class(dimmer_module_container2_btns[btn], 'dimmer_btn_active') and btn == 0:
                return 1
            if check_class(dimmer_module_container3_btns[btn], 'dimmer_btn_active') and btn != 0:
                return 1
            if not check_class(dimmer_module_container3_btns[btn], 'dimmer_btn_active') and btn == 0:
                return 1
        
        remove_dialog(driver)
        
    except:
        return 1
    
    
    # check header and check state in case of 'ON' state
    try:
        main_Dimmer = get_device_by_name(driver, 'Main Dimmer Panel')
        buttons = main_Dimmer.find_elements(By.CSS_SELECTOR, 'button')
        state = main_Dimmer.find_element(By.CSS_SELECTOR, '.device_state')
        # turn off dimmer 
        buttons[1].click()
        if state.text != 'ON':
            return 1
        
         # popup dialog
        try_click(buttons[0])

        dimmers_modules_container = driver.find_elements(By.CSS_SELECTOR, '.dimmer_module_container')

        for dimmer_module in dimmers_modules_container:
            light_intensity = dimmer_module.find_element(By.CSS_SELECTOR, '.dimmer_state_view')
            if extract_numbers(light_intensity.text)[0] != '100':
                return 1
            
        dimmer_module_container1 = dimmers_modules_container[0]
        dimmer_module_container2 = dimmers_modules_container[1]
        dimmer_module_container3 = dimmers_modules_container[2]
        dimmer_module_container4 = dimmers_modules_container[3]
        
        dimmer_module_container1_btns = dimmer_module_container1.find_elements(By.CSS_SELECTOR, '.dimmer_btns_cont>button')
        dimmer_module_container2_btns = dimmer_module_container2.find_elements(By.CSS_SELECTOR, '.dimmer_btns_cont>button')
        dimmer_module_container3_btns = dimmer_module_container3.find_elements(By.CSS_SELECTOR, '.dimmer_btns_cont>button')
        dimmer_module_container4_btns = dimmer_module_container4.find_elements(By.CSS_SELECTOR, '.dimmer_btns_cont>button')

        # check all buttins states
        for btn in range(4):
            if check_class(dimmer_module_container1_btns[btn], 'dimmer_btn_active') and btn != 3:
                return 1
            if not check_class(dimmer_module_container1_btns[btn], 'dimmer_btn_active') and btn == 3:
                return 1
            if check_class(dimmer_module_container2_btns[btn], 'dimmer_btn_active') and btn != 3:
                return 1
            if not check_class(dimmer_module_container2_btns[btn], 'dimmer_btn_active') and btn == 3:
                return 1
            if check_class(dimmer_module_container3_btns[btn], 'dimmer_btn_active') and btn != 3:
                return 1
            if not check_class(dimmer_module_container3_btns[btn], 'dimmer_btn_active') and btn == 3:
                return 1
            if check_class(dimmer_module_container4_btns[btn], 'dimmer_btn_active') and btn != 3:
                return 1
            if not check_class(dimmer_module_container4_btns[btn], 'dimmer_btn_active') and btn == 3:
                return 1
        
        remove_dialog(driver)
        
    except:
        return 1

    return 0





def us_toggle_each_button(driver: webdriver.Chrome) -> int:
    '''    
    5- User able to toggle 4 dim levels on the device
    6- The dim level is shown on both the slider and controls
    '''

    func_id = MODULE_ID + '.us_toggle_each_button'

    # go to living room
    is_living_room = go_to_living_room(driver)
    if not is_living_room:
        return 1
    # grap elements
    try:
        main_Dimmer = get_device_by_name(driver, 'Main Dimmer Panel')
        buttons = main_Dimmer.find_elements(By.CSS_SELECTOR, 'button')
        state = main_Dimmer.find_element(By.CSS_SELECTOR, '.device_state')
    except:
        return 1
    

    # check all possible conditions and its corresponding button state
    values = ['0', '33', '66', '100']
    

    for i in range(4):
        for j in range(4):
            for k in range(4):
               for l in range(4):
                    # open control panel and turn on corresponding lights

                    try_click(buttons[0])
                    dialog = driver.find_element(By.XPATH, '//*[@role="dialog"]')
                    dimmer_module_container1 = dialog.find_elements(By.CSS_SELECTOR, '.dimmer_module_container')[0]
                    dimmer_module_container2 = dialog.find_elements(By.CSS_SELECTOR, '.dimmer_module_container')[1]
                    dimmer_module_container3 = dialog.find_elements(By.CSS_SELECTOR, '.dimmer_module_container')[2]
                    dimmer_module_container4 = dialog.find_elements(By.CSS_SELECTOR, '.dimmer_module_container')[3]

                    dimmer_module_container1_btns = dimmer_module_container1.find_elements(By.CSS_SELECTOR, '.dimmer_btns_cont>button')
                    dimmer_module_container2_btns = dimmer_module_container2.find_elements(By.CSS_SELECTOR, '.dimmer_btns_cont>button')
                    dimmer_module_container3_btns = dimmer_module_container3.find_elements(By.CSS_SELECTOR, '.dimmer_btns_cont>button')
                    dimmer_module_container4_btns = dimmer_module_container4.find_elements(By.CSS_SELECTOR, '.dimmer_btns_cont>button')

                    # click corresponding buttons
                    dimmer_module_container1_btns[i].click()
                    dimmer_module_container2_btns[j].click()
                    dimmer_module_container3_btns[k].click()
                    dimmer_module_container4_btns[l].click()

                    time.sleep(0.1)

                    # check light intensity value
                    light_intensity = dimmer_module_container1.find_element(By.CSS_SELECTOR, '.dimmer_state_view')
                    if extract_numbers(light_intensity.text)[0] != values[i]:
                        return 1

                    light_intensity = dimmer_module_container2.find_element(By.CSS_SELECTOR, '.dimmer_state_view')
                    if extract_numbers(light_intensity.text)[0] != values[j]:
                        return 1
                    
                    light_intensity = dimmer_module_container3.find_element(By.CSS_SELECTOR, '.dimmer_state_view')
                    if extract_numbers(light_intensity.text)[0] != values[k]:
                        return 1

                    light_intensity = dimmer_module_container4.find_element(By.CSS_SELECTOR, '.dimmer_state_view')
                    if extract_numbers(light_intensity.text)[0] != values[l]:
                        return 1

                    # check all buttins states
                    for btn in range(4):

                        if check_class(dimmer_module_container1_btns[btn], 'dimmer_btn_active') and btn != i:
                            return 1
                        if not check_class(dimmer_module_container1_btns[btn], 'dimmer_btn_active') and btn == i:
                            return 1
                        if check_class(dimmer_module_container2_btns[btn], 'dimmer_btn_active') and btn != j:
                            return 1
                        if not check_class(dimmer_module_container2_btns[btn], 'dimmer_btn_active') and btn == j:
                            return 1
                        
                        
                        if check_class(dimmer_module_container3_btns[btn], 'dimmer_btn_active') and btn != k:
                            return 1
                        if not check_class(dimmer_module_container3_btns[btn], 'dimmer_btn_active') and btn == k:
                            return 1
                        if check_class(dimmer_module_container4_btns[btn], 'dimmer_btn_active') and btn != l:
                            return 1
                        if not check_class(dimmer_module_container4_btns[btn], 'dimmer_btn_active') and btn == l:
                            return 1

                    remove_dialog(driver)
                    if state.text == 'ON' and i == 0 and j == 0 and k == 0 and l == 0:
                        return 1
                    if state.text == 'OFF' and (i != 0 or j != 0 or k != 0 or l != 0):
                        return 1
                    # check if states are sent by invoked correctly 
                    
                    try_click(buttons[0])
                    dialog = driver.find_element(By.XPATH, '//*[@role="dialog"]')
                    dimmer_module_container1 = dialog.find_elements(By.CSS_SELECTOR, '.dimmer_module_container')[0]
                    dimmer_module_container2 = dialog.find_elements(By.CSS_SELECTOR, '.dimmer_module_container')[1]
                    dimmer_module_container3 = dialog.find_elements(By.CSS_SELECTOR, '.dimmer_module_container')[2]
                    dimmer_module_container4 = dialog.find_elements(By.CSS_SELECTOR, '.dimmer_module_container')[3]

                    dimmer_module_container1_btns = dimmer_module_container1.find_elements(By.CSS_SELECTOR, '.dimmer_btns_cont>button')
                    dimmer_module_container2_btns = dimmer_module_container2.find_elements(By.CSS_SELECTOR, '.dimmer_btns_cont>button')
                    dimmer_module_container3_btns = dimmer_module_container3.find_elements(By.CSS_SELECTOR, '.dimmer_btns_cont>button')
                    dimmer_module_container4_btns = dimmer_module_container4.find_elements(By.CSS_SELECTOR, '.dimmer_btns_cont>button')


                    # check light intensity value
                    light_intensity = dimmer_module_container1.find_element(By.CSS_SELECTOR, '.dimmer_state_view')
                    if extract_numbers(light_intensity.text)[0] != values[i]:
                        return 1

                    light_intensity = dimmer_module_container2.find_element(By.CSS_SELECTOR, '.dimmer_state_view')
                    if extract_numbers(light_intensity.text)[0] != values[j]:
                        return 1
                    
                    light_intensity = dimmer_module_container3.find_element(By.CSS_SELECTOR, '.dimmer_state_view')
                    if extract_numbers(light_intensity.text)[0] != values[k]:
                        return 1

                    light_intensity = dimmer_module_container4.find_element(By.CSS_SELECTOR, '.dimmer_state_view')
                    if extract_numbers(light_intensity.text)[0] != values[l]:
                        return 1
                    
                    # check all buttins states
                    for btn in range(4):
                        if check_class(dimmer_module_container1_btns[btn], 'dimmer_btn_active') and btn != i:
                            return 1
                        if not check_class(dimmer_module_container1_btns[btn], 'dimmer_btn_active') and btn == i:
                            return 1
                        if check_class(dimmer_module_container2_btns[btn], 'dimmer_btn_active') and btn != j:
                            return 1
                        if not check_class(dimmer_module_container2_btns[btn], 'dimmer_btn_active') and btn == j:
                            return 1
                        if check_class(dimmer_module_container3_btns[btn], 'dimmer_btn_active') and btn != k:
                            return 1
                        if not check_class(dimmer_module_container3_btns[btn], 'dimmer_btn_active') and btn == k:
                            return 1
                        if check_class(dimmer_module_container4_btns[btn], 'dimmer_btn_active') and btn != l:
                            return 1
                        if not check_class(dimmer_module_container4_btns[btn], 'dimmer_btn_active') and btn == l:
                            return 1
                        
                    remove_dialog(driver)
                    print(i,j,k,l)
    return 0
