# syntax=docker/dockerfile:1
ARG PYTHON_VER=3.12
FROM python:${PYTHON_VER}-alpine AS main

WORKDIR /app
RUN mkdir vn_cache
COPY api.py \
     fetching.py \
     requirements.txt \
     /app

RUN apk upgrade && \
    apk add --no-cache git

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ARG _TWILIO_ACCOUNT_SID
ENV TWILIO_ACCOUNT_SID=${_TWILIO_ACCOUNT_SID}

ARG _TWILIO_AUTH_TOKEN
ENV TWILIO_AUTH_TOKEN=${_TWILIO_AUTH_TOKEN}

EXPOSE 8000

FROM main AS app-loop
ENTRYPOINT ["fastapi", "dev", "--host", "0.0.0.0", "--port", "8000", "api.py"]

FROM main AS interactive
ENTRYPOINT ["/bin/sh"]
