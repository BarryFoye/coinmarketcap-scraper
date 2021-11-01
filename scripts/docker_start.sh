#!/bin/sh

# Set up environment variables
ENV_VARS="$(dirname $(dirname ${0}))/src/cmc_data/data_model/.env"
export $(cat ${ENV_VARS} | xargs)
export DB_STORAGE=/var/opt/coinmarketcap

# Create the folder where the database is to be stored, if it does not exist
if [ ! -d ${DB_STORAGE} ]
then
    sudo mkdir -p -m 666 ${DB_STORAGE}
    sudo chown ${USER}:staff ${DB_STORAGE}
fi

# Kick in docker compose
docker-compose up --build
