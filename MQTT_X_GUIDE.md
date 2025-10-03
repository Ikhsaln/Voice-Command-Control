# 📡 **Panduan Lengkap Konfigurasi MQTT X**
## Untuk Sistem Command Voice Relay Control

---

## 🎯 **MQTT X Setup untuk Testing & Development**

### **1. Download & Install MQTT X**

#### **macOS:**
```bash
# Download dari website resmi
# https://mqttx.app/

# Atau menggunakan Homebrew
brew install mqttx
```

#### **Windows/Linux:**
- Download dari: https://mqttx.app/
- Install seperti aplikasi biasa

### **2. Jalankan MQTT Broker**

#### **Pastikan Mosquitto Running:**
```bash
# Cek status
brew services list | grep mosquitto

# Start jika belum running
brew services start mosquitto

# Atau start manual
mosquitto -c /opt/homebrew/etc/mosquitto/mosquitto.conf
```

---

## 🔧 **Konfigurasi MQTT X Step-by-Step**

### **Step 1: Buka MQTT X**

1. **Launch MQTT X** dari Applications/Start Menu
2. **Interface utama** akan muncul

### **Step 2: Buat New Connection**

1. **Klik "+"** di kiri atas untuk new connection
2. **Isi Connection Details:**
   ```
   Name: Voice Relay Local
   Client ID: mqttx_local_test
   Host: localhost
   Port: 1883
   Username: (kosong)
   Password: (kosong)
   ```
3. **Klik "Connect"**

### **Step 3: Verify Connection**

- **Status harus "Connected"** (hijau)
- **Jika gagal**, cek MQTT broker status

---

## 📤 **Testing Device Discovery**

### **Step 1: Publish Device Data**

1. **Klik tab "Publish"** di MQTT X
2. **Isi Topic:** `MODULAR_DEVICE/AVAILABLES`
3. **Isi Payload:**
   ```json
   [
     {
       "id": "",
       "name": "RelayMini1",
       "address": 37,
       "device_bus": 0,
       "part_number": "RELAYMINI",
       "mac": "70:f7:54:cb:7a:93",
       "device_type": "Modular",
       "manufacturer": "IOT",
       "topic": "Limbah/Modular/relay_mini/1"
     },
     {
       "id": "",
       "name": "Relay1",
       "address": 35,
       "device_bus": 0,
       "part_number": "RELAY",
       "mac": "70:f7:54:cb:7a:94",
       "device_type": "Modular",
       "manufacturer": "IOT",
       "topic": "Limbah/Modular/relay/1"
     }
   ]
   ```
4. **Klik "Publish"**

### **Step 2: Verify Device Reception**

1. **Buka web interface** di `http://localhost:8000`
2. **Cek dropdown "Device Name"** - harus muncul "RelayMini1 (RELAYMINI)"
3. **Pilih device** dan lihat info otomatis terisi

---

## 📥 **Monitoring System Topics**

### **Step 1: Subscribe ke Response Topics**

1. **Klik tab "Subscriptions"** di MQTT X
2. **Add subscriptions:**
   ```
   Topic: response/automation_voice/result
   QoS: 0
   ```
3. **Klik "Subscribe"**

### **Step 2: Subscribe ke Control Topics**

**Tambahkan subscriptions:**
```
Topic: modular
QoS: 0
```

---

## 🎮 **Testing Voice Control Commands**

### **Step 1: Buat Configuration**

1. **Di web interface** (`http://localhost:8000`):
   - Pilih device: "RelayMini1"
   - Description: "Lampu utama ruangan meeting"
   - Object Name: **"lampu utama"** (penting untuk voice)
   - Pin: PIN1
   - Klik "Create Configuration"

### **Step 2: Test Voice Command via MQTT X**

1. **Di MQTT X tab "Publish"**
2. **Topic:** `modular`
3. **Payload untuk ON:**
   ```json
   {
     "mac": "70:f7:54:cb:7a:93",
     "protocol_type": "Modular",
     "device": "RELAYMINI",
     "function": "write",
     "value": {
       "pin": 1,
       "data": 1
     },
     "address": 37,
     "device_bus": 0,
     "Timestamp": "2025-10-01 10:20:00"
   }
   ```
4. **Klik "Publish"**

