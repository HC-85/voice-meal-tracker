#!/bin/sh
docker run \
    -p 8000:8000 \
    -v /workspaces/voice-meal-tracker/voicenotes/vn_cache:/app/vn_cache \
    voicenote-fetching