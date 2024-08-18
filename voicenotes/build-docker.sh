#!/bin/sh
docker build \
    --build-arg _TWILIO_ACCOUNT_SID=${TWILIO_ACCOUNT_SID} \
    --build-arg _TWILIO_AUTH_TOKEN=${TWILIO_AUTH_TOKEN} \
    -t voicenote-fetching .