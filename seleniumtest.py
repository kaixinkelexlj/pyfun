#!/usr/bin/python
# coding=utf-8
from string import Template
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

options = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': '/home/admin/downloads'}
options.add_experimental_option('prefs', prefs)

chromeDriverPath = r'/Users/xulujun/greens/chromedriver'


def show_search_result(source):
    soup = BeautifulSoup(source, "html.parser")
    # print soup.prettify()
    list = soup.select('div.result')
    for el in list:
        link = el.select("a")[0]
        print link.get("href")
        print "text[%s]" % (link.get_text())


def show_cookie(cookies):
    for cookie in cookies:
        print Template("domain[$domain],name[$name],value[$value],path[$path]").substitute(cookie)


def open_chrome():
    driver = webdriver.Chrome(chromeDriverPath, chrome_options=options);
    # webdriver.get("https://www.baidu.com");
    # driver.get('http://sahitest.com/demo/saveAs.htm')
    # driver.find_element_by_xpath('//a[text()="testsaveas.zip"]').click()

    # driver.get("https://work.alibaba-inc.com")

    try:
        driver.get("https://www.baidu.com")
        kw = driver.find_element_by_css_selector("input[id=kw]")
        print kw.get_attribute("id")
        kw.send_keys(u"python selenium 教程")
        kw.send_keys(Keys.RETURN)
        driver.find_element_by_id("su").click()
        sleep(3)
        show_cookie(driver.get_cookies())
        show_search_result(driver.page_source)
    finally:
        driver.close()
        driver.quit()


def alineiwai():
    driver = webdriver.Chrome(chromeDriverPath, chrome_options=options);
    try:
        driver.get("https://work.alibaba-inc.com")
        WebDriverWait(driver, 20, 0.5).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "div.sweetremind-tip")))
        show_cookie(driver.get_cookies())
    finally:
        driver.close()
        driver.quit()


# open_chrome()

alineiwai()


# show_search_result('<div class="result"><a href="https://www.baidu.com">test</a></div>')
