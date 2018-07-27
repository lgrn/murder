# murder

A group of crows is called a "murder". A crow is a bird. Twitter's logo is a bird. Is it a stupid name? Let me know in six months if you remembered it. This script will take an input file containing one name per row, and try all names against the twitter API for availability.

## Getting Started

The first thing you need is an input file. The second thing you need is patience.

### Creating an input file from dictionaries

One way to look for short, memorable names is to generate an input file from dictionaries. For example, you could grab this:

`git clone https://github.com/dwyl/english-words.git`

### Running the script

The script takes no parameters. It expects `input.txt` in the same folder, and will print to STDOUT. If matches are found, they are appended to `output.txt`.

### Example usage

```
> python .\murder.py
Step 1: Imported 180,165 words from input.txt.
Step 2: Cleaned up import to only include compliant words. We now have 9,083 words.
[  TAKEN  ] 'abaft'. Too bad. Stalling for next API call.
[  TAKEN  ] 'abaka'. Too bad. Stalling for next API call.
[  TAKEN  ] 'abama'. Too bad. Stalling for next API call.
[  TAKEN  ] 'abamp'. Too bad. Stalling for next API call.
[  TAKEN  ] 'abana'. Too bad. Stalling for next API call.
(...)
```

This is really as fun as it gets.

### Why is it so slow?

If you run queries faster than what the script limits you to, twitter will rate-limit you. Therefore, the script has a pause between every query. If you have less than 200 queries, you could change the timer in the script:

`sleep_seconds = 8`

## License

This project is in the public domain - see the [LICENSE](LICENSE) file for details.
