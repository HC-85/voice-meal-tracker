#!/bin/bash

if [ -z "$1" ]; then
  echo "Error: No local source directory provided."
  echo "Usage: $0 <local_source_directory>"
  exit 1
fi

sudo mkdir -p /mnt/local
sudo chown codespace:codespace /mnt/local

sudo tailscale up --accept-routes --authkey $TAILSCALE_KEY

export LOCAL_IP_ADDRESS=$(tailscale status | grep -v 'codespaces' | awk '{print $1}')

sshfs $LOCAL_USERNAME@$LOCAL_IP_ADDRESS:/home/$LOCAL_USERNAME/$1 /mnt/local