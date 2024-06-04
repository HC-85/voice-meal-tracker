# syntax=docker/dockerfile:1

#FROM ubuntu:focal
#RUN apt update
#RUN apt install -y moby-cli moby-engine 
#RUN apt install git-lfs cmake build-essential cppcheck
#RUN apt install valgrind lldb llvm gdb clang python3-dev vim vim-doc xtail software-properties-common
#RUN apt install libsecret-1-dev libnss3 libnspr4 libatk-bridge2.0-0 libatk1.0-0 libx11-6 libpangocairo-1.0-0
#RUN apt install libx11-xcb1 libcups2 libxcomposite1 libxdamage1 libxfixes3 libpango-1.0-0 libgbm1 libgtk-3-0
#RUN apt install openssh-server lxc pigz iptables tar g++ gcc libc6-dev make pkg-config sed python3-minimal

#RUN pip install --no-cache-dir numpy pandas scipy matplotlib scikit-learn torch requests \
#    jupyterlab_git certifi setuptools wheel

#RUN pipx install pylint flake8 autopep8 black yapf mypy pydocstyle pycodestyle bandit virtualenv pipx
    
FROM mcr.microsoft.com/devcontainers/universal:2-linux
# ONLY IMAGE I'VE FOUND THAT WORKS WITH TAILSCALE ???
#FROM huggingface/transformers-torch-light
WORKDIR /app


RUN apt-get update 
RUN apt-get install openssh-client
RUN apt-get install -y sshfs

COPY requirements.txt /app
RUN pip uninstall -y scipy
RUN pip install --no-cache-dir -r /app/requirements.txt