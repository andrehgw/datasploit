#!/usr/bin/env python

import base
import vault
import sys
from termcolor import colored

# Control whether the module is enabled or not
ENABLED = True

class style:
    BOLD = '\033[1m'
    END = '\033[0m'

def banner():
    # Write a cool banner here
    print colored(style.BOLD + '\n[+] Checking if Facebook username exists\n' + style.END, 'blue')
    pass


def main(username):
    user_information = []
    facebook_access_token = vault.get_key('facebook_access_token')
    
    if facebook_access_token != None and len(facebook_access_token) > 0:
        user_information.append("TODO: implement facebook query for %s..." % username)
    else: 
        user_information.append("no Facebook access token configured")
    
    return user_information


def output(data, username=""):
    # Use the data variable to print out to console as you like
    for i in data:
        print i


if __name__ == "__main__":
    try:
        username = sys.argv[1]
        banner()
        result = main(username)
        output(result, username)
    except Exception as e:
        print e
        print "Please provide a username as argument"
