#!/bin/bash

# Activate environment
if [ -d venv ]
then
    source ./venv/bin/activate
fi

# Initialise the data model
python -m cmc_data.data_model init-db \
    -D ${DB_DRIVER} \
    -h ${DB_HOST} \
    -p ${DB_PORT} \
    -U ${DB_USER} \
    -W ${DB_PASSWORD}
