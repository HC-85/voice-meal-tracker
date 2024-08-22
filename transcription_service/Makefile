CACHE_DIR=/fetching_service/vn_cache

app: build-app run-app fetch

build-app:
	@docker build \
	--target app-loop \
    -t transcription-app .

run-app:
	@docker run \
	--name transcription-app \
	--detach \
    -p 8000:8000 \
    -v /workspaces/voice-meal-tracker${CACHE_DIR}:/app/vn_cache \
    transcription-app

interactive: build-interactive run-interactive

build-interactive:
	@docker build \
	--target interactive \
    -t transcription-interactive .

run-interactive:
	@docker run \
	--name transcription-interactive \
    -p 8000:8000 \
    -v /workspaces/voice-meal-tracker${CACHE_DIR}:/app/vn_cache \
    -it transcription-interactive