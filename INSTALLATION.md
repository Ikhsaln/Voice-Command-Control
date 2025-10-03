# 📦 Installation Guide

Panduan lengkap untuk menginstall dan mengkonfigurasi Voice Control Relay System.

## 🎯 System Requirements

### Minimum Requirements
- **OS:** macOS 10.15+, Ubuntu 18.04+, Windows 10+
- **Python:** 3.8 or higher
- **RAM:** 2GB minimum, 4GB recommended
- **Storage:** 500MB free space
- **Network:** Stable internet connection (for speech recognition)

### Recommended Hardware
- **Microphone:** USB condenser microphone (Blue Yeti, Audio-Technica AT2020)
- **CPU:** Intel i5 or equivalent
- **RAM:** 8GB or more
- **Storage:** SSD with 1GB free space

## 🚀 Quick Installation

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd voice-control-relay
```

### Step 2: Install Python Dependencies
```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Install System Dependencies

#### macOS
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install PortAudio
brew install portaudio

# Install PyAudio
pip install pyaudio
```

#### Ubuntu/Debian
```bash
# Update system
sudo apt update

# Install system dependencies
sudo apt install python3-dev portaudio19-dev python3-pyaudio

# Install PyAudio
pip install pyaudio
```

#### Windows
```bash
# Install PyAudio (pre-compiled wheel)
pip install pyaudio
```

### Step 4: Configure Microphone Permissions

#### macOS
1. Go to **System Settings** → **Privacy & Security** → **Microphone**
2. Check ✅ **Terminal** and **Python** applications
3. Restart Terminal if needed

#### Linux
```bash
# PulseAudio/Alsa permissions (usually automatic)
# Test microphone access
arecord -l  # List audio devices
```

#### Windows
1. Go to **Settings** → **Privacy** → **Microphone**
2. Allow microphone access for Python applications

### Step 5: Test Installation
```bash
# Test basic functionality
python -c "import speech_recognition as sr; print('Speech recognition OK')"

# Test microphone access
python -c "
import pyaudio
p = pyaudio.PyAudio()
print(f'Available devices: {p.get_device_count()}')
p.terminate()
"
```

## 🔧 Advanced Configuration

### Environment Variables

Create `.env` file in project root:

```bash
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
PORT=8000
FLASK_HOST=0.0.0.0

# MQTT Configuration
MQTT_BROKER=localhost
MQTT_PORT=1883
MQTT_USERNAME=  # Optional
MQTT_PASSWORD=  # Optional

# Speech Recognition
SPEECH_LANGUAGE=id-ID  # id-ID for Indonesian, en-US for English
SPEECH_TIMEOUT=5       # Seconds to wait for speech
SPEECH_PHRASE_TIME=5   # Maximum phrase length

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/voice_relay.log
```

### MQTT Broker Setup

#### Option 1: Local MQTT Broker (Recommended for Development)
```bash
# Install Mosquitto (macOS)
brew install mosquitto

# Start Mosquitto
brew services start mosquitto

# Or run manually
mosquitto -c /usr/local/etc/mosquitto/mosquitto.conf
```

#### Option 2: Docker MQTT Broker
```bash
# Run Eclipse Mosquitto in Docker
docker run -it -p 1883:1883 eclipse-mosquitto:2.0
```

#### Option 3: Cloud MQTT Broker
- **HiveMQ Cloud** (Free tier available)
- **CloudMQTT** (Paid service)
- **AWS IoT Core** (Enterprise)

### SSL/TLS Configuration (Production)

```bash
# Generate SSL certificates
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Configure Flask for HTTPS
FLASK_SSL_CERT=cert.pem
FLASK_SSL_KEY=key.pem
```

## 🎙️ Microphone Setup

### Test Microphone
```bash
# Record test audio (macOS)
rec -d 3 test.wav
play test.wav

