# Setup the backend
cd chatbot-core

Write-Host "Setting up the chatbot's backend"

# Create virtual environment
python3.10 -m venv .venv

# Activate virtual environment
source .venv/Scripts/Activate.ps1

Write-Host "Downloading the dependencies"

pip install -r requirements.txt

# Create the vector db
cd scripts

python3 generate_full_time_embedded_db.py

# Train the chatbot
cd ..

rasa train

# Setup frontend
cd ../chatbot-interface

Write-Host "Setting up the chatbot's frontend"

# Install the dependencies
npm install

Write-Host "Setup complete"