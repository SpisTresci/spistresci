# -*- coding: utf-8 -*-

import logging
import time

from django.core.management.base import BaseCommand

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

logger = logging.getLogger('afiliant_update_logger')

class Command(BaseCommand):

    login_url = 'https://ssl.afiliant.com/wydawcy/logowanie'
    login_username = 'spistresci'
    login_password = 'pomyslowo42'
    xml_urls = [
        'http://www.afiliant.com/publisher/index.php?c=Xml&format=&id_shop=&sort=&page=1',
        'http://www.afiliant.com/publisher/index.php?c=Xml&format=&id_shop=&sort=&page=2'
    ]

    def handle(self, *args, **options):
        self.driver = webdriver.Firefox()
        if not self.login():
            return
        self.update_xml_files()
        self.driver.quit()


    def login(self):
        def login_load_completed(d):
            return d.execute_script("return document.readyState") == "complete" and \
                self.login_url in d.current_url

        def login_completed(d):
            return d.execute_script("return document.readyState") == "complete" and \
                'http://www.afiliant.com/publisher/index.php' in d.current_url

        try:
            self.driver.get(self.login_url)
            WebDriverWait(self.driver, 30).until(login_load_completed)
        except:
            return False

        self.driver.execute_script("return document.getElementById('login').value = '%s';" % self.login_username)
        self.driver.execute_script("return document.getElementById('haslo').value = '%s';" % self.login_password)
        submit_btn = self.driver.find_element_by_css_selector("a#zaloguj")

        try:
            submit_btn.submit()
            WebDriverWait(self.driver, 30).until(login_completed)
        except:
            return False
        return True

    def update_xml_files(self):
        logger.info('*'*20)
        logger.info('start')
        for url in self.xml_urls:
            def load_completed(d):
                return d.execute_script("return document.readyState") == "complete" and \
                    url in d.current_url

            eor = False  # end of rows
            clicked_links = []
            while(not eor):
                not_clicked = 0
                self.driver.get(url)
                WebDriverWait(self.driver, 60).until(load_completed)
                rows = self.driver.find_elements_by_css_selector('table.table_thin tr')
                for row in rows[1:]:  # [1:] skips header
                    try:
                        row_id = row.get_attribute('id')
                    except:
                        break

                    try:
                        btn = row.find_element_by_css_selector('a.update')
                    except:
                        not_clicked += 1
                        continue
                    else:
                        href = btn.get_attribute('href')
                        if href in clicked_links:
                            not_clicked += 1
                            continue
                        btn.click()
                        time.sleep(3)
                        clicked_links.append(href)
                if not_clicked >= len(clicked_links):
                    eor = True
                logger.info('end of row')