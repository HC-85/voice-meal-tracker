# syntax=docker/dockerfile:1

FROM mcr.microsoft.com/devcontainers/universal:2-linux
# ONLY IMAGE I'VE FOUND THAT WORKS WITH TAILSCALE ???
#FROM huggingface/transformers-torch-light
WORKDIR /app

RUN apt-get update && \
    apt-get install -y openssh-client sshfs

COPY requirements.txt /app
RUN pip uninstall -y scipy
RUN pip install --no-cache-dir -r /app/requirements.txt