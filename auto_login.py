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
    browser.add_cookie({"name": "MUSIC_U", "value": "00B7ED13CBE217B81E0BBD97DD8CE4D230955D020F7A3288AA35549DA96AC04CCBEC041208E5FFBED9D78931AF625607C9C1D5C48C7C6AD59308492D47D5264E4CBEDB9AF53955B7820124073296A28F714759A26BBF46CC351AB4F3B0DF319ED09620B42938046A4274757596F5AD7D26608CC815C38185D39D38AF77B3EC7EE707CB05FAE237581760F2EBD04EDD8B6523A43E09D436D4522CD43426F6B63947135F7FC1D4DEA00593B6DD3A2FB1EF37B33FA2E7B521D378AE217C6B8F85C990FFF46B45E20E7D3F53015BA9903BC62E7554FEE7FE521D232683D443E52DD63F7C7C14307D62B43ADBCE0D8D1606518349299902FC6D0EEAD0BFD063136E6CDB86E207A0005B48E10CA444A3404549FB5FCB45969FE79E792EC2C4A48C582CB0300455833D785C9E89146D70E7221E3A718FE7ADF05D940078D4885F8E264868C4AE47013F16E5A1A3E9F0A891187E57E75A336E56B78D4111E6F61E8E0550813036A1AE1C508BED9A82EE73C19D3F16C3202F1A3E46A2483243E37F297B6065507FA3DF0C4ED803B120BF037123DBB76C8D8EECDFB021A6719C292837ADCE68"})
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
