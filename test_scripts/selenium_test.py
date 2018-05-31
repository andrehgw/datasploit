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

from selenium.webdriver.support.ui import WebDriverWait


# Lieferando
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,TimeoutException
 

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
    
    """
    Test for Yahoo
    """
    """
    url = "https://login.yahoo.com"
    testuser = "maik.kunze@freenet.de"
    
    options = webdriver.FirefoxOptions()
    options.set_headless(True)
    
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
    """
    
    """
    Test for Lieferando
    """
    url = "https://www.lieferando.de"
    testuser = "maik.kunze12@freenet.de"
    surname = "Maik Kunze"
    testpassword = "1stVerySecurePassword!"
    
    options = webdriver.FirefoxOptions()
    options.set_headless(True)
    
    driver = webdriver.Firefox(options=options)
    
    driver.get(url)
    
    """
    try a new Lieferando registration - if account already exists, website gives error message
    """
    try:
    
        driver.find_element_by_xpath("//button[@class='menu button-myaccount userlogin']").click()
        
        wait = WebDriverWait(driver, 10)
        createbutton = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-click='register']")))
        createbutton.click()
        
        userfield = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='iaccountuser']")))
        userfield.send_keys(testuser)
        
        surnamefield = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='iaccountsurname']")))
        surnamefield.send_keys(surname)
        
        pass1field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='iaccountpass']")))
        pass1field.send_keys(testpassword)
        
        pass2field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='iaccountpass2']")))
        pass2field.send_keys(testpassword)
        
        checkagb = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='legal']/label[@class='checkbox-inline']")))
        checkagb.click()
        
        registerbutton = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='registerbutton']")))
        registerbutton.click()
                
        # worst case but no other possibility because it comes only html back 
        # for div "userpanel-wrapper", so 3 seconds should be enough to get
        # a AJAX-response
        time.sleep(3)
        
        """
        interpret the result: if there exists already an account, then exist
        the following:
            <div id='userpanel-wrapper'>
               <div id='notification'>
               ...
               </div>
               <form id='iaccountsignupform'>
            </form>
            </div>
        
        if the registration was successful, the div 'userpanel-wrapper' doesn't
        contain the div 'notification' and the form 'iaccountsignupform',
        so testing for existence div and form mentioned shows the email-address
        is already registered or not
        """
        try:
            notification = driver.find_element_by_xpath("//div[@id='notification']")
            signupform = driver.find_element_by_xpath("//form[@id='iaccountsignupform']")
            print "Lieferando %s exists" % testuser
        except NoSuchElementException, e:
            print "Lieferando no account %s " % testuser
        
        
    except NoSuchElementException, e:
        print "Error: %s" % e
    except TimeoutException, e:
        print "Error: %s" % e
    finally:
        driver.close()
    
    
if __name__ == "__main__":
        
    sys.exit(main())