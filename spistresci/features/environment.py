import os
from selenium import webdriver


def before_all(context):
    context.base_url = os.environ.get('ST_URL')
    context.driver = webdriver.Chrome()


def after_all(context):
    context.driver.quit()
