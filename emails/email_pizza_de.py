#!/usr/bin/env python
# encoding: utf-8
"""
Connect the website pizza.de and test with the passwort reset form
the existence of an account with given email

@author:     Andre Fiedler <andre@balticnetwork.de>
@copyright:  Copyright
@license:    GPL
@version:    1.0.0
@contact:    andre@balticnetwork.de

"""
import base
import vault
import sys

import requests
import json

from termcolor import colored
from base import style

# Control whether the module is enabled or not
ENABLED = True


def banner():
    '''
    prints banner on stdout
    '''
    # Write a cool banner here
    print colored(style.BOLD + '\n[+] Checking pizza.de\n' + style.END, 'blue')
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
    
    try:
        s = requests.Session()
        s.headers.update({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
        s.headers.update({'Accept':'application/vnd.deliveryhero.v2.12+json'})
        s.headers.update({'Accept-Encoding':'gzip, deflate, br'})
        s.headers.update({'content-type':'text/plain;charset=UTF-8'})
        s.headers.update({'Authentication':'LH api-key=BqFXeTedMu1LQazCYZznkzyL5CFffcWIDW7GEpmCFVAPLi1dA4cdt76BnXkyEuqWAbCf8ZWtADOzaz5851LQj1dlppQVZSxPPAe0cA0g7Tn2GoXWTdfStKk5yrKrrB0J'})
        
        payload = {'email':email,'op':'reset'}
        
        r = s.put('https://pizza.de/dowant-api/authorization/', data=json.dumps(payload))
        
        # status code HTTP 200 and empty - then an account exists
        if int(r.status_code) == 200 and len(json.loads(r.content))==0:
            account_information.append("pizza.de account %s exists" % email) 
        else:
            account_not_exists_info.append("No account %s on pizza.de" % email)
        
    except Exception, e:
        account_error.append("error: %s" % repr(e))
    
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
