# 📚 **Tutorial Lengkap - Command Voice Relay Control**
## Sistem Kontrol Relay Berbasis Suara PT Grahasumber Prima Elektronik

---

## 🎯 **Panduan Lengkap Menjalankan Program**

### **Persiapan Awal**

#### **1. Sistem Requirements**
```bash
✅ Python 3.8+
✅ MQTT Broker (Mosquitto/Eclipse Mosquitto)
✅ Microphone (untuk voice control)
✅ Port 8000 & 1883 tersedia
```

#### **2. Install Dependencies**
```bash
# Install Python packages
pip3 install -r requirements.txt

# Atau install manual:
pip3 install flask paho-mqtt speechrecognition --break-system-packages
```

#### **3. Setup MQTT Broker**
```bash
# Install Mosquitto (macOS dengan Homebrew)
brew install mosquitto

# Jalankan MQTT broker
brew services start mosquitto

# Atau jalankan manual
mosquitto -c /opt/homebrew/etc/mosquitto/mosquitto.conf
```

---

## 🚀 **Tutorial Step-by-Step**

### **Langkah 1: Testing Sistem**

#### **1.1 Test Backend CRUD Operations**
```bash
# Jalankan test CRUD
python3 test_automation_voice.py

# Output yang diharapkan:
# ✅ All CRUD operations completed successfully!
```

#### **1.2 Test Voice Control Logic**
```bash
# Jalankan test voice control
python3 test_voice_control.py

# Output yang diharapkan:
# ✅ Device matching, ✅ Voice command processing, ✅ Configuration loading
```

#### **1.3 Test Demo Voice Control**
```bash
# Jalankan demonstrasi lengkap
python3 demo_voice_control.py

# Output yang diharapkan:
# ✅ Command analysis, ✅ Object extraction, ✅ Configuration lookup, ✅ MQTT payload creation
```

### **Langkah 2: Setup Device Data**

#### **2.1 Publish Sample Device Data**
```bash
# Terminal 1: Jalankan MQTT publisher
python3 test_devices.py

# Output yang diharapkan:
# ✅ Device data published to MQTT successfully!
```

### **Langkah 3: Jalankan Web Interface**

#### **3.1 Start Flask Application**
```bash
# Terminal 2: Jalankan web server
python3 app.py

# Output yang diharapkan:
# * Serving Flask app 'app'
# * Running on http://127.0.0.1:8000
# * Running on http://192.168.0.164:8000
```

#### **3.2 Akses Website**
```
🌐 Buka browser dan akses:
   http://localhost:8000
   atau
   http://192.168.0.164:8000
```

### **Langkah 4: Konfigurasi Device**

#### **4.1 Buat Configuration Baru**
1. **Pilih Device** dari dropdown (akan terisi otomatis dari MQTT)
2. **Isi Description** (opsional)
3. **Isi Object Name** (penting untuk voice control)
4. **Pilih Pin** (6 untuk RELAYMINI, 8 untuk RELAY)
5. **Klik "Create Configuration"**

#### **4.2 Contoh Configuration**
```json
{
  "id": "auto-generated-uuid",
  "description": "Lampu utama ruangan meeting",
  "object_name": "lampu utama ruangan meeting",
  "device_name": "RelayMini1",
  "part_number": "RELAYMINI",
  "pin": 1,
  "address": 37,
  "device_bus": 0,
  "mac": "70:f7:54:cb:7a:93"
}
```

### **Langkah 5: Voice Control Setup**

#### **5.1 Start Voice Control**
1. Klik tombol **"Start Voice Control"** di web interface
2. Tunggu status berubah menjadi **"Voice control is active..."**

#### **5.2 Voice Commands yang Didukung**

**Bahasa Indonesia:**
- ✅ "nyalakan lampu utama ruangan meeting"
- ✅ "matikan lampu utama ruangan meeting"
- ✅ "hidupkan kipas angin"
- ✅ "padamkan kipas angin"

**English:**
- ✅ "turn on lamp"
- ✅ "turn off lamp"
- ✅ "switch on fan"
- ✅ "switch off fan"

#### **5.3 Cara Kerja Voice Control**
```
1. 🎤 User bicara: "nyalakan lampu utama"
2. 🧠 Speech Recognition: Deteksi "nyalakan" = action "on"
3. 📝 Object Extraction: Ambil "lampu utama"
4. 🔍 Configuration Lookup: Cari di automationVoiceConfig.json
5. 📊 Data Extraction: Ambil pin=1, address=37, dll
6. 📡 MQTT Payload: Buat payload sesuai format
7. 📤 Publish: Kirim ke topic "modular"
8. ⚡ Relay Control: Device menerima dan menjalankan
```