# Record test audio (Linux)
arecord -d 3 -f cd test.wav
aplay test.wav
```

### Configure Audio Settings

#### macOS Audio Settings
1. **System Settings** → **Sound** → **Input**
2. Select your microphone
3. Adjust **Input volume** to 70-80%
4. Test with **Voice Memos** app

#### Linux Audio Settings
```bash
# Check ALSA devices
aplay -l

# Configure PulseAudio (if using)
pactl list sources
pactl set-source-volume <source> 70%
```

### Microphone Recommendations

| Microphone | Price Range | Quality | Best For |
|------------|-------------|---------|----------|
| **Blue Yeti USB** | $100-150 | Professional | Studio recording |
| **Audio-Technica AT2020** | $80-120 | Studio | Podcasting |
| **Fifine K669B** | $30-50 | Good | Budget option |
| **Built-in Mac mic** | Free | Basic | Testing only |

## 🚀 Running the Application

### Development Mode
```bash
# Run with debug mode
FLASK_DEBUG=True python app.py

# Access at: http://localhost:8000
```

### Production Mode
```bash
# Run production server
FLASK_ENV=production python app.py

# Or use Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Docker Deployment
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "app.py"]
```

```bash
# Build and run
docker build -t voice-control .
docker run -p 8000:8000 voice-control
```

## 🔍 Troubleshooting Installation

### Common Issues

#### 1. "PortAudio not found"
```bash
# macOS
brew install portaudio
pip uninstall pyaudio
pip install pyaudio

# Linux
sudo apt install portaudio19-dev
pip install pyaudio
```

#### 2. "No microphone found"
```bash
# Check microphone devices
python -c "
import speech_recognition as sr
for i, mic in enumerate(sr.Microphone.list_microphone_names()):
    print(f'{i}: {mic}')
"
```

#### 3. "Permission denied" (macOS)
- Go to System Settings → Privacy → Microphone
- Allow access for Terminal and Python

#### 4. "MQTT connection failed"
```bash
# Check if MQTT broker is running
netstat -an | grep 1883

# Test MQTT connection
mosquitto_pub -h localhost -t test -m "hello"
```

#### 5. "Speech recognition failed"
- Check internet connection (Google API requires internet)
- Try different microphone
- Adjust microphone volume
- Test with shorter commands

### Debug Commands
```bash
# Check Python environment
python --version
pip list | grep -E "(flask|speech|paho|pyaudio)"

# Test imports
python -c "import flask, speech_recognition, paho.mqtt.client, pyaudio; print('All imports OK')"

# Check system audio
# macOS
system_profiler SPAudioDataType
# Linux
pactl info
```

## 📊 Performance Tuning

### Memory Optimization
```python
# In app.py, adjust worker settings
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
```

### Speech Recognition Optimization
```python
# In voice_control.py
recognizer.energy_threshold = 300    # Lower = more sensitive
recognizer.pause_threshold = 0.8     # Shorter pause detection
recognizer.dynamic_energy_threshold = True
```

### Database Optimization
- JSON file is suitable for small deployments (<100 devices)
- For larger deployments, consider SQLite or PostgreSQL
- Implement data caching for better performance

## 🔒 Security Considerations

### Production Security
```bash
# Use strong passwords
# Configure firewall
# Enable SSL/TLS
# Regular security updates
# Monitor logs for suspicious activity
```

### API Security
```python
# Add authentication if needed
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    # Implement authentication logic
    pass
```

## 📞 Support

If you encounter issues during installation:

1. Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
2. Review application logs in `logs/` directory
3. Test individual components separately
4. Check GitHub Issues for similar problems

## ✅ Post-Installation Checklist

- [ ] Python dependencies installed
- [ ] System dependencies installed
- [ ] Microphone permissions granted
- [ ] Audio devices detected
- [ ] MQTT broker running
- [ ] Application starts without errors
- [ ] Web interface accessible
- [ ] Voice commands work
- [ ] Logs are being written

**Installation complete! 🎉**
