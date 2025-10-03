# 🎤 Voice Control Relay System

Sistem kontrol relay berbasis suara dengan antarmuka web modern untuk otomasi rumah tangga dan IoT. Mendukung kontrol perangkat relay melalui perintah suara dalam bahasa Indonesia dan Inggris.

## ✨ Fitur Utama

- 🎙️ **Voice Control** - Kontrol perangkat dengan perintah suara
- 🌐 **Web Interface** - Antarmuka web responsif dan modern
- 🔄 **Real-time Monitoring** - Monitoring status perangkat secara real-time
- 📱 **RESTful API** - API lengkap untuk integrasi
- 🔗 **MQTT Integration** - Komunikasi real-time dengan perangkat IoT
- 🎯 **Multi-language** - Dukungan bahasa Indonesia dan Inggris
- 📊 **Device Management** - Manajemen perangkat relay lengkap

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- macOS/Linux/Windows
- Mikrofon (USB recommended)
- MQTT Broker (opsional untuk development)

### Installation

```bash
# Clone repository
git clone <repository-url>
cd voice-control-relay

# Install dependencies
pip install -r requirements.txt

# Install system dependencies (macOS)
brew install portaudio

# Run application
python app.py
```

### Akses Aplikasi

Buka browser dan akses: `http://localhost:8000`

## 🎯 Voice Commands

### Bahasa Indonesia
- "nyalakan [nama perangkat]" - Menyalakan perangkat
- "matikan [nama perangkat]" - Mematikan perangkat
- "hidupkan [nama perangkat]" - Menyalakan perangkat
- "padamkan [nama perangkat]" - Mematikan perangkat

### English
- "turn on [device name]" - Turn on device
- "turn off [device name]" - Turn off device
- "switch on [device name]" - Turn on device
- "switch off [device name]" - Turn off device

### Contoh Penggunaan
```
"nyalakan lampu utama"
"matikan lampu tamu"
"turn on living room light"
"turn off bedroom lamp"
```

## 🏗️ Arsitektur Sistem

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Browser   │────│   Flask App     │────│   MQTT Broker   │
│                 │    │   (Backend)     │    │                 │
│ • User Interface│    │ • REST API      │    │ • Device Comm   │
│ • Voice Control │    │ • Voice Engine  │    │ • Real-time     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Relay Devices │
                       │   (Physical)    │
                       └─────────────────┘
```

## 📁 Struktur Proyek

```
voice-control-relay/
├── app.py                      # Main Flask application
├── voice_control.py            # Voice recognition engine
├── AutomationVoice.py          # Device management service
├── middleware/
│   ├── mqtt_handler.py         # MQTT communication
│   ├── logging.py              # Logging utilities
│   └── network_utils.py        # Network utilities
├── templates/
│   ├── index.html              # Main web interface
│   └── index_modern.html       # Alternative interface
├── static/                     # Static assets
├── JSON/
│   └── automationVoiceConfig.json  # Device configurations
├── logs/                       # Application logs
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🔧 Konfigurasi

### Environment Variables

```bash
# Flask Configuration
FLASK_ENV=production          # production/development
FLASK_DEBUG=False            # True/False
PORT=8000                    # Port number

# MQTT Configuration
MQTT_BROKER=localhost        # MQTT broker address
MQTT_PORT=1883              # MQTT port
```

### Device Configuration

Edit file `JSON/automationVoiceConfig.json`:

```json
[
  {
    "id": "unique-id",
    "desc": "Lampu utama ruangan",
    "object_name": "lampu utama",
    "device_name": "RelayMini1",
    "part_number": "RELAYMINI",
    "pin": 1,
    "address": 37,
    "device_bus": 0,
    "mac": "70:f7:54:cb:7a:93"
  }
]
```

## 🚀 Deployment

### Docker Deployment

```bash
# Build image
docker build -t voice-control-system .

# Run container
docker run -p 8000:8000 voice-control-system
```

### Production Deployment

```bash
# Install as system service
sudo cp command-voice-relay.service /etc/systemd/system/
sudo systemctl enable command-voice-relay
sudo systemctl start command-voice-relay
```

## 📊 Monitoring

### Health Check
```bash
curl http://localhost:8000/api/status/mqtt
```

### Logs
```bash
tail -f logs/voice_relay_$(date +%Y%m%d).log
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Speech Recognition API
- Flask web framework
- Paho MQTT library
- Tailwind CSS

## 📞 Support

Untuk bantuan atau pertanyaan:
- Buat issue di GitHub
- Email: support@example.com
- Dokumentasi lengkap: [Wiki](https://github.com/username/repo/wiki)

---

**Made with ❤️ for IoT and Home Automation**
