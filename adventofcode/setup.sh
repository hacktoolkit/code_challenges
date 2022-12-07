#!/bin/bash

usage() {
    echo 'Usage:'
    echo '    ./setup.sh YYYY'
}

SYMLINKS="download.sh puzzle.sh template.py utils/"


if [ $# == 1 ]
then
    YEAR=$1

    echo "Creating directory ${YEAR}..."
    mkdir -p ${YEAR}
    cd ${YEAR}

    echo "Creating symlinks..."
    for symlink in ${SYMLINKS}
    do
        if [ ${symlink} == 'template.py' ]
        then
            SYMLINK_DEST='00.py'
        else
            SYMLINK_DEST='.'
        fi
        ln -fs ../${symlink} ${SYMLINK_DEST}
    done

    echo "Ready to start hacking away for ${YEAR}!"
else
    usage
fi
