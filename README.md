# murder

A group of crows is called a "murder". A crow is a bird. Twitter's logo is a bird. Is it a stupid name? Let me know in six months if you remembered it. This script will take an input file containing one name per row, and try all names against the twitter API for availability.

## Getting Started

The first thing you need is an input file. The second thing you need is patience.

### Creating an input file from dictionaries

One way to look for short, memorable names is to generate an input file from dictionaries. For example, you could grab this:

`git clone https://github.com/dwyl/english-words.git`

The shortest allowed name on twitter is five characters, so you could do this to fetch only those words into a new file:

`grep -e "^.....$" words.txt > input.txt`

You now have an input file with a bunch of five letter English words, time to run them against the twitter api

### Running the script

The script takes no parameters. It expects input.txt in the same folder, and will print to STDOUT. If you want to save the result (you probably do), run something like this:

`./murder.py | tee output.txt`

The script will give you feedback after each try. This may seem annoying, but it's a good way to see that the script is still working.

When the script is done, an easy way to show all available names is to do the following:

`grep AVAILABLE output.txt`

**Do not access any of the text files while the script is running**. The script will remove invalid names from your `input.txt` after every query, so that if it crashes you won't have to re-run names that are taken, only re-validate probably available ones, which should be few. The `output.txt` file will obviously be handled by `tee` and it will stop writing to the file if it detects someone tampering with it.

### Why is it so slow?

If you run queries faster than this, twitter will rate-limit you. Therefore, the script has a pause between every query. Probably you prefer for all your queries to go through and not crash half way before speed. That being said, if you have less than 200 queries, you could comment out the timer:

`# time.sleep(10)`

## License

This project is in the public domain - see the [LICENSE](LICENSE) file for details.
