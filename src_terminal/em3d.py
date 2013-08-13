#!/usr/bin/python

import sys, getopt
import logging
import os
import xml.etree.ElementTree as ET
import EM3Dnalib
import EM3Dreprap

DEFAULT_CONFIG_FILE = ('em3d.xml')


def main(argv):
    # comment
    # sample implementation of arguments:
    # http://www.cyberciti.biz/faq/python-command-line-arguments-argv-example/
    try:
        opts, args = getopt.getopt(argv, "h:c", ["config="])
    except getopt.GetoptError:
        print 'em3d.py -h for help'
        print 'usage: em3d.py -c <filename>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'em3d.py -h for more help'
            sys.exit()
        elif opt == ("-c", "--config"):
            config = arg
            print config

    tree = ET.parse('em3da.xml')
    devices = tree.getroot()

    print len(devices)
    print tree.findtext('./log/log-file')
    print tree.findtext('./pna/ip')
    print tree.findtext('./pna/port')
    print tree.findtext('./pna/calib')
    print tree.findtext('./atmega/port')
    print tree.findtext('./atmega/baud')

if __name__ == '__main__':
    main(sys.argv[1:])
