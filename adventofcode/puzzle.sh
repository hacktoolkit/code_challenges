#!/bin/bash

YEAR=`basename $(pwd)`

~/venv/bin/python utils/aoc_client.py --year $YEAR --day $1 --type puzzle --save
