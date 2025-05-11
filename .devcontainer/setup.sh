#!/bin/bash
# Update apt and install necessary packages
apt update -y
apt install -y python3-dev libpq-dev libhdf5-dev graphviz

# Download and install POETRY
curl -sSL https://install.python-poetry.org | python3 -

echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

# Install python3.11
# apt install -y software-properties-common
# add-apt-repository ppa:deadsnakes/ppa -y
# apt update
# apt install -y python3.11 python3.11-venv python3.11-dev
