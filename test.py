# _*_ coding=utf-8 _*_

from selenium import webdriver

driver = webdriver.Chrome()

driver.get("https://www.baidu.com")

print(driver.page_source)