#!/usr/bin/env python3

""" Example of browsing for a service.

The default is HTTP and HAP; use --find to search for all available services in the network
"""

import argparse
import logging
from time import sleep
from typing import cast

from zeroconf import IPVersion, ServiceBrowser, ServiceStateChange, Zeroconf, ZeroconfServiceTypes


def on_service_state_change(
    zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange
) -> None:
    print(f"Service {name} of type {service_type} state changed: {state_change}")

    if state_change is ServiceStateChange.Added:
        info = zeroconf.get_service_info(service_type, name)
        print("Info from zeroconf.get_service_info: %r" % (info))

        if info:
            addresses = ["%s:%d" % (addr, cast(int, info.port)) for addr in info.parsed_scoped_addresses()]
            print("  Addresses: %s" % ", ".join(addresses))
            print("  Weight: %d, priority: %d" % (info.weight, info.priority))
            print(f"  Server: {info.server}")
            if info.properties:
                print("  Properties are:")
                for key, value in info.properties.items():
                    print(f"    {key}: {value}")
            else:
                print("  No properties")
        else:
            print("  No info")
        print('\n')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--find', action='store_true', help='Browse all available services')
    parser.add_argument('--airplay', action='store_true', help='Searching for airplay services')
    parser.add_argument('--airprint', action='store_true', help='Searching for airprint services')
    parser.add_argument('--printer', action='store_true', help='Searching for printer services')
    parser.add_argument('--homekit', action='store_true', help='Searching for printer services')
    parser.add_argument('--ipps', action='store_true', help='Searching for printer services')


    version_group = parser.add_mutually_exclusive_group()
    version_group.add_argument('--v6', action='store_true')
    version_group.add_argument('--v6-only', action='store_true')
    args = parser.parse_args()

    if args.debug:
        logging.getLogger('zeroconf').setLevel(logging.DEBUG)
    if args.v6:
        ip_version = IPVersion.All
    elif args.v6_only:
        ip_version = IPVersion.V6Only
    else:
        ip_version = IPVersion.V4Only

    zeroconf = Zeroconf(ip_version=ip_version)

    #services = ["_http._tcp.local.", "_hap._tcp.local."]

    if args.find:
        services = list(ZeroconfServiceTypes.find(zc=zeroconf))
    elif args.airplay:
        services = ["_airplay._tcp.local."]
    elif args.airprint:
        services = ["_airprint._tcp.local."]
    elif args.printer:
        services = ["_printer._tcp.local."]
    elif args.homekit:
        services = ["_homekit._tcp.local."]
    elif args.ipps:
        services = ["_ipps._tcp.local."]

    print("\nBrowsing %s service(s), press Ctrl-C to exit...\n" % services)

    browser = ServiceBrowser(zeroconf, services, handlers=[on_service_state_change])

    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        zeroconf.close()
