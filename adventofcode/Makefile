les## help - Display help about make targets for this Makefile
help:
	@cat Makefile | grep '^## ' --color=never | cut -c4- | sed -e "`printf 's/ - /\t- /;'`" | column -s "`printf '\t'`" -t


## setup - Installs dependencies
setup:
    # cargo install aoc-cli
    ~/venv/bin/pip install -r requirements.txt
