CACHE_DIR=/fetching_service/vn_cache

app: build-app run-app

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

run-debug:
	@docker run \
	--name transcription-app \
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

transcribe:
	@ while ! curl --silent -X GET http://127.0.0.1:8000/health | grep "OK" > /dev/null; do\
		sleep 0.1; \
		echo waiting...; \
	done; \
 		curl -X POST http://127.0.0.1:8000/transcribe \
    	-H "Content-Type: application/json" \
    	-d '{"file_path": "/app/vn_cache/2024-06-06_01-09_MM4934b92d3bc05bf9724195031b693ad1.ogg"}'