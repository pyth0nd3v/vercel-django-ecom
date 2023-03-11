#!/bin/bash

# Set the Python version
export PYTHON_VERSION=3.10.6

# Set the pip version
export PIP_VERSION=22.0.2

# Create a virtual environment
python${PYTHON_VERSION} -m venv env

# Activate the virtual environment
source env/bin/activate

# Upgrade pip to the specified version
pip install --upgrade pip==${PIP_VERSION}

# Install the packages from requirements.txt
pip install -r requirements.txt
