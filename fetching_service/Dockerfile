# syntax=docker/dockerfile:1
ARG PYTHON_VER=3.12
FROM python:${PYTHON_VER}-alpine AS base
ENV SERVICE=fetch

WORKDIR /app
RUN mkdir vn_cache
COPY api_${SERVICE}.py \
     app_${SERVICE}.py \
     requirements_${SERVICE}.txt \
     /app

RUN apk upgrade && \
    apk add --no-cache git

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements_${SERVICE}.txt

EXPOSE 8000

FROM base AS app-loop
ENTRYPOINT ["sh", "-c", "fastapi dev --host 0.0.0.0 --port 8000 api_${SERVICE}.py"]

FROM base AS interactive
ENTRYPOINT ["/bin/sh"]
