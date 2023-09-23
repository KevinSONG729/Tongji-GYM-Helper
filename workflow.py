import urllib.request as request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains  import ActionChains
import base64
from decorators import retry, validate_input
from word_detection_and_match import get_coordinate
import time
import json
import os

config = {}

@ retry(3, 1)
def login_core(webdriver:webdriver, wait:WebDriverWait):
    wait.until(lambda x: x.find_element(By.CLASS_NAME, 'back-img'))
    while True:
        if "https://ids.tongji.edu.cn:8443/" not in webdriver.current_url:
            return
        back_img = browser.find_element(By.CLASS_NAME, 'back-img')
        back_img_src = back_img.get_attribute('src')[22:]
        back_img_src_b64 = base64.b64decode(back_img_src)
        with open('backimg.png', 'wb') as f:
            f.write(back_img_src_b64)
        target_word = browser.find_element(By.CLASS_NAME, 'verify-msg').text[-6:-1].split(',')
        coordinates = get_coordinate(target_word, 'backimg.png')
        print(coordinates)
        for c in coordinates:
            ActionChains(browser).move_to_element_with_offset(back_img, -200+int(c[1]*config["img_ratio"][0]), -100+int(c[0]*config["img_ratio"][1])).click().perform()
        time.sleep(2)

def login(webdriver:webdriver, student_id:str, password:str):
    wait = WebDriverWait(webdriver, 2000)
    wait.until(lambda x: x.find_element(By.NAME, 'Ecom_User_ID'))
    webdriver.find_element(By.NAME, 'Ecom_User_ID').send_keys(student_id)
    webdriver.find_element(By.NAME, 'Ecom_Password').send_keys(password)
    webdriver.find_element(By.NAME, 'btsubmit').click()
    login_core(webdriver, wait)

def init(config_filepath):
    option_funcs = [webdriver.EdgeOptions, webdriver.ChromeOptions, webdriver.FirefoxOptions, webdriver.SafariOptions, webdriver.IeOptions]
    driver_funcs = [webdriver.Edge, webdriver.Chrome, webdriver.Firefox, webdriver.Safari, webdriver.Ie]
    platform_names = ['Edge', 'Chrome', 'Firefox', 'Safari', 'Ie']
    with open(config_filepath, 'r', encoding='utf-8') as file:
        f = json.load(file)
    f["img_ratio"] = (f["img_width"]/f["img_width_online"], f["img_height"]/f["img_height_online"])
    options = option_funcs[platform_names.index(f["platform"])]()
    if f["is_headless"] == True:
        options.add_argument("--headless")
    if f["firefox_driver_bin_location"] != "":
        os.environ["PATH"] += os.pathsep + f["firefox_driver_bin_location"]
    browser = driver_funcs[platform_names.index(f["platform"])](options=options)
    wait = WebDriverWait(browser, 2000)
    return f, browser, wait

def booking_tennis(browser:webdriver, wait:WebDriverWait, destination_ip:str):
    browser.get(destination_ip)
    wait.until(lambda x: x.find_element(By.CLASS_NAME, 'el-button.el-button--primary'))
    button = browser.find_element(By.CLASS_NAME, 'el-button.el-button--primary').click()
    print(browser.current_url)
    if "https://ids.tongji.edu.cn:8443/" in browser.current_url:
        login(browser, config["student_id"], config["password"]) 
    wait.until(lambda x: x.find_element(By.CLASS_NAME, 'el-button.el-button--text'))
    browser.find_elements(By.CLASS_NAME, 'el-button.el-button--text')[1].click() #首页预约按钮
    check_click_status_and_click(browser, wait, By.XPATH, "//*[contains(text(),"+f"\'{config['GYM_choice']}\'"+")]") #选择场馆
    check_click_status_and_click(browser, wait, By.XPATH, '//*[@id="app"]/div/div[2]/section/main/div[2]/div[2]/form/div[2]/div/div') #点击场地下拉按钮
    check_click_status_and_click(browser, wait, By.XPATH, "//*[contains(text(),"+f"\'{config['playground_choice']}\'"+")]") #选择场地
    check_num_status(wait, By.CLASS_NAME, 'el-radio.lineRadio.is-bordered', 6) #确认周一-周日被加载
    check_click_status_and_click(browser, wait, By.XPATH, "//*[contains(text(),\'"+config['day_choice']+"\')]") #选择星期几
    if config['day_choice'] in ['周一','周二','周三','周四','周五']:
        check_num_status(wait, By.CLASS_NAME, 'el-radio.is-bordered', 5)
    else:
        check_num_status(wait, By.CLASS_NAME, 'el-radio.is-bordered', 12)
    check_click_status_and_click(browser, wait, By.XPATH, "//*[contains(text(),"+f"\' {config['time_choice']}\'"+")]") #选择时间
    check_click_status_and_click(browser, wait, By.CLASS_NAME, 'el-button.el-button--primary') #点击预约按钮
    check_num_status(wait, By.CLASS_NAME, 'el-input__inner', 1)
    browser.find_elements(By.CLASS_NAME, 'el-input__inner')[-1].send_keys(config["partner_student_id"]) #输入同行人学号
    check_num_status(wait, By.CLASS_NAME, 'el-button.el-button--primary', 1)
    # browser.find_elements(By.CLASS_NAME, 'el-button.el-button--primary')[-1].click() #提交
    print('success')
    time.sleep(10)

@validate_input
def check_num_status(wait: WebDriverWait, ByType: By, ByName: str, minnum: int=1):
    print(f"checking num {ByType}:{ByName} > {minnum}...")
    while True:
        if len(wait.until(lambda x:x.find_elements(ByType, ByName)))>minnum:
            time.sleep(2)
            break

@validate_input
def check_click_status_and_click(browser: webdriver, wait: WebDriverWait, ByType: By, ByName: str):
    print(f"checking button {ByType}:{ByName} clickable...")
    try:
        button = wait.until(EC.element_to_be_clickable((ByType, ByName)))
        button.click()
    except ElementClickInterceptedException:
        print("Trying to click on the button again")
        time.sleep(2)
        browser.execute_script("arguments[0].click()", button)

if __name__ == '__main__':
    config, browser, wait = init('config.json')
    booking_tennis(browser, wait, "https://gym.tongji.edu.cn/Pc/#/login")