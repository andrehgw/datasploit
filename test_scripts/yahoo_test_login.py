#!/usr/local/bin/python2.7
# encoding: utf-8
'''
test_scripts.yahoo_test_login -- connect Yahoo to test if user
exists with email

test_scripts.yahoo_test_login is a test script

It defines classes_and_methods

@author:     Andre Fiedler

@copyright:  2018 GCHN. All rights reserved.

@license:    GPL

@contact:    andre@balticnetwork.de
@deffield    updated: Updated

@see:     https://stackoverflow.com/questions/11974478/how-to-login-to-yahoo-programatically-from-an-ubuntu-server
          https://stackoverflow.com/questions/28038950/how-to-get-the-scrapy-form-submission-working
          https://www.analyticsvidhya.com/blog/2017/07/web-scraping-in-python-using-scrapy/
'''

import sys
import os

import requests
import json

import scrapy

import time

#import vault

#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys

import datetime

from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
 


from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter


# import dmoz spider class
from DmozSpider import DmozSpider

# scrapy api
from scrapy import signals, log
from twisted.internet import reactor
from scrapy.crawler import Crawler, CrawlerProcess
from scrapy.settings import Settings
from time import sleep


__all__ = []
__version__ = 0.1
__date__ = '2018-05-18'
__updated__ = '2018-05-18'

DEBUG = 0
TESTRUN = 0
PROFILE = 0


yahoo_url = "https://login.yahoo.com/"

   

class wait_for_page_load(object):

    def __init__(self, browser):
        self.browser = browser

    def __enter__(self):
        self.old_page = self.browser.find_element_by_tag_name('html')

    def page_has_loaded(self):
        new_page = self.browser.find_element_by_tag_name('html')
        return new_page.id != self.old_page.id

    def __exit__(self, *_):
        self.wait_for(self.page_has_loaded)   
        
    def wait_for(self,condition_function):
        start_time = time.time()
        while time.time() < start_time + 3:
            if condition_function():
                return True
            else:
                time.sleep(0.1)
        raise Exception(
            'Timeout waiting for {}'.format(condition_function.__name__)
        )


class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s


  Created by Andre Fiedler on %s.
  Copyright 2018 GCHN. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        
        # Process arguments
        args = parser.parse_args()

        verbose = args.verbose
        
        if verbose > 0:
            print("Verbose mode on")
                
        
        print ("connect yahoo: %s\n" % yahoo_url)
        
        """        
        s = requests.Session()
        s.headers.update({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
        s.headers.update({'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
        s.headers.update({'Accept-Encoding':'gzip, deflate, br'})
        r=s.get(yahoo_url)
        
        cookies = s.cookies.get_dict()
            
        print cookies
        
        s.headers.update({'Accept':'*/*'})
        s.headers.update({'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'})
        s.headers.update({'X-Requested-With':'XMLHttpRequest'})
        
                
        payload = {'acrumb':'MghWr0VD',
                   'crumb':'QrlXw.NGMIX',
                   'passwd':'',
                   'sessionIndex':'QQ--',
                   'signin':'Weiter',
                   'username':'john@yahoo.com'}
        
        
        r = s.post(yahoo_url, data=payload)
        
        print json.loads(r.text)
        """
 
 
        """       
        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })
        
        process.crawl(DmozSpider())
        process.start()
        """    
        
        """
        opts = Options()
        opts.set_headless()
        assert opts.headless  # operating in headless mode
        browser = Firefox(options=opts)
        browser.get('https://duckduckgo.com')
        """
        
        
        
        # The place we will direct our WebDriver to
        url = "https://login.yahoo.com"
        
        testuser = "john@yahoo.com"
        
        print "testing for %s" % testuser
        
        # Creating the WebDriver object using the ChromeDriver
        driver = webdriver.Firefox()
        driver.set_page_load_timeout(30)
        
        wait = WebDriverWait(driver, 30)
        
        driver.get(url)
        
               
        with wait_for_page_load(driver):
            driver.find_element_by_id("login-username").send_keys(testuser)
            driver.find_element_by_id("login-signin").click()
            #print "Button is clicked at time: " + str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
            #wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
            #print "Ajax request is completed at time: " + str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        
        #source = driver.page_source
        
        try:
            errortest = driver.find_element_by_id("username-error")
            if errortest != None:
                print "user doesn't exist"
        except NoSuchElementException:
            print "user exist"
        #print source
        
        driver.close()
        
        return 0
    
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    
    except Exception, e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
        sys.argv.append("-v")
    
    sys.exit(main())