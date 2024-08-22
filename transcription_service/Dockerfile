ARG SERVICE=transcribe
FROM lscr.io/linuxserver/faster-whisper:latest AS base

WORKDIR /app
RUN mkdir vn_cache

COPY api_transcribe.py \
     app_transcribe.py \
     requirements_transcribe.txt \
     /app

RUN pip install --no-cache-dir --upgrade pip && \
pip install --no-cache-dir -r requirements_transcribe.txt

EXPOSE 8000

FROM base AS app-loop
ENTRYPOINT ["sh", "-c", "fastapi dev --host 0.0.0.0 --port 8000 api_${SERVICE}.py"]

FROM base AS interactive
ENTRYPOINT ["/bin/sh"]
