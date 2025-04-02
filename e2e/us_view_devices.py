from selenium import webdriver
from selenium.webdriver.common.by import By
from e2e.e2e_utils import *
import e2e_data


MODULE_ID = 'e2e.us_devices_tests'
_rooms = e2e_data.rooms
_devices = e2e_data.mapped_devices


def us_view_room_devices(driver: webdriver.Chrome) -> int:
    ''''
    2- User clicks on a room card
    3- The app shows devices in this room
    4- Each device is a card with quick action buttons, connection state and device state
    '''
    func_id = MODULE_ID + '.us_view_room_devices'
    #   log in and save data in local storage
    save_username_pass_local_storage(driver)
    try: 
        
        bottom_bar_options = driver.find_elements(By.CSS_SELECTOR, '#bottom_bar_cont>div')
        bottom_bar_options[0].click()

        rooms_container = driver.find_element(By.CSS_SELECTOR, '#temp_humd_section + div')
        rooms = rooms_container.find_elements(By.CSS_SELECTOR, 'button')
        remove_alert(driver)
        for i, room in enumerate(rooms):
            if room.text != _rooms[i]:
                return 1
            room.click()
            devices_names = driver.find_elements(By.CSS_SELECTOR, '.device_name')
            for j, device_name in enumerate(devices_names):
                if (device_name.text != _devices[i][j]['device_name']):
                    return 1
    except:
        return 1
    return 0
