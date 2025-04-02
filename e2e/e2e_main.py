# autopep8: off
import os
import sys
import json
import glob
import argparse
from selenium import webdriver
from importlib import import_module
from selenium.webdriver.chrome.service import Service
sys.path.append(os.getcwd())
from e2e.e2e_utils import *
# autopep8: on


def create_chrome_test_session() -> webdriver.Chrome:
    func_id = 'e2e.e2e_main.create_chrome_session'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("disable-infobars")
    ilog(func_id, 'Creating Chrome Testing Session')
    _webdriver = webdriver.Chrome()
    return _webdriver


def load_user_stories() -> dict:
    func_id = 'e2e.e2e_main.load_user_stories'
    us_files = glob.glob('e2e/us_*.py')
    us_module_names = [x.split('/')[1].replace('.py', '') for x in us_files]
    us_modules = {module_name: {'module': import_module(module_name)} for module_name in us_module_names}

    # find us functions in each module
    for module_name, module_info in us_modules.items():
        module = module_info['module']
        module_attrs = dir(module)
        us_funcs = [getattr(module, x) for x in module_attrs if x[:3] == 'us_']
        us_funcs = [x for x in us_funcs if callable(x)]
        us_modules[module_name]['us_funcs'] = us_funcs
        us_func_names = [x.__name__ for x in us_funcs]
        us_modules[module_name]['us_func_names'] = us_func_names

    # print found us modules
    us_modules_info = {module_name: module_info['us_func_names'] for module_name, module_info in us_modules.items()}
    ilog(func_id, f"Found US Modules:\n{json.dumps(us_modules_info, indent=2)}")
    return us_modules


def exec_us_func(module_name: str, driver: webdriver.Chrome, us_func):
    ilog(func_id, f"Executing US function: {module_name}.{us_func.__name__}")
    rc = us_func(driver)
    if rc != 0:
        elog(func_id, f"US function: {module_name}.{us_func.__name__} faild [rc={rc}]")
        sys.exit(rc)


if __name__ == "__main__":
    # parse cli arguments
    parser = argparse.ArgumentParser(prog='e2e_main', description='ISIX E2E Testing Program')
    parser.add_argument('--module', '-m', help='E2E Test Module', required=False)
    parser.add_argument('--user-story', '-us', help='E2E Test User Story', required=False)
    args = parser.parse_args()
    func_id = 'e2e.e2e_main'

    # connect to chrome debug session
    chrome_test_session = create_chrome_test_session()
    chrome_test_session.get('http://localhost:5173/')
    chrome_test_session.implicitly_wait(WDIWV)
    us_modules = load_user_stories()

    if args.module and args.user_story:
        target_module_name = args.module
        target_us_func_name = args.user_story
        try:
            target_us_func = [x for x in us_modules[target_module_name]['us_funcs'] if x.__name__ == target_us_func_name][0]
        except:
            elog(func_id, f"US function: {target_module_name}.{target_us_func_name} not Found")
            sys.exit(1)
        exec_us_func(target_module_name, chrome_test_session, target_us_func)

    elif args.user_story:
        target_us_func_name = args.user_story
        try:
            target_us_func = [x for x in us_modules[target_us_func_name]['us_funcs'] if x.__name__ == target_us_func_name][0]
        except:
            elog(func_id, f"US function: {target_us_func_name} not Found")
            sys.exit(1)
        exec_us_func(target_us_func_name, chrome_test_session, target_us_func)

    elif args.module:
        target_module_name = args.module
        if target_module_name not in us_modules:
            elog(func_id, f"US Module: {target_module_name} not Found")
            sys.exit(1)
        for us_func in us_modules[target_module_name]['us_funcs']:
            exec_us_func(target_module_name, chrome_test_session, us_func)

    else:
        # exec all us routines
        for module_name, module_info in us_modules.items():
            for us_func in module_info['us_funcs']:
                exec_us_func(module_name, chrome_test_session, us_func)

    print('E2E testing routine finished successfully')
    chrome_test_session.quit()
