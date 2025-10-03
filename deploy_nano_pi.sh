#!/bin/bash

# Deployment script for Nano Pi
# Run this on your Nano Pi after transferring the project files

echo "=== Command Voice Relay - Nano Pi Deployment ==="

# Update system
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python and pip if not installed
echo "Installing Python and pip..."
sudo apt install python3 python3-pip python3-venv -y

# Install system dependencies for speech recognition
echo "Installing system dependencies for speech recognition..."
sudo apt install portaudio19-dev python3-pyaudio -y

# Create project directory
echo "Setting up project directory..."
mkdir -p ~/command-voice-relay
cd ~/command-voice-relay

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Install Mosquitto MQTT broker if not already installed
echo "Installing MQTT broker..."
sudo apt install mosquitto mosquitto-clients -y

# Start MQTT broker
echo "Starting MQTT broker..."
sudo systemctl enable mosquitto
sudo systemctl start mosquitto

# Configure firewall (optional - allow port 8000)
echo "Configuring firewall..."
sudo ufw allow 8000
sudo ufw allow 1883  # MQTT port
sudo ufw --force enable

echo "=== Deployment completed! ==="
echo "To start the application:"
echo "cd ~/command-voice-relay"
echo "python3 app.py"
echo ""
echo "Access the web interface at: http://192.168.0.193:8000"
