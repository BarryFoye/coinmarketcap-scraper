#!/bin/sh

# Activate environment
if [ -d ${WORKDIR}/venv ] && [ -z ${VIRTUAL_ENV+x} ]
then
    source ${WORKDIR}/venv/bin/activate
fi

# Initialise the data model
python -m cmc_data.data_model init-db \
    -D ${DB_DRIVER} \
    -h ${DB_HOST} \
    -p ${DB_PORT} \
    -U ${DB_USER} \
    -W ${DB_PASSWORD}
