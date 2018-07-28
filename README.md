# murder

A group of crows is called a "murder". A crow is a bird. Twitter's logo is a bird. Is it a stupid name? Let me know in six months if you remembered it. This script will take an input file containing one name per row, validate them, and try them against the twitter API for availability.

## Getting Started

The first thing you need is an input file. The second thing you need is patience.

### Creating an input file from dictionaries

One way to look for short, memorable names is to generate an input file from dictionaries. For example, you could grab this:

`git clone https://github.com/dwyl/english-words.git`

### Running the script

The script takes no parameters. It expects `input.txt` in the same folder, and will print to STDOUT. If matches are found, they are appended to `output.txt`. If a name is detected to be unavailable, it will be saved to `unavailable.txt`. If this file exists when the script is run, any entries in it will be disregarded before making API calls.

#### Input file vs. What is actually queried

The default configuration is very conservative and only runs valid usernames that have an exact length of 5 characters. For a regular English dictionary, this is still a large amount of words (likely thousands). For your reference, here are some examples of time required to run through an entire list of names:

| Words  | sleep_seconds | Hours required | Days required |
| ------ | ------------- | -------------- | ------------- |
| 10,000 | 10            | 27.8           |               |
|100,000 | 10            |                | 11.6          |

If you accept longer names, the limit is easily changed in the script from `== 5` to, for example `<= 7`.

### Why is it so slow?

If you run queries faster than what the script limits you to, twitter will rate-limit you. Therefore, the script has a pause between every query. If you have less than 200 queries, you could change the timer in the script:

`sleep_seconds = 10`

## License

This project is in the public domain - see the [LICENSE](LICENSE) file for details.
