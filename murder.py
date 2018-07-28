#!/usr/bin/env python3

# murder 0.2.3

import time
import requests
import json
import re
import sys

# Your "filename" file should contain one word per row. Don't worry about
# newlines and whitespace, it will be stripped. Any names containing anything
# but A-Z/a-z, underscores and numbers will be skipped and not queried.

filename = "input.txt"

try:
    with open(filename) as f:
        lines = [line.strip().strip('\n').lower() for line in open(filename)]
        lines = list(set(lines))
except FileNotFoundError:
    print("For this script to work, {} needs to exist in the working directory. Exiting.".format(filename))
    raise SystemExit

unavailable_filename = "unavailable.txt"

try:
    with open(unavailable_filename) as f:
        unavailable_lines = [line.strip().strip('\n') for line in open(unavailable_filename)]     
except FileNotFoundError:
    print("\n{} was not found. That's fine, probably there wasn't a previous run.".format(unavailable_filename))

available_filename = "output.txt"

try:
    with open(available_filename) as f:
        available_lines = [line.strip().strip('\n') for line in open(available_filename)]     
except FileNotFoundError:
    print("\n{} was not found. That's fine, probably there wasn't a previous run.".format(available_filename))


pretty_amount = "{:,}".format(len(lines))

print("\n[>>>>>>>>>] Imported {} words from {}.".format(pretty_amount,filename))

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
        reason = data.get("reason")
    except UnboundLocalError:
        print('[  JSON!  ] Twitter refused to give us a decent response for this request: ')
        print(url)
        print('[  JSON!  ] Assuming its unavailable and attempting to move on.')
        reason = "unavailable"
        pass
    except ValueError:
        print('[  JSON!  ] UH-OH! You\'re probably being rate limited :( ) ')
        print('[  JSON!  ] You should stop for now and/or adjust your sleep_timer ) ')
        print('[  JSON!  ] ValueError for this request: ')
        print(url)
        raise SystemExit

    if reason == "available":
        return True
    else:
        return False

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
print("[>>>>>>>>>] Cleaned up import to only include compliant words. We now have {} words.".format(pretty_amount) + "\n")

# Clean the array further by removing already checked names (failed and succeeded).

try:
    for i in unavailable_lines:
        if i in clean_lines:
            clean_lines.remove(i)
            print("[ CLEANUP ] '{}' will not be checked, we already know it's taken.".format(i.lower()))
    for i in available_lines:
        if i in clean_lines:
            clean_lines.remove(i)
            print("[ CLEANUP ] '{}' will not be checked, we already know it's available.".format(i.lower()))
except NameError:
    # If there wasn't a previous run, this won't exist. That's fine.
    pass

try:
    if unavailable_lines:
        pretty_amount = "{:,}".format(len(clean_lines))
        print("[>>>>>>>>>] After cross-checking unavailable.txt we are down to {} words.".format(pretty_amount) + "\n")
except NameError:
    pass

# NOTE: time.sleep waits because twitter has a rate limit of 150/15min (?) <- bad guess

print("[>>>>>>>>>] Making API calls now." + "\n")

sleep_seconds = 10

for i in clean_lines:
    sys.stdout.flush()
    if is_available(i):
        print("[AVAILABLE] '{}'! Saving to output.txt, stalling for next API call.".format(i.lower()))
        ok_tries += 1
        write_available(i.lower() + '\n')
        sys.stdout.flush()
        time.sleep(sleep_seconds)
    else:
        print("[  TAKEN  ] '{}'. Too bad. Stalling for next API call.".format(i.lower()))
        failed_tries += 1
        #delete_row(i)
        write_unavailable(i.lower() + '\n')
        time.sleep(sleep_seconds)

total_tries = failed_tries + ok_tries

print("Script finished. Twitter was hit with "
      "{} queries. We found {} available names, saved to output.txt".format(total_tries,ok_tries))