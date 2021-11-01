#!/bin/sh

# Activate environment
if [ -d venv ] && [ -z ${VIRTUAL_ENV+x} ]
then
    source ./venv/bin/activate
fi

python -m cmc_data populate-latest
