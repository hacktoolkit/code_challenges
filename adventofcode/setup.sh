#!/bin/bash

usage() {
    echo 'Usage:'
    echo '    ./setup.sh YYYY'
}

SYMLINKS="download.py download.sh template.py utils/"


if [ $# == 1 ]
then
    YEAR=$1

    echo "Creating directory ${YEAR}..."
    mkdir -p ${YEAR}
    cd ${YEAR}

    echo "Creating symlinks..."
    for symlink in ${SYMLINKS}
    do
        ln -fs ../${symlink} .
    done

    echo "Ready to start hacking away for ${YEAR}!"
else
    usage
fi