### **Step 3: Test Voice Command via Web Interface**

1. **Di web interface**, klik **"Start Voice Control"**
2. **Katakan:** "nyalakan lampu utama"
3. **Monitor di MQTT X** tab "Subscriptions" - harus ada payload terkirim ke topic "modular"

---

## 🔍 **Advanced MQTT X Features**

### **1. Message History**

- **Klik tab "History"** untuk melihat semua messages
- **Filter by topic** untuk melihat spesifik messages
- **Export messages** untuk debugging

### **2. Multiple Connections**

- **Buat connection baru** untuk testing paralel
- **Connection 1:** Untuk publishing device data
- **Connection 2:** Untuk monitoring control commands

### **3. QoS Testing**

- **Test QoS 0, 1, 2** untuk reliability testing
- **Monitor message delivery** dengan retained messages

---

## 🐛 **Troubleshooting MQTT X**

### **Connection Issues**

#### **Error: Connection Refused**
```
✅ Cek MQTT broker running:
brew services list | grep mosquitto

✅ Restart broker:
brew services restart mosquitto

✅ Cek port 1883 tidak blocked:
telnet localhost 1883
```

#### **Error: Authentication Failed**
```
✅ Pastikan username/password kosong
✅ Cek broker config untuk anonymous access
```

### **Message Issues**

#### **Messages Tidak Terima**
```
✅ Cek topic spelling (case-sensitive)
✅ Verify QoS settings
✅ Check retained message settings
```

#### **Messages Tidak Publish**
```
✅ Verify JSON format valid
✅ Check connection status (hijau)
✅ Monitor broker logs
```

---

## 📊 **MQTT X untuk Production Testing**

### **1. Load Testing**

- **Publish multiple messages** secara berurutan
- **Monitor response times** di subscriptions
- **Test connection stability** dengan long-running sessions

### **2. Integration Testing**

- **Test dengan real hardware** jika tersedia
- **Monitor actual relay responses**
- **Verify end-to-end functionality**

### **3. Debugging Production Issues**

- **Capture all MQTT traffic** dengan MQTT X
- **Analyze message patterns** untuk troubleshooting
- **Test failover scenarios** dengan broker restart

---

## 🎯 **MQTT X Shortcuts & Tips**

### **Keyboard Shortcuts:**
- `Ctrl+N`: New connection
- `Ctrl+T`: New tab
- `Ctrl+Enter`: Publish message
- `Ctrl+L`: Clear log

### **Best Practices:**
- **Gunakan descriptive names** untuk connections
- **Save frequently used payloads** sebagai templates
- **Monitor connection status** terus menerus
- **Use different colors** untuk different connection types

### **Advanced Features:**
- **Scripts**: Automate testing scenarios
- **Import/Export**: Share connection configs
- **Themes**: Customize UI appearance
- **Plugins**: Extend functionality

---

## 📋 **Checklist Testing dengan MQTT X**

### **✅ Basic Connectivity**
- [ ] MQTT broker running
- [ ] MQTT X connected (status hijau)
- [ ] Can publish test message
- [ ] Can subscribe to topics

### **✅ Device Discovery**
- [ ] Publish device data ke `MODULAR_DEVICE/AVAILABLES`
- [ ] Web interface menampilkan devices
- [ ] Device filtering working (RELAYMINI/RELAY only)

### **✅ Voice Control**
- [ ] Create configuration dengan object_name
- [ ] Voice control dapat start/stop
- [ ] Commands dipublish ke topic `modular`
- [ ] Payload format sesuai spesifikasi

### **✅ System Integration**
- [ ] All CRUD operations working
- [ ] Real-time updates via MQTT
- [ ] Error handling proper
- [ ] Logging comprehensive

---

## 🚀 **Quick Start Commands**

```bash
# 1. Start MQTT broker
brew services start mosquitto

# 2. Start web app
python3 app.py

# 3. Publish device data
python3 test_devices.py

# 4. Open MQTT X and connect to localhost:1883

# 5. Test voice control
python3 demo_voice_control.py
```

---

**🎉 MQTT X siap digunakan untuk testing sistem Command Voice Relay Control!**

**Dokumentasi lengkap:** `MQTT_X_GUIDE.md`
