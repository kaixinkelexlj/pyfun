#!/usr/bin/python
# coding=utf-8
from string import Template
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': '/home/admin/downloads'}
options.add_experimental_option('prefs', prefs)

options.add_experimental_option('prefs', prefs)
options.add_argument("start-maximized")  # open Browser in maximized mode
options.add_argument("disable-infobars")  # disabling infobars
options.add_argument("--disable-extensions")  # disabling extensions
options.add_argument("--disable-gpu")  # applicable to windows os only
options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
options.add_argument("--no-sandbox")  # Bypass OS security model
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-zygote')

chromeDriverPath = r'/Users/didi/selenium/chromedriver'


def show_search_result(source):
    soup = BeautifulSoup(source, "html.parser")
    # print soup.prettify()
    list = soup.select('div.result')
    for el in list:
        link = el.select("a")[0]
        print link.get("href")
        # print "text[%s]" % (link)


def show_cookie(cookies):
    for cookie in cookies:
        print Template("domain[$domain],name[$name],value[$value],path[$path]").substitute(cookie)


def open_chrome():
    driver = webdriver.Chrome(chromeDriverPath, chrome_options=options)

    try:
        driver.get("https://www.baidu.com")
        kw = driver.find_element_by_css_selector("input[id=kw]")
        print kw.get_attribute("id")
        kw.send_keys(u"python selenium 教程")
        kw.send_keys(Keys.RETURN)
        driver.find_element_by_id("su").click()
        sleep(3)
        print driver.current_url
        show_cookie(driver.get_cookies())
        show_search_result(driver.page_source)
    finally:
        driver.close()
        driver.quit()


open_chrome()

# show_search_result('<div class="result"><a href="https:#www.baidu.com">test</a></div>')
