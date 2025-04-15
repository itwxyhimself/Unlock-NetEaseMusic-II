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
    browser.add_cookie({"name": "MUSIC_U", "value": "00B65373BC1916BA3C4C8A1BFBFB9B1264BA30E19A97246F275C8131CCB326DD07CBE871E7FCEE93EB5708D93608EAF1DE83889919024ED62476F5EB3AB7F517738FDF42B246F0C9DECF01FFD5EC0E86DBBE8F600CAE14D086A4F60CEF7F638DB7C66D28718EE13A73510440810FF07354A0B51F92E4BA1AEF0F83E2C986D46C269E78B081E28D3EB9909E4C72F0F15BC07170AD1F7AECC13C6EEC3B7E6605B7B79BFF8D5CD0D768E59050D0F167C87BDBDDD505F9E41E9C8DA1592169F24B99CF5F25E0ADF841B0D001EB5E8FB9F58DE3CA5FF662A0BB95836A0B317394972976A0992A999F697AA1A78C77EF26F8E579C971022015697AF942A45BC43EC544DD5B94B3EE5CEC8C058C5161FCB8CBC79A978135BC3CB55F0A9513E2C8D3A1CC1147B9CB5F439F22474853F06259F1EF18698CE797D40C368E3814C4B937F8727655F24F1CB5791F39246D0ADD78083A88AC818A4B68E5E2B8589B7F01C3C4A059C6B11AD4ECF3A5755F1879E5A3BC08E5"})
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
