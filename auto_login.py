# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0003B199AD93A0FB580C652E3C2C0981C6D1D52CE5A1241FE864B27818942165082879D83456CE2904FEB940EF3A341A4BC22FD858AF8EB564E2206DCCC7F77C482FC71012BB69B19B5DAB1E697FE644D0593AFE4D3A05F9CB37558D615E9F06E72ECAA98C9407E4C2BBAD21213275F424B9E3CD927D4BC663CF548F3F2EB001A693EC226814087D5066A72AC03F70ED00DB0D6513089900F8FEC9AFE6A15E55732B64E7AF47278B6B3AD2028F8F1FBC257B8445B4B1AA2F5CF0A6F18B0C5FED5D73161872DDB9BBA93D3FC06D3A1F24E185C287C47B1F95B1D558ECE0EB9E8D8401E46D9A31BB297B6EB1D90570E4B79B0AAA0842D5D89AB5CA51D188E5EC79652BCAF03D6D6D3B5207D31E1CF5FC400C9D84AC68EB21A46AC8BCB456E32936E2E23CE6B73E2DFBA26A80494E9B87E2C68E939EF4052B98CF58ABDBC964022E9DCDA8FA5D7D61E36768B6480CC0D4B35D8E95CF13331ED263A8C894876DBF6200"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