---

## 🔧 **Troubleshooting Guide**

### **Error: Flask Port 5000 Already in Use**
```bash
# Gunakan port alternatif
FLASK_APP=app.py FLASK_RUN_PORT=8000 python3 -m flask run --host=0.0.0.0
```

### **Error: MQTT Broker Not Connected**
```bash
# Cek MQTT broker status
brew services list | grep mosquitto

# Restart MQTT broker
brew services restart mosquitto

# Atau jalankan manual
mosquitto -p 1883
```

### **Error: No Speech Recognition**
```bash
# Install PyAudio untuk microphone support
brew install portaudio
pip3 install pyaudio

# Jika masih error, voice control akan berjalan tanpa microphone
# tapi tetap bisa testing dengan text commands
```

### **Error: Import Module Not Found**
```bash
# Install ulang dependencies
pip3 install --upgrade -r requirements.txt --break-system-packages
```

### **Error: Permission Denied**
```bash
# Jalankan dengan sudo jika perlu
sudo python3 app.py
```

---

## 📊 **Monitoring & Logs**

### **Log Files**
```
logs/voice_relay_YYYYMMDD.log
```

### **Monitoring Commands**
```bash
# Cek proses berjalan
ps aux | grep python

# Cek port yang digunakan
lsof -i :8000
lsof -i :1883

# Monitor MQTT messages
mosquitto_sub -h localhost -t "modular"
mosquitto_sub -h localhost -t "response/automation_voice/result"
```

---

## 🎯 **Testing Scenarios**

### **Scenario 1: Full Voice Control**
```bash
# 1. Start MQTT broker
brew services start mosquitto

# 2. Publish device data
python3 test_devices.py

# 3. Start web interface
python3 app.py

# 4. Create configuration via web UI
# 5. Start voice control
# 6. Say: "nyalakan lampu utama ruangan meeting"
```

### **Scenario 2: Manual Testing**
```bash
# Test tanpa voice (text-based)
python3 demo_voice_control.py

# Test CRUD operations
python3 test_automation_voice.py

# Test device matching
python3 test_voice_control.py
```

### **Scenario 3: API Testing**
```bash
# Test REST API
curl http://localhost:8000/api/configurations
curl http://localhost:8000/api/devices/available

# Test voice control API
curl -X POST http://localhost:8000/api/voice/start
```

---

## 🚀 **Production Deployment**

### **1. Systemd Service (Linux)**
```bash
# Buat service file
sudo nano /etc/systemd/system/voice-relay.service

[Unit]
Description=Voice Relay Control Service
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/voice-relay
ExecStart=/usr/bin/python3 app.py
Restart=always

[Install]
WantedBy=multi-user.target

# Enable dan start service
sudo systemctl enable voice-relay
sudo systemctl start voice-relay
```

### **2. Docker Deployment**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "app.py"]
```

### **3. Nginx Reverse Proxy**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📞 **Support & Help**

### **Common Issues & Solutions**

| Problem | Solution |
|---------|----------|
| **Port already in use** | Change port in app.py or kill process |
| **MQTT connection failed** | Check broker is running on port 1883 |
| **Voice not recognized** | Check microphone permissions |
| **Device not found** | Verify object_name in configuration |
| **Web interface not loading** | Check Flask is running on correct port |

### **Debug Commands**
```bash
# Check Python version
python3 --version

# Check installed packages
pip3 list | grep -E "(flask|mqtt|speech)"

# Check network connectivity
ping localhost
telnet localhost 1883

# Check file permissions
ls -la JSON/
ls -la logs/
```

---

## 🎉 **Success Checklist**

- ✅ **Dependencies installed**
- ✅ **MQTT broker running**
- ✅ **Flask app started**
- ✅ **Web interface accessible**
- ✅ **Device data published**
- ✅ **Configuration created**
- ✅ **Voice control working**
- ✅ **MQTT messages flowing**
- ✅ **Relay control functional**

---

## 📝 **Catatan Penting**

1. **Object Name** sangat penting untuk voice recognition
2. **MQTT broker** harus running sebelum start aplikasi
3. **Microphone permission** diperlukan untuk voice control
4. **Port 8000** untuk web, **port 1883** untuk MQTT
5. **Logs** tersimpan di folder `logs/` untuk debugging

---

**🎯 Sistem siap digunakan! Akses: http://localhost:8000**
