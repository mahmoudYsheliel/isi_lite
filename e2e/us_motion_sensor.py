from selenium import webdriver
from selenium.webdriver.common.by import By
from e2e.e2e_utils import *



MODULE_ID = 'e2e.us_motion_sensor'



def us_control_room_motion_sensor(driver:webdriver.Chrome)->int:
    '''
    3- User able to turn on/off room motion sensor by clicking on device power button
    4- User able to configure room motion sensor security mode
    5- If security mode is enabled the app displays a notification if motion detected
    6- If security mode is disabled room lights are turned on
    '''
    func_id = MODULE_ID + '.us_control_room_motion_sensor'
    # go to living room
    is_living_room = go_to_living_room(driver)
    if not is_living_room:
        return 1
    
    
    
    alert = driver.find_element(By.XPATH, '//*[@role="alert"]')
    alert.find_element(By.CSS_SELECTOR,'button').click()
    
    motion_sensor = get_device_by_name(driver, 'Motion Sensor')
    main_switch = get_device_by_name(driver, 'Main Switch')
    
    if main_switch.find_element(By.CSS_SELECTOR,'.device_state').text == 'ON':
        main_switch.find_elements(By.CSS_SELECTOR,'button')[1].click()

        
    motion_sensor.click()
    dialog = driver.find_element(By.XPATH, '//*[@role="dialog"]')
    
    modes = dialog.find_elements(By.CSS_SELECTOR, '#motion_sensor_mode_cont button')
    header = dialog.find_element(By.CSS_SELECTOR, '.p-dialog-header')
    
    if header.text != 'Motion Sensor':
        return 1
    
    #normal mode test
    modes[0].click()
    
    remove_dialog(driver)
    if motion_sensor.find_element(By.CSS_SELECTOR,'.device_state').text != 'NORMAL':
        return 1
    mqtt_send_notification_simulation('MOTION')
    
    if main_switch.find_element(By.CSS_SELECTOR,'.device_state').text != 'ON':
        return 1
    
    # if button is on remain on
    mqtt_send_notification_simulation('MOTION')
    
    if main_switch.find_element(By.CSS_SELECTOR,'.device_state').text != 'ON':
        return 1
    
    #security mode
    motion_sensor.click()
    dialog = driver.find_element(By.XPATH, '//*[@role="dialog"]')
    modes = dialog.find_elements(By.CSS_SELECTOR, '#motion_sensor_mode_cont button')
    modes[1].click()
    remove_dialog(driver)
    if motion_sensor.find_element(By.CSS_SELECTOR,'.device_state').text != 'SECURITY':
        return 1
    mqtt_send_notification_simulation('MOTION')
    
    alert = driver.find_element(By.XPATH, '//*[@role="alert"]')
    header = alert.find_element(By.CSS_SELECTOR,'.p-toast-message-text>:first-child')
    message = alert.find_element(By.CSS_SELECTOR,'.p-toast-message-text>:last-child')
    
    if header.text != 'Room: Living Room \n Device: Motion Sensor' or message.text != 'Motion Detected':
        return 1
    alert.find_element(By.CSS_SELECTOR,'button').click()
    
    return 0
