#!/usr/bin/env python

# This file enables editable installs (pip install -e .[dev])

# ##########################################################
#  See this issue: https://github.com/pypa/pip/issues/7953
import site
import sys
site.ENABLE_USER_SITE = "--user" in sys.argv[1:]
# ##########################################################

import setuptools

if __name__ == "__main__":
    setuptools.setup()
