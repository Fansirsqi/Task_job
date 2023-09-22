
from dotenv import load_dotenv
from os import environ
from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from time import sleep
from selenium.webdriver.support import expected_conditions as ECS
import re

load_dotenv()

ck_dic = eval(environ.get("COOKIE_CONFIG").replace(" ", ""))


def set_cookie(driver, cookie_str):
    cookies = {}
    for cookie in cookie_str.split(";"):
        name, value = cookie.strip().split("=", 1)
        cookies[name] = value
    driver.add_cookie(cookies)


options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
set_cookie(driver, ck_dic["fansir"])
driver.get("https://www.52pojie.cn/")
