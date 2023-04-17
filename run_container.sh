#!/bin/bash
# Run the flask app
docker run \
    -d \
    -p 5000:5000 \
    --name zscaller_gui \
    zscaller