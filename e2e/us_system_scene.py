from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from e2e.e2e_utils import *
import time

devices = ['Main Switch', 'Main Switch Panel', 'Main Plug', 'Main Dimmer', 'Main Dimmer Panel']
scene_name = 'e2e scene'

MODULE_ID = 'e2e.us_system_scene'


def move_to_scenes(driver: webdriver.Chrome) -> bool:
    try:
        bottom_bar_options = driver.find_elements(By.CSS_SELECTOR, '#bottom_bar_cont>div')
        bottom_bar_options[2].click()
        alert = driver.find_element(By.XPATH, '//*[@role="alert"]')
        remove_alert(driver)
        return True
    except:
        return False


def move_to_home(driver: webdriver.Chrome) -> bool:
    try:
        bottom_bar_options = driver.find_elements(By.CSS_SELECTOR, '#bottom_bar_cont>div')
        bottom_bar_options[0].click()
        return True
    except:
        return False


def add_scene(driver: webdriver.Chrome) -> bool:
    try:
        add_button = driver.find_element(By.CSS_SELECTOR, '.add_button')
        add_button.click()
        return True
    except:
        return False


def perform_power_click(driver: webdriver.Chrome, device_name: str, actions: list[dict]) -> bool:
    try:
        device = get_device_by_name(driver, device_name)
        device.find_elements(By.CSS_SELECTOR, 'button')[1].click()
        if 'Dimmer' in device_name:
            actions.append({"device": device_name, "command": "0"})
        else:
            actions.append({"device": device_name, "command": "TOGGLE"})
        return True
    except:
        return False


def check_actions(dialog: WebElement, expected_actions: list[dict]) -> bool:
    recorded_actions = dialog.find_elements(By.CSS_SELECTOR, '.action_list >*')
    if len(expected_actions) != len(recorded_actions):
        return False
    for expected_action, recorded_action in zip(expected_actions, recorded_actions):
        device_name = recorded_action.find_element(By.CSS_SELECTOR, '.message_field').text.split('\n')[1]
        command = recorded_action.find_element(By.CSS_SELECTOR, '.message_field').text.split('\n')[3]
        if device_name != expected_action.get('device') or command != expected_action.get('command'):
            return False
    return True


def scene_search(driver: webdriver.Chrome, value: str) -> bool:
    try:
        input = driver.find_element(By.CSS_SELECTOR, '#smart_scene_search input')
        input.send_keys(Keys.CONTROL + "a")
        input.send_keys(Keys.DELETE)
        input.send_keys(value)
        return True
    except:
        return False


def get_scenes(driver: webdriver.Chrome) -> list[WebElement] | bool:
    try:
        return driver.find_elements(By.CSS_SELECTOR, '#devices_cont>*')
    except:
        return False


def record_action_save_scene(driver: webdriver.Chrome) -> bool|list:
    add_scene(driver)
    dialog = driver.find_element(By.XPATH, '//*[@role="dialog"]')
    # start recording
    dialog.find_element(By.XPATH, '//*[@aria-label="Record Actions"]').click()
    actions = []
    # perform and record actions
    for device in devices:
        perform_power_click(driver, device, actions)
        
    alert = driver.find_element(By.XPATH, '//*[@role="alert"]')
    remove_alert(driver)
    
    arr = record_states(driver)
        
    # stop recording
    driver.find_element(By.XPATH, '//*[@aria-label="Stop Recording"]').click()

    # check if actions recorded correctly
    dialog = driver.find_element(By.XPATH, '//*[@role="dialog"]')
    if not check_actions(dialog, actions):
        return False

    dialog.find_element(By.CSS_SELECTOR, 'input').send_keys(scene_name)
    driver.find_element(By.XPATH, '//*[@aria-label="Create"]').click()

    # check alert message
    time.sleep(2)
    alert = driver.find_element(By.XPATH, '//*[@role="alert"]')
    if alert.text != "Updated\nSmart Scenes Updated Succesfully":
        return False
    remove_alert(driver)
    return arr


def trigger_action(driver: webdriver.Chrome) -> int:
    scene_search(driver, scene_name)
    scenes = get_scenes(driver)
    if len(scenes) != 1:
        return False
    e2e_scene = scenes[0]
    # trigger action
    time.sleep(1)
    e2e_scene.click()
    time.sleep(1)
    alert = driver.find_element(By.XPATH, '//*[@role="alert"]')
    if alert.text != 'Executed\ne2e scene Executed Succesfully':
        return False
    return True


def record_states(driver: webdriver.Chrome) -> bool:
    states =[]
    for device in devices:
        device_element = get_device_by_name(driver,device)
        states.append(device_element.find_element(By.CSS_SELECTOR,'.device_state').text)
    return states
    
def check_state_flipped(state1,state2):
    if [state1,state2] ==['ON','OFF'] or [state2,state1] ==['ON','OFF'] :
        return True
    return False
    
def us_create_trigger_scene(driver: webdriver.Chrome) -> int:
    func_id = MODULE_ID + '.us_create_trigger_scene'
    '''
        User can create system scenes
        2- User navigates to system scenes page using the bottom bar
        3- User clicks on the plus sign and view the create scene modal
        4- User enters scene name
        5- user selects ison to scene
        6- User clicks on start recording to record actions in this scene
        7- When the app enters recording mode and stop recording button appear
        8- User starts to control home devices as he normaly does
        9- User clicks on bottom button to end recording mode
        10- User see recorded actions list in the create scene modal
        11- User clicks on create to create the scene
        12- The app dispalys a notification when the scene is created
        13- The new scene is added to the scenes list view and can now be triggred
    '''
    save_username_pass_local_storage(driver)
    old_states =record_states(driver)
    if not move_to_scenes(driver):
        return 1

    mediate_states = record_action_save_scene(driver)

    if not mediate_states:
        return 1

    '''
    User can trigger system scenes
    2- User navigates to system scenes page using the bottom bar
    3- User able to delete or view scenes
    4- User can filter scenes using search bar
    5- User trigger a scene by clicking on it
    6- The app dispalys a notification when the scene is triggred
    '''
    
    if not trigger_action(driver):
        return 1
    if not move_to_home(driver):
        return 1
    current_state = record_states(driver)
    #both are equal because we reflected state twice
    for i in range(len(devices)):
        if current_state[i] != old_states[i]:
            return 1
        if not check_state_flipped(current_state[i],mediate_states[i]):
            return 1
        
    return 0
