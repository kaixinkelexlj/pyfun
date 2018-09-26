# coding=utf-8
import sys

from selenium import webdriver

reload(sys)
sys.setdefaultencoding('utf8')

options = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'd:\\downloads'}
options.add_experimental_option('prefs', prefs)
chromeDriverPath = r'D:\greens\selenium\chromedriver.exe'


def baiduindex(keyword):
    driver = webdriver.Chrome(chromeDriverPath, chrome_options=options);
    # try:
    driver.get("https://index.baidu.com")
    kw_input = driver.find_element_by_id("schword")
    kw_input.send_keys(keyword)
    commit_btn = driver.find_element_by_id("searchWords")
    commit_btn.click()
    # finally:
    # driver.close()
    # driver.quit()


baiduindex(u'三生三世')
