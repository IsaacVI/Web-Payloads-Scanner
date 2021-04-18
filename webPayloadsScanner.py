#!/bin/python3

import requests
import argparse
import random
import string

parser = argparse.ArgumentParser(description='Try to use payloads on target website')

parser.add_argument('-u', '--url', dest='url', type=str, required=True, help='target URL')
parser.add_argument('-p', '--payloads', dest='payloads', type=str, required=True, help='file with payloads')
parser.add_argument('-r', '--replace', dest='replace', type=str, required=False, default="{payload}",
                    help='change default replacing string, Default: {payload}')
parser.add_argument('-P', '--post', dest='post', type=str, required=False, help='post data')
parser.add_argument('-d', '--default_payload', dest='default_payload', type=str, required=False,
                    help='add default payload what will be used to compare otherwise will be randomised')
parser.add_argument('-l', '--simple-length', dest='advance_length', action='store_false', default=True, required=False,
                    help='dont calculate differences in payloads lengths to reduce results')
parser.add_argument('-c', '--cookies', dest='cookies', type=str, required=False, help='additional cookies')
parser.add_argument('-H', '--headers', dest='headers', type=str, required=False, help='additional headers')
parser.add_argument('-b', '--byte-difference', dest='byte_difference', type=int, required=False, default=0,
                    help='max difference in size from default response in bytes to not mark as suspicious')
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False, required=False,
                    help='show additional info')

args = parser.parse_args()

cookies = {}
if args.cookies is not None and args.cookies:
    for cookie in args.cookies.replace("  "," ").replace("; ", ";").split(";"):
        c = cookie.split('=', 1)
        cookies[c[0]] = c[1]

headers = {}
if args.headers is not None and args.headers:
    for header in args.headers.replace("  "," ").replace("; ", ";").split(";"):
        h = header.split('=', 1)
        headers[h[0]] = h[1]

replaceString = args.replace

is_post = args.post is not None and args.post
post_data = {}
if is_post:
    for pd in args.post.replace("  ", " ").replace("; ", ";").split(";"):
        p = pd.split('=', 1)
        post_data[p[0]] = p[1]

verbose = args.verbose
advance_length = args.advance_length
url = args.url
byte_difference = args.byte_difference

def get(target_url):
    global cookies
    global headers
    return requests.get(target_url, cookies=cookies, headers=headers, allow_redirects=False)


def post(target_url, data):
    global cookies
    global headers
    return requests.post(target_url, data=data, cookies=cookies, headers=headers, allow_redirects=False)


def execute_payload(target_url: str, payload, data_org):
    global replaceString
    global is_post
    data = data_org.copy()
    target_url = target_url.replace(replaceString, payload)
    if is_post:
        for i in data:
            data[i] = data[i].replace(replaceString, payload)
        return post(target_url, data)
    else:
        return get(target_url)


file = open(args.payloads, mode='r')
payloads = file.read()
file.close()


default_payload = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

if args.default_payload is not None:
    default_payload = args.default_payload

default_result = execute_payload(url, default_payload, post_data)
default_payload_length = len(default_payload)
default_response_code = default_result.status_code
default_response_length = len(default_result.content)
print()
print("--- Web Payload Scanner ---")
print()
print(f"[+] Default payload: {default_payload} returned code: {default_response_code} "
      f"and has length: {default_response_length} will be used to compare results")
print(f"Default link: {default_result.url}")

payloads_list = payloads.splitlines()

print()
print(f"[+] Testing {len(payloads_list)} payloads")
print()

success = 0

for pl in payloads_list:
    result = execute_payload(url, pl, post_data)
    result_length = len(result.content)
    result_code = result.status_code
    if default_response_code != result_code or \
            (abs(result_length - default_response_length) > byte_difference and
             (not advance_length or default_response_length - result_length != default_payload_length - len(pl))):
        success += 1
        print(f"[!] Payload looks suspicious: {pl} "
              f"returned code: {result_code} and has length: {result_length} link: {result.url}")
    elif verbose:
        print(f"[+] Payload: {pl} returned code: {result_code} and has length: {result_length}")

print()
print(f"[+] {success} payloads looks suspicious")
print()
