# Deployment Guide - Nano Pi

Panduan lengkap untuk men-deploy aplikasi Command Voice Relay ke Nano Pi dengan IP 192.168.0.193.

## 📋 Prerequisites

- Nano Pi dengan sistem operasi Linux (Ubuntu/Debian-based)
- Akses SSH ke Nano Pi
- Koneksi internet pada Nano Pi
- Port 8000 dan 1883 tersedia

## 🚀 Langkah-langkah Deployment

### 1. Transfer File ke Nano Pi

Transfer semua file proyek ke Nano Pi menggunakan SCP atau SFTP:

```bash
# Dari komputer lokal Anda
scp -r /path/to/command-voice-relay pi@192.168.0.193:~/
```

Atau menggunakan rsync untuk transfer yang lebih efisien:
```bash
rsync -avz /path/to/command-voice-relay pi@192.168.0.193:~/
```

### 2. SSH ke Nano Pi

```bash
ssh pi@192.168.0.193
```

### 3. Jalankan Script Deployment

```bash
cd ~/command-voice-relay
chmod +x deploy_nano_pi.sh
sudo ./deploy_nano_pi.sh
```

Script ini akan:
- Update sistem
- Install Python dan dependencies
- Install Mosquitto MQTT broker
- Setup firewall
- Install Python packages

### 4. Setup Systemd Service (Opsional - untuk auto-start)

```bash
# Copy service file
sudo cp command-voice-relay.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable command-voice-relay

# Start service
sudo systemctl start command-voice-relay

# Check status
sudo systemctl status command-voice-relay
```

### 5. Manual Start (Alternatif)

Jika tidak menggunakan systemd:

```bash
cd ~/command-voice-relay
python3 app.py
```

## 🌐 Akses Web Interface

Setelah aplikasi berjalan, akses dari browser:

```
http://192.168.0.193:8000
```

## 🔧 Konfigurasi Tambahan

### Firewall Settings

Jika perlu mengubah firewall:

```bash
# Check status
sudo ufw status

# Allow additional ports jika diperlukan
sudo ufw allow 22    # SSH
sudo ufw allow 8000  # Flask app
sudo ufw allow 1883  # MQTT
```

### MQTT Broker Configuration

MQTT broker Mosquitto sudah terinstall. Konfigurasi default:
- Host: localhost
- Port: 1883
- No authentication

Untuk konfigurasi custom, edit `/etc/mosquitto/mosquitto.conf`

### Environment Variables

Anda bisa mengatur environment variables:

```bash
export FLASK_DEBUG=False
export FLASK_HOST=0.0.0.0
export PORT=8000
```

## 🧪 Testing

### Test MQTT Connection

```bash
# Subscribe ke topic
mosquitto_sub -h localhost -t "test/topic"

# Publish message dari terminal lain
mosquitto_pub -h localhost -t "test/topic" -m "Hello from Nano Pi"
```

### Test Web Interface

1. Buka `http://192.168.0.193:8000`
2. Coba load configurations
3. Test voice commands

### Test Device Connection

1. Pastikan perangkat relay terhubung ke jaringan yang sama
2. Publish device data ke MQTT topic `MODULAR_DEVICE/AVAILABLES`
3. Check di web interface apakah device muncul

## 📊 Monitoring

### Logs

```bash
# Application logs
tail -f ~/command-voice-relay/logs/voice_relay_$(date +%Y%m%d).log

# System logs
sudo journalctl -u command-voice-relay -f
```

### System Resources

```bash
# Check memory usage
free -h

# Check CPU usage
top

# Check disk usage
df -h
```

## 🔄 Update Aplikasi

Untuk update aplikasi:

1. Transfer file baru ke Nano Pi
2. Restart service:

```bash
sudo systemctl restart command-voice-relay
```

Atau jika manual:
```bash
pkill -f "python3 app.py"
cd ~/command-voice-relay
python3 app.py
```

## 🐛 Troubleshooting

### Aplikasi Tidak Bisa Diakses

1. Check apakah aplikasi running:
```bash
ps aux | grep python3
```

2. Check port:
```bash
netstat -tlnp | grep 8000
```

3. Check firewall:
```bash
sudo ufw status
```

### MQTT Connection Failed

1. Check MQTT broker:
```bash
sudo systemctl status mosquitto
```

2. Test MQTT:
```bash
mosquitto_pub -h localhost -t "test" -m "test"
```

### Voice Control Tidak Berfungsi

1. Check microphone access:
```bash
arecord -l
```

2. Install audio dependencies:
```bash
sudo apt install portaudio19-dev python3-pyaudio
```

## 📞 Support

Jika ada masalah, check:
1. Logs aplikasi
2. System logs
3. MQTT broker status
4. Network connectivity

IP Nano Pi: `192.168.0.193`
Port Aplikasi: `8000`
Port MQTT: `1883`
