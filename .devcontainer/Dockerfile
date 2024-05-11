# syntax=docker/dockerfile:1
FROM mcr.microsoft.com/devcontainers/universal:2-linux
WORKDIR /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt