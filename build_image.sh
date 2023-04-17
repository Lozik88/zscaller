#!/bin/bash
# List of environment variable names to check
# These MUST be set prior to build.
ENV_VARS=("ZSCALER_USR" "ZSCALER_PW" "ZSCALER_API_KEY")

# Loop through each variable name
for VAR_NAME in "${ENV_VARS[@]}"
do
  # Check if the variable is set
  if [ -z "${!VAR_NAME}" ]
  then
    # Print an error message and exit with a non-zero status
    echo "Error: Environment variable '$VAR_NAME' is not set."
    exit 1
  fi
done

docker build \
    --pull \
    --rm \
    --build-arg ZSCALER_USR=$ZSCALER_USR \
    --build-arg ZSCALER_API_KEY=$ZSCALER_API_KEY \
    --build-arg ZSCALER_PW=$ZSCALER_PW \
    -f "Dockerfile" \
    -t zscaller:latest \
    "." 
