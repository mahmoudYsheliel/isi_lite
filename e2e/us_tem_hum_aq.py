from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from e2e.e2e_utils import *
import time

MODULE_ID = 'us_tem_hum_aq'


def us_view_tem_hum_aq(driver:webdriver.Chrome)->int:
    func_id = MODULE_ID + '.us_control_room_motion_sensor'
    
     # go to living room
    is_living_room = go_to_living_room(driver)
    if not is_living_room:
        return 1
    mqtt_send_sensor_value(0,'TEMP',10,'temp_0')
    mqtt_send_sensor_value(0,'AIR_Q',10,'airq_0')
    mqtt_send_sensor_value(0,'HUMD',10,'humd_0')
    
    mqtt_send_sensor_value(1,'TEMP',20,'temp_0')
    mqtt_send_sensor_value(1,'AIR_Q',20,'airq_0')
    mqtt_send_sensor_value(1,'HUMD',20,'humd_0')
    
    temp_val = get_device_by_name(driver,'Temperature Sensor').find_element(By.CSS_SELECTOR,'.device_state').text
    hum_val = get_device_by_name(driver,'Air Quality Sensor').find_element(By.CSS_SELECTOR,'.device_state').text
    air_val =get_device_by_name(driver,'Humidity Sensor').find_element(By.CSS_SELECTOR,'.device_state').text
    
    if int(temp_val) != 10 or int(hum_val) != 10 or int(air_val) != 10:
        return 1
    
    header_states = driver.find_elements(By.CSS_SELECTOR,'.ths_text_cont')
    for state in header_states:
        value = int(re.findall(r'\d+', state.text)[0])
        if value !=10:
            return 1
        
    rooms_container = driver.find_element(By.CSS_SELECTOR, '#temp_humd_section + div')
    rooms = rooms_container.find_elements(By.CSS_SELECTOR, 'button')
    rooms[1].click()  # Bedroom room
    
    temp_val = get_device_by_name(driver,'Temperature Sensor').find_element(By.CSS_SELECTOR,'.device_state').text
    hum_val = get_device_by_name(driver,'Air Quality Sensor').find_element(By.CSS_SELECTOR,'.device_state').text
    air_val =get_device_by_name(driver,'Humidity Sensor').find_element(By.CSS_SELECTOR,'.device_state').text
    time.sleep(3)
    if int(temp_val) != 20 or int(hum_val) != 20 or int(air_val) != 20:
        return 1
    
    header_states = driver.find_elements(By.CSS_SELECTOR,'.ths_text_cont')
    for state in header_states:
        value = int(re.findall(r'\d+', state.text)[0])
        if value !=20:
            return 1

    return 0