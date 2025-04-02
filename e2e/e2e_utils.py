import socket
import colorama
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import base64
import re
from selenium.webdriver.common.action_chains import ActionChains
import paho.mqtt.client as mqtt_client
import e2e_data

_devices = e2e_data.mapped_devices

WDIWV = 1  # web driver implicit wait time in seconds
server_ip = '127.0.0.1'
mqtt_user_name = 'isi_muser'
mqtt_password = 'oE74zxUFEY35JX5ffyx4zUZTSauYS2zCFVhvL6gZe5bsBCQo3tP2pCS5VrH98mvX'


def elog(func_id: str, msg: str):
    err_tag = f"{colorama.Fore.RED}[ERROR]{colorama.Style.RESET_ALL}"
    print(f"{err_tag} {func_id} | {msg}")


def ilog(func_id: str, msg: str):
    info_tag = f"{colorama.Fore.GREEN}[INFO]{colorama.Style.RESET_ALL}"
    print(f"{info_tag} {func_id} | {msg}")


def js_click(driver: webdriver.Chrome, btn):
    driver.execute_script('arguments[0].click();', btn)


def clear_local_storage(driver: webdriver.Chrome):
    try:
        driver.execute_script("localStorage.clear()")
    except:
        return


def get_local_storage_items(driver: webdriver) -> dict:
    local_storage_length = driver.execute_script("return window.localStorage.length;")
    if local_storage_length == 0:
        return {}
    return driver.execute_script(
        "var ls = window.localStorage, items = {}; "
        "for (var i = 0, k; i < ls.length; ++i) "
        "  items[k = ls.key(i)] = ls.getItem(k); "
        "return items; ")


def get_local_storage_keys(driver: webdriver.Chrome) -> list:
    return driver.execute_script(
        "var ls = window.localStorage, keys = []; "
        "for (var i = 0; i < ls.length; ++i) "
        "  keys[i] = ls.key(i); "
        "return keys; ")


def get_local_storage_item(driver: webdriver.Chrome, key: str) -> str:
    return driver.execute_script("return window.localStorage.getItem(arguments[0]);", key)


def set_local_storage_item(driver: webdriver.Chrome, key: str, value: str) -> None:
    driver.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);", key, value)


def has(self, key):
    return key in self.keys()


def remove(driver: webdriver.Chrome, key: str) -> None:
    driver.execute_script("window.localStorage.removeItem(arguments[0]);", key)


def clear(driver: webdriver.Chrome) -> None:
    driver.execute_script("window.localStorage.clear();")


def save_username_pass_local_storage(driver: webdriver.Chrome) -> None:
    set_local_storage_item(driver, 'mqtt_password', mqtt_password)
    set_local_storage_item(driver, 'mqtt_username', mqtt_user_name)
    driver.refresh()


def go_to_living_room(driver: webdriver.Chrome) -> bool:
    save_username_pass_local_storage(driver)
    # go to living room
    remove_alert(driver)
    try:

        bottom_bar_options = driver.find_elements(By.CSS_SELECTOR, '#bottom_bar_cont>div')
        bottom_bar_options[0].click()
        rooms_container = driver.find_element(By.CSS_SELECTOR, '#temp_humd_section + div')
        rooms = rooms_container.find_elements(By.CSS_SELECTOR, 'button')
        rooms[0].click()  # living room

        return True
    except:
        return False


def get_device_by_name(driver: webdriver.Chrome, name: str) -> WebElement | None:
    try:
        device_cards = driver.find_elements(By.CSS_SELECTOR, '.device_card')
        for d in device_cards:
            if d.find_element(By.CSS_SELECTOR, '.device_name').text == name:
                return d
    except:
        return None


def check_class(element: WebElement, class_name: str) -> bool:
    class_attribute = element.get_attribute("class")
    if class_name in class_attribute.split():
        return True
    return False


def remove_dialog(driver: webdriver.Chrome) -> None:
    try:
        dialog = driver.find_element(By.XPATH, '//*[@role="dialog"]')
        close = dialog.find_element(By.CSS_SELECTOR,'//*[@aria-label ="Close"]')
        close.click()
    except:
        action = ActionChains(driver)
        action.move_by_offset(0, 0).click().perform()


