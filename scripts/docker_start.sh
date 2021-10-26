#!/bin/bash

# Set up environment variables
ENV_VARS="$(dirname $(dirname ${0}))/src/cmc_data/data_model/.env"
export $(cat ${ENV_VARS} | xargs)

# Kick in docker compose
docker compose up
