#syntax=docker/dockerfile:1
ARG PYTHON_VER=3.12
FROM python:${PYTHON_VER}-alpine

RUN mkdir kernel_files output

RUN apk upgrade && \
    apk add --no-cache git

RUN python -m pip install --upgrade pip && \
    pip --no-cache-dir install kaggle