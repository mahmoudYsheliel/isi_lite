from selenium import webdriver
from selenium.webdriver.common.by import By
from e2e.e2e_utils import *
from selenium.webdriver.common.keys import Keys
import time


MODULE_ID = 'e2e.us_network_profile'


true_data = ['isi_lite', server_ip, mqtt_user_name, mqtt_password]
false_data = ['false profile network', 'false broker', 'false username', 'false password']

false_profiles = []
for i in ['0','1']:
    copy = [data + i for data in false_data]
    false_profiles.append(copy)
    
profile_with_missing_field =[]    
for i in range(4):
    copy = false_data.copy()
    copy[i] = ''
    profile_with_missing_field.append(copy)
    
    

'''
    2- uer abe to view network profiles 
    3- user able to connect profile from profiles and get highlighted
    4- user able to view profile name, broker, username, password
    5- user able to edit any of the previous fields
    6- user able to delete profile
    7- user able to add profile
    8- user able to test connection to profile
'''


def check_actions(buttons: list[WebElement]) -> bool:
    if buttons[0].is_enabled() or buttons[0].text != 'Connect':
        return False
    if buttons[1].is_enabled() or buttons[1].text != 'Save':
        return False
    if buttons[2].is_enabled() or buttons[2].text != 'Test':
        return False
    return True


def check_fields(fields: list[WebElement]) -> bool:
    if fields[0].text != 'Profile Name:' or fields[1].text != 'Broker IP:' or fields[2].text != 'Username:' or fields[3].text != 'Password:':
        return False
    return True


def add_data_to_input_fields(fields: list[WebElement], data: list[str]) -> bool:
    if len(fields) != 4 or len(data) != 4:
        return
    # clear fields first
    for i, field in enumerate(fields):
        field.find_element(By.CSS_SELECTOR, 'input').send_keys(Keys.CONTROL + "a")
        field.find_element(By.CSS_SELECTOR, 'input').send_keys(Keys.DELETE)
        field.find_element(By.CSS_SELECTOR, 'input').send_keys(data[i])
    return True


def test_profile(driver: webdriver.Chrome, profile: WebElement, expected_success: bool) -> bool:
    test_button = profile.find_elements(By.CSS_SELECTOR, '.field_actions>button')[2]
    if not test_button.is_enabled():
        return False
    test_button.click()
    time.sleep(2)  # wait untill connnected
    test_button = profile.find_elements(By.CSS_SELECTOR, '.field_actions>button')[2]
    background_color = test_button.value_of_css_property('background-color')

    alert = None
    try:
        alert = driver.find_element(By.XPATH, '//*[@role="alert"]')
    except:
        return False
    if not alert:
        return False

    if expected_success:
        if background_color != 'rgba(22, 163, 74, 1)':
            return False
        if alert.text != 'Success\nTest Connection Succeded':
            return False

    if not expected_success:
        if background_color != 'rgba(220, 38, 38, 1)':
            return False
        if alert.text != 'Failure\nTest Connection Failed':
            return False
    return True


def connect_profile(driver: webdriver.Chrome, profile: WebElement, expected_success: bool) -> bool:
    connect_button = profile.find_elements(By.CSS_SELECTOR, '.field_actions>button')[0]
    if not connect_button.is_enabled():
        return False
    connect_button.click()
    time.sleep(2)  # wait untill connnected
    alert = None
    try:
        alert = driver.find_element(By.XPATH, '//*[@role="alert"]')
    except:
        return False
    if not alert:
        return False
    if expected_success:
        if alert.text != 'Connected\nConnected to ISI Device Network':
            return False

    if not expected_success:
        if alert.text != 'Failure\nTest Connection Failed':
            return False

    return True



def check_add_missing_data_profile(driver:webdriver.Chrome)->bool:
    clear_local_storage(driver)
    if not move_to_notwork_profile(driver):
        return False
    # test adding one profile
    add_button = driver.find_element(By.CSS_SELECTOR, '.add_button')
    add_button.click()
    netwok_field = driver.find_element(By.CSS_SELECTOR, '.ISInetwork_profile>*')
    actions = netwok_field.find_elements(By.CSS_SELECTOR, '.field_actions>button')
    text_input_fields = netwok_field.find_elements(By.CSS_SELECTOR, '.element')
    header = netwok_field.find_element(By.CSS_SELECTOR, '.p-fieldset-legend')

    # check actions are disabled and header is untitled
    if not (check_actions(actions) and check_fields(text_input_fields) and header.text == 'Untitled'):
        return False

    # add data with missing field and check action buttons
    for i in range(4):
        add_data_to_input_fields(text_input_fields, profile_with_missing_field[i])
        actions = netwok_field.find_elements(By.CSS_SELECTOR, '.field_actions>button')
        if not check_actions(actions):
            return False
    return True
        
        
        
