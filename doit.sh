#!/bin/bash
set -x
set -e
rm -rf .python/
/usr/local/bin/python2.6 create-plone-bootstrap.py

# I've built a virgin python with no extra packages to test in the case
# where there's no setuptools or virtualenv installed.
$PWD/tools/bin/python plone-try-bootstrap.py 
