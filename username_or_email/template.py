#!/usr/bin/env python
# encoding: utf-8

import base
import vault
import sys

from termcolor import colored
from base import style

# Control whether the module is enabled or not
ENABLED = True


def banner():
    # Write a cool banner here
    pass


def main(accountname):
    # Use the accountname variable to do some stuff and return the data
    print accountname
    return []


def output(data, accountname=""):
    # Use the data variable to print out to console as you like
    for i in data:
        print i


if __name__ == "__main__":
    try:
        accountname = sys.argv[1]
        banner()
        result = main(accountname)
        output(result, accountname)
    except Exception as e:
        print e
        print "Please provide a accountname as argument"
