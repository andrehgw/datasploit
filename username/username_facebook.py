#!/usr/bin/env python
# encoding: utf-8

"""
Query Facebook graph search API for user. 

    https://graph.facebook.com/maik.kunze?access_token=<ACCESS_TOKEN>
    
    --> get <ACCESS_TOKEN> from: https://developers.facebook.com/tools/accesstoken/

Searching for user string with the graph API isn't possible, 
but there's a trick with the error message:

response user exists:
---------------------
    {
       "error": {
          "message": "(#803) Cannot query users by their username (<username>)",
          "type": "OAuthException",
          "code": 803,
          "fbtrace_id": "ChAg6PPZ+RN"
       }
    }

response if user doesn't exist:
-------------------------------
    {
      "error": {
        "message": "(#803) Some of the aliases you requested do not exist: maik.kunzeddddd",
        "type": "OAuthException",
        "code": 803,
        "fbtrace_id": "FKQiim56y8K"
      }
    }

So, with parsing the error message we can suspect the user exist.

"""

__author__ = "Andre Fiedler <andre@balticnetwork.de>"
__copyright__ = "Copyright"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Andre Fiedler"
__email__ = "andre@balticnetwork.de"
__status__ = "Production"


import base
import vault
import sys

import requests
import json

from base import style

from termcolor import colored

# Control whether the module is enabled or not
ENABLED = True


facebook_access_token=vault.get_key('facebook_access_token')

fb_api_url = "https://graph.facebook.com"

def banner():
    # Write a cool banner here
    print colored(style.BOLD + '\n[+] Checking Facebook\n' + style.END, 'blue')
    pass


def main(username):
    userstats = {}
    
    user_information = []
    user_error = []
    
    facebook_access_token = vault.get_key('facebook_access_token')
    
    if facebook_access_token != None and len(facebook_access_token) > 0:
        try:
            graph_url = '%s/%s?access_token=%s' % (fb_api_url,username,facebook_access_token)
            req = requests.get(graph_url)
            data = json.loads(req.text)
            
            if 'error' in data and len(data['error']) > 0:
                errordict = data['error']
                if 'message' in errordict and len(errordict['message']) > 0: 
                    errormessage = errordict['message']
                    # user exists ;-)
                    if errormessage.find('query users by their username') != -1:
                        user_information.append("user alias '%s' exists on Facebook" % username)
                    else: 
                        user_error.append("'%s' not found on Facebook" % username)
                else:
                    user_error.append("no tag 'message'")     
            else:
                user_error.append("no tag 'error'")
                           
        except Exception, e:
            user_error.append("Error: %s" % repr(e) )
        
    else: 
        user_error.append("no Facebook access token configured")
    
    userstats['user_information'] = user_information
    userstats['user_error'] = user_error
    
    return userstats


def output(data, username=""):
    # output all errors
    if 'user_error' in data and len(data['user_error']) > 0:
        for cerror in data['user_error']:
            print colored(style.BOLD + "[!] Error: " + cerror + style.END, 'red')
            
    # output all user information
    if 'user_information' in data and len(data['user_information']) > 0:
        for cinfo in data['user_information']:
            print colored(style.BOLD + cinfo + style.END, 'green')
            
    


if __name__ == "__main__":
    try:
        username = sys.argv[1]
        banner()
        result = main(username)
        output(result, username)
    except Exception as e:
        print e
        print "Please provide a username as argument"
