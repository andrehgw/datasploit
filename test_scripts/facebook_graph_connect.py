#!/usr/local/bin/python2.7
# encoding: utf-8
'''
test_scripts.facebook_graph_connect -- Connect Facebook Graph API

test_scripts.facebook_graph_connect is a test script

It defines classes_and_methods

@author:     Andre Fiedler

@copyright:  2018 GCHN. All rights reserved.

@license:    GPL

@contact:    andre@balticnetwork.de
@deffield    updated: Updated
'''

import sys
import os

import requests
import json


from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2018-05-18'
__updated__ = '2018-05-18'

DEBUG = 0
TESTRUN = 0
PROFILE = 0


fb_api_url = "https://graph.facebook.com"


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
                
                
        '''
        main routine - test Facebook Graph API
        '''
            
        token_url = "%s/oauth/access_token?grant_type=facebook_exchange_token&client_id=%s&client_secret=%s&facebook_exchange_token=%s" % (fb_api_url,facebook_client_id,facebook_client_secret,facebook_exchange_token)                
        req = requests.get(token_url)
        data = json.loads(req.text)
        if 'access_token' in data:
            fb_access_token=data['access_token']
            print ("access token: %s\n" % fb_access_token)
            
            # test own profile metadata
            graph_url = "%s/me?metadata=1&access_token=%s" % (fb_api_url,fb_access_token) 
            req = requests.get(graph_url)
            data = json.loads(req.text)
            
            # search for user
            username = "maik.kunze"
            graph_url = "%s/%s?access_token=%s" % (fb_api_url,username,fb_access_token)
            req = requests.get(graph_url)
            data = json.loads(req.text)
            
            
            
        else:
            raise(Exception("didn't get no token from Facebook ;-("))
            
        
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