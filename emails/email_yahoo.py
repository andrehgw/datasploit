#!/usr/bin/env python
# encoding: utf-8
"""
Connect yahoo login-page to test if account with email exist. 
For this test we use the errormessage from yahoo if there's no
account for given email.

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
from selenium.common.exceptions import NoSuchElementException

# Control whether the module is enabled or not
ENABLED = True


def wait_for(condition_function):
    '''
    function waits until condition_function returns true or the timeout
    of 3 seconds reached. 
    :param condition_function: 
    :return true if condition_function returns true
    :raise Exception: if timeout occurs 
    '''
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
    '''
    class is used as condition for waiting for request
    :see wait_for()
    '''

    def __init__(self, browser):
        self.browser = browser

    def __enter__(self):
        self.old_page = self.browser.find_element_by_tag_name('html')

    def page_has_loaded(self):
        new_page = self.browser.find_element_by_tag_name('html')
        return new_page.id != self.old_page.id

    def __exit__(self, *_):
        wait_for(self.page_has_loaded)



def banner():
    '''
    prints banner on stdout
    '''
    # Write a cool banner here
    print colored(style.BOLD + '\n[+] Checking Yahoo\n' + style.END, 'blue')
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
    
    url = "https://login.yahoo.com"
    testuser = email
    
    options = webdriver.FirefoxOptions()
    
    webdriver_headless = vault.get_key('webdriver_headless')
    if webdriver_headless != None and webdriver_headless.lower() == "true":
        options.set_headless(True)
    
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    
    # fill login form and press the "further"-button
    try:
        #element = WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        with wait_for_page_load(driver):
            driver.find_element_by_id("login-username").send_keys(testuser)
            driver.find_element_by_id("login-signin").click()
        
    except Exception, e:
        account_error.append("error: %s" % repr(e))
    
    """
    If there doesn't exist an account with given email, Yahoo presents
    a red error message on the page. This is represented by the following tag
    after pressing the "further"-button:
    
    <p id="username-error" class="row error" role="alert" 
       data-error="messages.ERROR_INVALID_USERNAME">
       Diese E-Mail-Adresse ist uns leider nicht&nbsp;bekannt.
    </p>
    
    So if we don't have this element in the DOM, we can suspect, an
    account with given email exists.
    """
    try:
        errortest = driver.find_element_by_id("username-error")
        if errortest != None:
            account_not_exists_info.append("No account %s on Yahoo" % testuser)
    except NoSuchElementException:
        account_information.append("Yahoo account %s exists" %testuser) 
    
    
    
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
