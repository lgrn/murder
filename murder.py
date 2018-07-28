#!/usr/bin/env python3

# murder 0.2.2

import time
import requests
import json
import re
import sys

# Your "filename" file should contain one word per row. Don't worry about
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

pretty_amount = "{:,}".format(len(lines))

print("Step 1: Imported {} words from {}.".format(pretty_amount,filename))

# This regex pattern validates usernames.

pattern = re.compile("^[a-zA-Z0-9]+([._]?[a-zA-Z0-9]+)*$")

sys.stdout.flush()

# This function will check if a name is available:

def is_available(username):
    url = ("https://twitter.com/users/username_available"
    "?scribeContext%5Bcomponent%5D=form&scribeContext%5B"
    "element%5D=screen_name&username=" + str(username.lower()) +
    "&value=" + str(username.lower()))
    response = requests.get(url)
    try:
        data = json.loads(response.text)
    except:
        print('[  JSON!  ] Malformed JSON detected when checking: ')
        print(url)
        pass
    
    if data.get("reason") == "available":
        return True
    else:
        return False

# This function deletes any name that we already checked from input.txt.
# It opens the file, reads all lines, and writes back all but one line.
# It feels a lot like making a cake with a hammer and a blow torch,
# but I'm not good with computers.

# def delete_row(r):
    # f = open("input.txt", "r")
    # lines = f.readlines()
    # f.close()
    # f = open("input.txt", "w")
    # for line in lines:
        # if line != r + "\n":
            # f.write(line)

# delete_row hammers IO so it's disabled by default, it was introduced
# in 0.1 and I am ashamed of it on a daily basis.

# write_available below will be used in case of AVAILABLE

def write_available(i):
    f = open("output.txt", "a")
    f.write(i)
    f.close()

def write_unavailable(i):
    f = open("unavailable.txt", "a")
    f.write(i)
    f.close()

failed_tries = 0
ok_tries = 0

# Let's clean up our "lines" array first so it only contains stuff we
# actually want to throw at the API.

clean_lines = []

for i in lines:
    if pattern.match(i) and len(str(i)) == 5:
        clean_lines.append(i)

# NOTE: "Compliant" below is decided by the for loop above.
        
pretty_amount = "{:,}".format(len(clean_lines))
print("Step 2: Cleaned up import to only include compliant words. We now have {} words.".format(pretty_amount))

# NOTE: time.sleep waits because twitter has a rate limit of 200/15min (?), 
# so this will run at most 90 (less than half) in that same period.

sleep_seconds = 8

for i in clean_lines:
    sys.stdout.flush()
    if is_available(i):
        print("[AVAILABLE] '{}'! Saving to output.txt, stalling for next API call.".format(i.lower()))
        ok_tries += 1
        write_available(i + '\n')
        sys.stdout.flush()
        time.sleep(sleep_seconds)
    else:
        print("[  TAKEN  ] '{}'. Too bad. Stalling for next API call.".format(i.lower()))
        failed_tries += 1
        #delete_row(i)
        write_unavailable(i + '\n')
        time.sleep(sleep_seconds)

total_tries = failed_tries + ok_tries

print("Script finished. Twitter was hit with "
      "{} queries. We found {} available names, saved to output.txt".format(total_tries,ok_tries))