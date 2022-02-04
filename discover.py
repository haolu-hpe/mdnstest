#!/usr/bin/env python3

""" Discoring mdns services in your network """

import logging
import sys

from zeroconf import ZeroconfServiceTypes


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) > 1:
        assert sys.argv[1:] == ['--debug']
        logging.getLogger('zeroconf').setLevel(logging.DEBUG)

    title = "Here is the list of mdns services in your local network"
    line = "*******************************************************"
    services = ZeroconfServiceTypes.find()
    print(title)
    print(line)
    print('\n'.join(services))
