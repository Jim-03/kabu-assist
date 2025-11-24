#!/usr/bin/env bash

# Setup the backend
cd chatbot-core

echo "Setting up the chatbot's backend"

# Create virtual environment
python3.10 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

echo "Downloading the dependencies"

pip install -r requirements.txt

# Create the vector db
cd scripts

python3 generate_full_time_embedded_db.py

# Train the chatbot
cd ..

rasa train

# Setup frontend
cd ../chatbot-interface

echo "Setting up the chatbot's frontend"

# Install the dependencies
npm install

echo "Setup complete"