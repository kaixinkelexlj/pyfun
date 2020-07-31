#!/usr/bin/python
# coding=utf-8
import os
import sys
from string import Template
from time import sleep

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

options = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': '/home/admin/downloads'}
options.add_experimental_option('prefs', prefs)
options.add_argument("start-maximized")  # open Browser in maximized mode
options.add_argument("disable-infobars")  # disabling infobars
options.add_argument("--disable-extensions")  # disabling extensions
options.add_argument("--disable-gpu")  # applicable to windows os only
options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
options.add_argument("--no-sandbox")  # Bypass OS security modeloptions.add_argument('--headless')
options.add_argument('--no-zygote')
options.add_argument("--headless")

# chromeDriverPath = r'/usr/bin/chromedriver'
chromeDriverPath = r'/Users/didi/selenium/chromedriver'


def show_cookie(cookies):
    for cookie in cookies:
        print Template("domain[$domain],name[$name],value[$value],path[$path]").substitute(cookie)


def open_chrome(user_name, password):
    driver = webdriver.Chrome(chromeDriverPath, chrome_options=options)
    try:
        # driver.get("http://me.xiaomikeji.com")
        # driver.add_cookie({"name": "language", "value": "zh_CN", "path": "/"})
        print "selenium login start"
        target_page = "http://xx.com/#/projects"
        driver.get(target_page)
        sleep(10)
        print driver.current_url
        driver.save_screenshot("login.png")
        driver.find_element_by_css_selector("input[id=username]").send_keys(user_name)
        driver.find_element_by_css_selector("input[id=password]").send_keys(password)
        driver.find_element_by_css_selector("div.submit").click()
        sleep(10)
        print driver.current_url
        print driver.page_source
        WebDriverWait(driver, 20, 0.5).until(lambda x: target_page in driver.current_url)
        print driver.current_url
        show_cookie(driver.get_cookies())
    finally:
        driver.quit()


print ("%s <username> <password>") % (os.path.dirname(sys.argv[0]))
if len(sys.argv) >= 3:
    open_chrome(sys.argv[1], sys.argv[2])
