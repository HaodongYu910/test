#!/usr/bin/python
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json


def main():
    print(json.dumps(dict(changed=False, failed=True, msg='this collection should be masked by testcoll in the user content root')))


if __name__ == '__main__':
    main()
