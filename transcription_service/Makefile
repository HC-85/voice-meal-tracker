AUDIO_FOLDER=vn_cache
TRANS_FOLDER=transcriptions

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
    -v /workspaces/voice-meal-tracker/fetching_service/${AUDIO_FOLDER}:/app/${AUDIO_FOLDER} \
    -v /workspaces/voice-meal-tracker/transcription_service/${TRANS_FOLDER}:/app/${TRANS_FOLDER} \
    transcription-app

run-debug:
	@docker run \
	--name transcription-app \
    -p 8000:8000 \
    -v /workspaces/voice-meal-tracker/fetching_service/${AUDIO_FOLDER}:/app/${AUDIO_FOLDER} \
    -v /workspaces/voice-meal-tracker/transcription_service/${TRANS_FOLDER}:/app/${TRANS_FOLDER} \
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
    -v /workspaces/voice-meal-tracker/fetching_service/${AUDIO_FOLDER}:/app/${AUDIO_FOLDER} \
    -v /workspaces/voice-meal-tracker/transcription_service/${TRANS_FOLDER}:/app/${TRANS_FOLDER} \
    -it transcription-interactive


AUDIO_FILE=2024-06-06_01-09_MM4934b92d3bc05bf9724195031b693ad1.ogg
transcribe-audio:
	@ while ! curl --silent -X GET http://127.0.0.1:8000/health | grep "OK" > /dev/null; do\
		sleep 0.1; \
		echo waiting...; \
	done; \
 		curl -X POST http://127.0.0.1:8000/transcribe \
    	-H "Content-Type: application/json" \
    	-d '{"file_path": "/app/${AUDIO_FOLDER}/${AUDIO_FILE}"}'

transcribe-all:
	@ while ! curl --silent -X GET http://127.0.0.1:8000/health | grep "OK" > /dev/null; do\
		sleep 0.1; \
		echo waiting...; \
	done; \
 		curl -X POST http://127.0.0.1:8000/transcribe_all