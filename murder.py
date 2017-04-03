#!/usr/bin/env python3

# murder 0.1

import time
import requests
import json
import re
import sys

# Your "filename" file should contain one name per row. Don't worry about
# newlines and whitespace, it will be stripped. Any names containing anything
# but A-Z/a-z, underscores and numbers will be skipped and not queried.
# 
# Example: 

# gagarin <- query
# uber    <- query
# über    <- skip

filename = "input.txt"

with open(filename) as f:
    lines = [line.strip().strip('\n') for line in open(filename)]

print("Done importing: {}. Running twitter API calls now.".format(filename))

# This regex pattern validates usernames.

pattern = re.compile("^[a-zA-Z0-9]+([._]?[a-zA-Z0-9]+)*$")

# Print feedback to stdout

sys.stdout.flush()

# This function will check if a name is available, then wait 10 seconds.
# It waits because twitter has a rate limit of 200/15min (?), so this will
# run at most 90 (less than half) in that same period.

def is_available(username):
    url = ("https://twitter.com/users/username_available"
    "?scribeContext%5Bcomponent%5D=form&scribeContext%5B"
    "element%5D=screen_name&username=" + username.lower() +
    "&value=" + username.lower())
    response = requests.get(url)
    data = json.loads(response.text)
    time.sleep(10)
    if data.get("reason") == "available":
        return True
    else:
        return False

# This function deletes any name that we already checked from input.txt.
# It opens the file, reads all lines, and writes back all but one line.
# It feels a lot like making a cake with a hammer and a blow torch,
# but I'm not good with computers.

def delete_row(r):
    f = open("input.txt", "r")
    lines = f.readlines()
    f.close()
    f = open("input.txt", "w")
    for line in lines:
        if line != r + "\n":
            f.write(line)

failed_tries = 0
ok_tries = 0

for i in lines:
    if pattern.match(i):
        sys.stdout.flush()
        if is_available(i):
            print("[AVAILABLE] '{}'".format(i.lower()))
            ok_tries += 1
            sys.stdout.flush()
        else:
            print("[  TAKEN  ] '{}'. Deleting.".format(i.lower()))
            failed_tries += 1
            delete_row(i)
    else:
        sys.stdout.flush()
        print(    "[ IGNORED ] '{}'. Deleting.".format(i.lower()))
        delete_row(i)

total_tries = failed_tries + ok_tries

print("Script finished. Twitter was hit with {} queries.".format(total_tries))
print("We found {} available names.".format(ok_tries))
