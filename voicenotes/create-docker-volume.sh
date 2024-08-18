#!/bin/sh
docker run \
    --mount source=myvol2,target=/app \
    -v /voicenotes/vn_cache:/app/vn_cache \
    voicenote-fetching