def remove_alert(driver: webdriver.Chrome) -> None:
    alert_remain = True
    while alert_remain:
        try:
            alert = driver.find_element(By.XPATH, '//*[@role="alert"]')
            alert.find_element(By.CSS_SELECTOR, 'div>button').click()
        except:
            alert_remain = False


def get_binary_string_specific_length(value: int, length: int) -> str:
    string = ''
    for i in range(length):
        if value % 2 == 0:
            string += '0'
        else:
            string += '1'
        value = value // 2
    return string


def extract_numbers(text: str) -> list[int]:
    numbers = re.findall(r'\d+', text)
    return numbers


def mqtt_send_notification_simulation(device_name: str) -> None:

    sensor = None
    for device in _devices[0]:
        if device['device_type'] == device_name:
            sensor = device
            break
    device_id = sensor['device_uuid'][-4:]

    _mqtt_client = mqtt_client.Client(client_id=f"isi_device.{device_id}", clean_session=True, userdata=None)
    _mqtt_client.username_pw_set(mqtt_user_name, mqtt_password)
    _mqtt_client.connect(server_ip, keepalive=60)
    _mqtt_client.publish(f"telem/{device_id}/notif")


def mqtt_send_sensor_value(room_id: int, device_name: str, device_sate: int, sensor_type: str) -> None:
    sensor = None
    for device in _devices[room_id]:
        if device['device_type'] == device_name:
            sensor = device
            break
    device_id = sensor['device_uuid'][-4:]

    _mqtt_client = mqtt_client.Client(client_id=f"isi_device.{device_id}", clean_session=True, userdata=None)
    _mqtt_client.username_pw_set(mqtt_user_name, mqtt_password)
    _mqtt_client.connect(server_ip, keepalive=60)
    _mqtt_client.publish(f"state/{device_id}/{sensor_type}", device_sate, retain=True)


def test_screenshot(element: WebElement, image_path: str) -> int:
    # this function takes element from web and compare it to image saved on the file
    comp_as_base64 = element.screenshot_as_base64
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        if encoded_string != comp_as_base64:
            return 1
    return 0


def get_elem_txt(elem: WebElement, css_selector: str) -> str | None:
    try:
        txt_elem = elem.find_element(By.CSS_SELECTOR, css_selector)
        return txt_elem.text
    except:
        return None


def try_get_elem_txt(driver: webdriver.Chrome, css_selector: str) -> str | None:
    TIME_OUT = 100
    for _ in range(TIME_OUT):
        try:
            elem = driver.find_element(By.CSS_SELECTOR, css_selector)
            if elem.text != '':
                return elem.text
        except:
            pass

    return None


def try_get_elem_txts(driver: webdriver.Chrome, css_selector: str) -> list[str] | None:
    TIME_OUT = 100
    elems_txt = []

    def _try_get_elem_txt(elem: WebElement) -> str | None:
        for _ in range(TIME_OUT):
            try:
                if elem.text != '':
                    return elem.text
            except:
                pass

        return None

    for _ in range(TIME_OUT):
        try:
            elems = driver.find_elements(By.CSS_SELECTOR, css_selector)
            elems_txt = [_try_get_elem_txt(elem) for elem in elems]
            if None not in elems_txt:
                return elems_txt
        except:
            pass

    return None


def try_get_elem(driver: webdriver.Chrome, css_selector: str) -> WebElement | None:
    TIME_OUT = 100
    for _ in range(TIME_OUT):
        try:
            elem = driver.find_element(By.CSS_SELECTOR, css_selector)
            return elem
        except:
            pass

    return None


def try_get_elems(driver: webdriver.Chrome, css_selector: str) -> list[WebElement] | None:
    TIME_OUT = 100
    for _ in range(TIME_OUT):
        try:
            elem = driver.find_elements(By.CSS_SELECTOR, css_selector)
            return elem
        except:
            pass

    return None


def try_click(button: WebElement) -> None:
    TIME_OUT = 100
    for _ in range(TIME_OUT):
        try:
            button.click()
            return None
        except:
            pass

    return None
