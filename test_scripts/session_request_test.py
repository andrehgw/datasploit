#!/usr/local/bin/python2.7
# encoding: utf-8

'''
Created on 2018-06-01

@author: Andre Fiedler <andre@balticnetwork.de>
'''


import sys

import requests
import json


        
        
def main():
    s = requests.Session()
    s.headers.update({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
    s.headers.update({'Accept':'application/vnd.deliveryhero.v2.12+json'})
    s.headers.update({'Accept-Encoding':'gzip, deflate, br'})
    s.headers.update({'content-type':'text/plain;charset=UTF-8'})
    s.headers.update({'Authentication':'LH api-key=BqFXeTedMu1LQazCYZznkzyL5CFffcWIDW7GEpmCFVAPLi1dA4cdt76BnXkyEuqWAbCf8ZWtADOzaz5851LQj1dlppQVZSxPPAe0cA0g7Tn2GoXWTdfStKk5yrKrrB0J'})
    
    
    payload = {'email':'maik.kunze1@freenet.de','op':'reset'}
    
    r = s.put('https://pizza.de/dowant-api/authorization/', data=json.dumps(payload))
    
    pass
    
    
    
if __name__ == "__main__":
        
    sys.exit(main())