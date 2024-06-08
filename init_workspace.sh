#!/bin/bash

if [ -z "$1" ]; then
  echo "Error: No local source directory provided."
  echo "Usage: $0 <local_source_directory>"
  exit 1
fi

scipy_version=$(python3 -c "import scipy; print(scipy.__version__)")

if [ "$scipy_version" == "1.13.1" ]; then
  pip uninstall -y scipy > /dev/null
fi

sudo mkdir -p /workspaces/Nutrition-Logger/audio/voicenotes

scipy_version=$(python3 -c "import scipy; print(scipy.__version__)")

if [ "$scipy_version" == "1.13.1" ]; then
sudo tailscale up --accept-routes --authkey $TAILSCALE_KEY
sudo mkdir -p /workspaces/Nutrition-Logger/audio/voicenotes

sudo mkdir -p /mnt/local
sudo chown codespace:codespace /mnt/local

sudo tailscale up --accept-routes --authkey $TAILSCALE_KEY

export LOCAL_IP_ADDRESS=$(tailscale status | grep -v 'codespaces' | awk '{print $1}')

sshfs $LOCAL_USERNAME@$LOCAL_IP_ADDRESS:/home/$LOCAL_USERNAME/$1 /mnt/local