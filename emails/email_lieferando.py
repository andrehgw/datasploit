#!/usr/bin/env python
# encoding: utf-8
"""
Connect Lieferando-website and test with registration form the extistence
of an account with given email-address

@author:     Andre Fiedler <andre@balticnetwork.de>
@copyright:  Copyright
@license:    GPL
@version:    1.0.0
@contact:    andre@balticnetwork.de
@requires:   Selenium bindings for Python and at least one driver
@see:        http://selenium-python.readthedocs.io/index.html

"""
import base
import vault
import sys
import time

from termcolor import colored
from base import style

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,TimeoutException


# Control whether the module is enabled or not
ENABLED = True


def banner():
    # Write a cool banner here
    '''
    prints banner on stdout
    '''
    # Write a cool banner here
    print colored(style.BOLD + '\n[+] Checking Lieferando\n' + style.END, 'blue')
    pass


def main(email):
    '''
    main functonality
    :param email: email to search for Yahoo account
    :return: dictionary with account information and error messages
    '''
    accountstats = {}
    account_information = []
    account_not_exists_info = []
    account_error = []
    
    url = "https://www.lieferando.de"
    testuser = email
    
    # username and password must be given 
    surname = "Maik Kunze"
    testpassword = "1stVerySecurePassword!"
    
    options = webdriver.FirefoxOptions()
    
    webdriver_headless = vault.get_key('webdriver_headless')
    if webdriver_headless != None and webdriver_headless.lower() == "true":
        options.set_headless(True)
    
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    
    """
    emulate registration of a user to Lieferando. Full ajax stack, so we have 
    to look for error-message tags which'll exist in the DOM if an error occours
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
        #driver.implicitly_wait(3)
        
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
            account_information.append("Lieferando account %s exists" %testuser) 
        except NoSuchElementException, e:
            account_not_exists_info.append("No account %s on Lieferando" %testuser)
        
    except NoSuchElementException, e:
        account_error.append("NoSuchElementException: %s" % e)
    except TimeoutException, e:
        account_error.append("TimeoutException: %s" % e)
    finally:
        driver.close()
    
    
    accountstats['account_information'] = account_information
    accountstats['account_not_exists_info'] = account_not_exists_info
    accountstats['account_error'] = account_error
    
    return accountstats
    


def output(data, email=""):
    '''
    prints account information on stdout
    :param data:  result with account information and error messages
    :param email:
    '''
    # output all errors
    if 'account_error' in data and len(data['account_error']) > 0:
        for cerror in data['account_error']:
            print colored(style.BOLD + "[!] Error: " + cerror + style.END, 'red')
            
    # output for not existing account
    if 'account_not_exists_info' in data and len(data['account_not_exists_info']) > 0:
        for cinfo in data['account_not_exists_info']:
            print colored(style.BOLD + cinfo + style.END, 'yellow')
            
    # output all user information
    if 'account_information' in data and len(data['account_information']) > 0:
        for cinfo in data['account_information']:
            print colored(style.BOLD + cinfo + style.END, 'green')


if __name__ == "__main__":
    try:
        email = sys.argv[1]
        banner()
        result = main(email)
        output(result, email)
    except Exception as e:
        print e
        print "Please provide an email as argument"
