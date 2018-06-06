#!/usr/bin/env python
# encoding: utf-8

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
    print colored(style.BOLD + '\n[+] Checking T-Online.de\n' + style.END, 'blue')
    pass


def main(accountname):
    '''
    main functonality
    :param email: email to search for Yahoo account
    :return: dictionary with account information and error messages
    '''
    accountstats = {}
    account_information = []
    account_not_exists_info = []
    account_error = []
    
    
    url = "https://meinkonto.telekom-dienste.de/wiederherstellung/passwort/index.xhtml"
    options = webdriver.FirefoxOptions()
    
    webdriver_headless = vault.get_key('webdriver_headless')
    if webdriver_headless != None and webdriver_headless.lower() == "true":
        options.set_headless(True)
    
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    
    
    try:
        wait = WebDriverWait(driver, 10)
        userfield = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@class='form-input'][@type='text']")))
        userfield.send_keys(accountname)
        
        furtherbutton = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        furtherbutton.click()
        
        # worst case but no other possibility because it comes only xml back, 
        # in case of success the client starts a new get request, in case the
        # account name doesn't exist, the client only shows the error message
        # beyond the input field
        time.sleep(3)
        
        try:
            errormessagediv = driver.find_element_by_xpath("//div[contains(@class,'decoration-negative')]")
            # here we go only without exception ;-)
            account_not_exists_info.append("No account %s on T-Online.de" % accountname)
        except NoSuchElementException, e:
            account_information.append("T-Online account %s exists" % accountname) 
        
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


def output(data, accountname=""):
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
        accountname = sys.argv[1]
        banner()
        result = main(accountname)
        output(result, accountname)
    except Exception as e:
        print e
        print "Please provide a accountname as argument"
