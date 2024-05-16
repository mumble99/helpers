import os
import sys
import base64
import hmac
import hashlib
import ipaddress

if len(sys.argv) > 1:
    filename = sys.argv[1]
    if os.path.exists(filename) and os.path.isfile(filename):
        with open(filename) as f:
            file_content = list(filter(lambda l: l, f.read().split("\n")))
    else:
        print('invalid file path')
        sys.exit()
else:
    file_content = list(filter(lambda l: l, sys.stdin.read().split("\n")))


def generate_ip():
    return [str(i) for i in ipaddress.ip_network("10.0.0.0/8").hosts()]


hashes = []
salts = []

for content in file_content:
    if content.startswith("|1|"):
        _, _, salt, host_str = content.split("|")
        host = host_str.split(" ")[0]
        hashes.append(host.encode())
        salts.append(base64.b64decode(salt.encode()))

for ip in generate_ip():
    temp_hashes = []
    for s in salts:
        temp_hashes.append(base64.b64encode(hmac.new(s, ip.encode(), hashlib.sha1).digest()))
    for h in hashes:
        if h in temp_hashes:
            print("found ip %s" % ip)
