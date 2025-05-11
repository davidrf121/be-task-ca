#!/bin/bash
# Update apt and install necessary packages
apt update -y
apt install -y python3-dev libpq-dev libhdf5-dev graphviz

# Download and install POETRY
curl -sSL https://install.python-poetry.org | python3 -
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