def check_save_two_profiles(driver:webdriver.Chrome)->bool:
    add_button = driver.find_element(By.CSS_SELECTOR, '.add_button')
    # add one more profiles > refresh > check if they are saved
    add_button.click()
    netwok_fields = driver.find_elements(By.CSS_SELECTOR, '.ISInetwork_profile>*')
    for i, netwok_field in enumerate(netwok_fields):
        text_input_fields = netwok_field.find_elements(By.CSS_SELECTOR, '.element')
        add_data_to_input_fields(text_input_fields,false_profiles[i])
        # save profile
        netwok_field.find_elements(By.CSS_SELECTOR,'div>button')[1].click()
    driver.refresh()
    if not move_to_notwork_profile(driver):
        return False
    
    netwok_fields = driver.find_elements(By.CSS_SELECTOR, '.ISInetwork_profile>*')
    if len(netwok_fields) != 2:
        return False
    for i, netwok_field in enumerate(netwok_fields):
        text_input_fields = netwok_field.find_elements(By.CSS_SELECTOR, '.element')
        profile_data=[]
        for text_input_field in text_input_fields:
            profile_data.append(text_input_field.find_element(By.CSS_SELECTOR,'input').get_attribute('value'))
        #check if profile data is correct
        if profile_data not in false_profiles:
            return False
    return True
        
def check_delete_profile(driver:webdriver.Chrome)->bool:
    # delete first profile and check
    remove_alert(driver)
    netwok_fields = driver.find_elements(By.CSS_SELECTOR, '.ISInetwork_profile>*')
    deleted_profile_name =netwok_fields[0].find_element(By.CSS_SELECTOR,'.fieldset_header>span').text
    deleted_profile_order = re.search(r'\d+(\.\d+)?', deleted_profile_name).group()
    netwok_fields[0].find_element(By.CSS_SELECTOR,'.fieldset_header>i').click()
    driver.refresh()
    # check if the other profile is saved
    if not move_to_notwork_profile(driver):
        return False
    
    netwok_fields = driver.find_elements(By.CSS_SELECTOR, '.ISInetwork_profile>*')
    if len(netwok_fields) != 1:
        return False
    
    text_input_fields = netwok_fields[0].find_elements(By.CSS_SELECTOR, '.element')
    for i,text_input_field in enumerate(text_input_fields):
        #check if profile data is correct
        data =text_input_field.find_element(By.CSS_SELECTOR,'input').get_attribute('value')
        if data != false_profiles[1-int(deleted_profile_order)][i]:
            return False
    return True
        
        
def move_to_notwork_profile(driver:webdriver.Chrome)->bool:
    try:
        bottom_bar_options = driver.find_elements(By.CSS_SELECTOR, '#bottom_bar_cont>div')
        bottom_bar_options[3].click()
        return True
    except:
        return False
        
######################################################## User Stories ###################################

def us_control_network_profiles(driver: webdriver.Chrome) -> int:
    '''
    1- user able to open configurations
    2- uer abe to view network profiles
    4- user able to view profile name, broker, username, password 
    5- user able to edit any of the previous fields
    6- user able to delete profile
    7- user able to add profile
    '''
    func_id = MODULE_ID + '.us_control_network_profiles'

    if not check_add_missing_data_profile(driver):
        return 1
    # cheeck added profiles
    if not check_save_two_profiles(driver):
        return 1
    # check deleting profile
    if not check_delete_profile(driver):
        return 1
    
    
    return 0


def us_test_and_connect_profile(driver:webdriver.Chrome)->int:
    '''
        3- user able to connect profile from profiles and get highlighted
        8- user able to test connection to profile
    '''
    #  clear local storage move to network profile
    try:
        clear_local_storage(driver)
        bottom_bar_options = driver.find_elements(By.CSS_SELECTOR, '#bottom_bar_cont>div')
        bottom_bar_options[3].click()
    except:
        return 1
    
    clear_local_storage(driver)
    if not move_to_notwork_profile(driver):
        return False
    
    alert = driver.find_element(By.XPATH, '//*[@role="alert"]')
    remove_alert(driver)
    
    # add profile
    add_button = driver.find_element(By.CSS_SELECTOR, '.add_button')
    add_button.click()
    netwok_field = driver.find_element(By.CSS_SELECTOR, '.ISInetwork_profile>*')
    text_input_fields = netwok_field.find_elements(By.CSS_SELECTOR, '.element')
    
    
    # test profile wrong data
    add_data_to_input_fields(text_input_fields,false_data)
    if not test_profile(driver,netwok_field,False):
        return 1
    
    # test profile correct data
    add_data_to_input_fields(text_input_fields,true_data)
    if not test_profile(driver,netwok_field,True):
        return 1
    
    
    
    # connect profile wrong data
    add_data_to_input_fields(text_input_fields,false_data)
    if not connect_profile(driver,netwok_field,False):
        return 1
    
    # connect profile correct data
    add_data_to_input_fields(text_input_fields,true_data)
    if not connect_profile(driver,netwok_field,True):
        return 1
    return 0
    