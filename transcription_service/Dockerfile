FROM lscr.io/linuxserver/faster-whisper:latest AS base
ENV SERVICE=transcribe

WORKDIR /app
RUN mkdir vn_cache transcriptions

COPY requirements_${SERVICE}.txt \
     /app

RUN pip install --no-cache-dir --upgrade pip && \
pip install --no-cache-dir -r requirements_${SERVICE}.txt

COPY api_${SERVICE}.py \
     app_${SERVICE}.py \
     /app

EXPOSE 8000

FROM base AS app-loop
ENTRYPOINT ["sh", "-c", "fastapi dev --host 0.0.0.0 --port 8000 api_${SERVICE}.py"]

FROM base AS interactive
ENTRYPOINT ["/bin/sh"]
