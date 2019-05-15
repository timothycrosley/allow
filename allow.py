#!/usr/bin/env python3
"""A simple script to manage my local DNS whitelist"""
import os
import sys
from pprint import pprint
from subprocess import call

import hug


@hug.cli(output=pprint)
def whitelist(*websites):
    """Mark a website as safe adding it to the whitelist. Must be ran as root or using sudo."""
    whitelisted = set()
    with open('/etc/dnsmasq.conf', 'r') as whitelist:
        for line in whitelist:
            if line.startswith("server=/") and line.endswith("/8.8.8.8\n"):
                whitelisted.add(line.replace("server=/", "", 1).replace("/8.8.8.8\n", "", 1))
    if not websites:
        return whitelisted

    already_whitelisted = whitelisted.intersection(websites)
    if already_whitelisted:
        sys.exit(f"ERROR: Aborting as some of the specified sites are already whitelisted {already_whitelisted}")

    if not os.geteuid() == 0:
        return call(['sudo', 'python3', *sys.argv])

    with open('/etc/dnsmasq.conf', 'a') as whitelist:
        for website in websites:
            whitelist.write(f"server=/{website}/8.8.8.8\n")

    call(('/etc/init.d/dnsmasq', 'restart'))


whitelist.interface.cli()
