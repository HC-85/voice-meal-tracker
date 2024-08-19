all: build run fetch

build:
	@docker build \
    --build-arg _TWILIO_ACCOUNT_SID=${TWILIO_ACCOUNT_SID} \
    --build-arg _TWILIO_AUTH_TOKEN=${TWILIO_AUTH_TOKEN} \
    -t voicenote-fetching .

run:
	@docker run \
	--name vn-fetcher \
	--detach \
    -p 8000:8000 \
    -v /workspaces/voice-meal-tracker/voicenotes/vn_cache:/app/vn_cache \
    voicenote-fetching

fetch: 
	@ while ! curl --silent -X GET http://127.0.0.1:8000/health | grep "OK" > /dev/null; do\
		sleep 0.1; \
	done; \
	curl -X POST http://127.0.0.1:8000/fetch > /dev/null

clear-all: clear-vn clear-docker

clear-vn:
	@curl -X DELETE http://127.0.0.1:8000/clear-cache > /dev/null

clear-docker: clear-containers clear-images

clear-images:
	@if [ -n "$(shell docker images -q)" ]; then \
		docker rmi $(shell docker images -q); \
		docker image prune -f; \
	else \
		echo $ "Already clean."; \
	fi

clear-containers:
	@if [ -n "$(shell docker ps -q)" ]; then \
		docker stop $(shell docker ps -q); \
		docker container prune -f; \
	else \
		echo $ "Already clean."; \
	fi

healthcheck:
	@curl -X GET http://127.0.0.1:8000/health
