#TODO: FIX clear-containers

CACHE_DIR=/fetching/vn_cache


app: build-app run-app fetch

build-app:
	@docker build \
	--target app-loop \
    --build-arg _TWILIO_ACCOUNT_SID=${TWILIO_ACCOUNT_SID} \
    --build-arg _TWILIO_AUTH_TOKEN=${TWILIO_AUTH_TOKEN} \
    -t vn-fetch-app .

run-app:
	@docker run \
	--name vn-fetch-app \
	--detach \
    -p 8000:8000 \
    -v /workspaces/voice-meal-tracker${CACHE_DIR}:/app/vn_cache \
    vn-fetch-app

fetch: 
	@ while ! curl --silent -X GET http://127.0.0.1:8000/health | grep "OK" > /dev/null; do\
		sleep 0.1; \
	done; \
	curl -X POST http://127.0.0.1:8000/fetch > /dev/null

interactive: build-interactive run-interactive

build-interactive:
	@docker build \
	--target interactive \
    --build-arg _TWILIO_ACCOUNT_SID=${TWILIO_ACCOUNT_SID} \
    --build-arg _TWILIO_AUTH_TOKEN=${TWILIO_AUTH_TOKEN} \
    -t vn-fetch-interactive .

run-interactive:
	@docker run \
	--name vn-fetch-interactive \
    -p 8000:8000 \
    -v /workspaces/voice-meal-tracker${CACHE_DIR}:/app/vn_cache \
    -it vn-fetch-interactive


clear-all: clear-vn clear-docker

clear-vn:
	@curl -X DELETE http://127.0.0.1:8000/clear-cache > /dev/null

clear-docker: clear-containers clear-images

clear-images:
	@if [ -n "$(shell docker images -q)" ]; then \
#		docker rmi $(shell docker images -q); \
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


