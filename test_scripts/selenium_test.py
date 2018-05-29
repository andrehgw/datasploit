#!/usr/local/bin/python2.7
# encoding: utf-8

'''
Created on 28.05.2018

@author: root

@see: http://www.obeythetestinggoat.com/how-to-get-selenium-to-wait-for-page-load-after-a-click.html

@see: http://selenium-python.readthedocs.io/index.html

'''

import time
import sys

from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
 

def wait_for(condition_function):
    start_time = time.time()
    while time.time() < start_time + 3:
        if condition_function():
            return True
        else:
            time.sleep(0.1)
    raise Exception(
        'Timeout waiting for {}'.format(condition_function.__name__)
    )
    
    
class wait_for_page_load(object):

    def __init__(self, browser):
        self.browser = browser

    def __enter__(self):
        self.old_page = self.browser.find_element_by_tag_name('html')

    def page_has_loaded(self):
        new_page = self.browser.find_element_by_tag_name('html')
        return new_page.id != self.old_page.id

    def __exit__(self, *_):
        wait_for(self.page_has_loaded)
        
        
def main():
    url = "https://login.yahoo.com"
    testuser = "john@yahoo.de"
    
    options = webdriver.FirefoxOptions()
    options.set_headless(False)
    
    driver = webdriver.Firefox(options=options)
    
    
        
    driver.get(url)
    
    try:
        #element = WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        with wait_for_page_load(driver):
            driver.find_element_by_id("login-username").send_keys(testuser)
            driver.find_element_by_id("login-signin").click()
        
    except Exception, e:
        sys.stderr.write("Error: " + repr(e) + "\n") 
    
    try:
        errortest = driver.find_element_by_id("username-error")
        if errortest != None:
            print "%s doesn't exist" % testuser
    except NoSuchElementException:
        print "%s exists" %testuser
    
    driver.close()
    
    
if __name__ == "__main__":
        
    sys.exit(main())