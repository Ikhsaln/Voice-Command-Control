# 👥 User Guide - Voice Control Relay System

Panduan lengkap untuk pengguna sistem kontrol relay berbasis suara.

## 🎯 Quick Start

### Langkah 1: Jalankan Aplikasi
```bash
cd voice-control-relay
python app.py
```

### Langkah 2: Akses Web Interface
Buka browser dan kunjungi: `http://localhost:8000`

### Langkah 3: Setup Device Pertama
1. Klik **"New Configuration"**
2. Pilih device dari dropdown
3. Isi nama objek (contoh: "lampu utama")
4. Pilih PIN yang tersedia
5. Klik **"Create Configuration"**

### Langkah 4: Test Voice Control
1. Klik **"Start Voice Control"**
2. Katakan: **"nyalakan lampu utama"**
3. Perangkat akan merespons perintah

## 🎙️ Voice Commands

### Bahasa Indonesia

#### Perintah Dasar
| Perintah | Contoh | Fungsi |
|----------|--------|--------|
| `nyalakan [nama]` | "nyalakan lampu utama" | Menyalakan perangkat |
| `matikan [nama]` | "matikan lampu utama" | Mematikan perangkat |
| `hidupkan [nama]` | "hidupkan lampu tamu" | Menyalakan perangkat |
| `padamkan [nama]` | "padamkan lampu tamu" | Mematikan perangkat |
| `aktifkan [nama]` | "aktifkan kipas angin" | Menyalakan perangkat |

#### Perintah Toggle
| Perintah | Contoh | Fungsi |
|----------|--------|--------|
| `toggle [nama]` | "toggle lampu kamar" | Mengubah status perangkat |
| `ubah [nama]` | "ubah lampu tidur" | Mengubah status perangkat |
| `ganti [nama]` | "ganti lampu dapur" | Mengubah status perangkat |

### English Commands

#### Basic Commands
| Command | Example | Function |
|---------|---------|----------|
| `turn on [name]` | "turn on living room light" | Turn on device |
| `turn off [name]` | "turn off living room light" | Turn off device |
| `switch on [name]` | "switch on bedroom lamp" | Turn on device |
| `switch off [name]` | "switch off bedroom lamp" | Turn off device |
| `power on [name]` | "power on fan" | Turn on device |
| `power off [name]` | "power off fan" | Turn off device |

### Tips Penggunaan Voice Commands

#### ✅ Do's
- Ucapkan dengan jelas dan normal volume
- Gunakan nama objek yang sudah dikonfigurasi
- Jaga jarak 15-30 cm dari mikrofon
- Pastikan environment quiet (tidak bising)
- Test dulu dengan "Test Command" button

#### ❌ Don'ts
- Jangan berbicara terlalu cepat
- Jangan gunakan nama yang belum terdaftar
- Jangan ada background noise yang keras
- Jangan tutup mulut saat berbicara
- Jangan gunakan aksen yang terlalu kental

## 🖥️ Web Interface Guide

### Dashboard Overview

#### Statistics Cards
- **Total Devices**: Jumlah device yang terdeteksi
- **Configurations**: Jumlah konfigurasi voice yang aktif
- **Voice Control**: Status voice recognition (Active/Inactive)
- **MQTT Status**: Status koneksi MQTT broker

#### Action Buttons
- **Start Voice Control**: Mengaktifkan voice recognition
- **Stop Voice Control**: Menonaktifkan voice recognition
- **Test Command**: Test voice command tanpa real device
- **Discover Devices**: Scan device baru di jaringan
- **New Configuration**: Tambah konfigurasi baru

### Device Management

#### Menambah Device Baru
1. Klik **"New Configuration"**
2. **Pilih Device**: Pilih dari dropdown device yang tersedia
3. **Object Name**: Nama yang akan digunakan untuk voice command
   - Contoh: "lampu utama", "kipas angin", "tv ruang tamu"
4. **PIN**: Pilih PIN yang tersedia untuk device tersebut
5. **Description**: Deskripsi opsional (untuk dokumentasi)
6. Klik **"Create Configuration"**

#### Mengedit Device
1. Klik ikon **Edit** (pensil) pada baris device
2. Ubah **Device**, **Object Name**, **PIN**, atau **Description**
3. Klik **"Update"** untuk menyimpan

#### Menghapus Device
1. Klik ikon **Delete** (sampah) pada baris device
2. Konfirmasi penghapusan
3. Device akan dihapus dari sistem

### Voice Control Features

#### Start Voice Control
1. Klik **"Start Voice Control"**
2. Sistem akan:
   - Mengakses mikrofon
   - Menampilkan status "Active"
   - Mulai listening untuk voice commands

#### Test Voice Commands
1. Klik **"Test Command"**
2. Masukkan command text secara manual
3. Klik **"Test Command"**
4. Sistem akan memproses tanpa mengirim ke device fisik

#### Stop Voice Control
1. Klik **"Stop Voice Control"**
2. Sistem akan:
   - Menonaktifkan mikrofon access
   - Menampilkan status "Inactive"
   - Menutup voice recognition

## 🔧 Device Configuration

### Understanding Device Parameters

#### Device Name
- Nama hardware device (RelayMini1, Relay1, dll)
- Otomatis terdeteksi dari MQTT broker

#### Part Number
- Tipe device hardware
- **RELAYMINI**: 6 PIN available (PIN1-PIN6)
- **RELAY**: 8 PIN available (PIN1-PIN8)

#### PIN Configuration
- PIN fisik pada device relay
- Setiap PIN mengontrol satu perangkat
- PIN yang sama bisa digunakan untuk device berbeda

#### Address & Device Bus
- Parameter komunikasi MQTT
- Biasanya tidak perlu diubah
- Auto-detected saat device discovery

### Best Practices untuk Naming

#### ✅ Good Object Names
- "lampu utama" → jelas dan spesifik
- "kipas angin kamar" → deskriptif
- "tv ruang tamu" → spesifik lokasi
- "pintu garasi" → jelas fungsi

#### ❌ Bad Object Names
- "device1" → tidak deskriptif
- "relay" → terlalu umum
- "lampu" → ambigu (lampu mana?)
- "test" → temporary naming

## 📊 Monitoring & Status

### Device Status Indicators

#### Status Colors
- 🟢 **Online**: Device aktif dan merespons
- 🔴 **Offline**: Device tidak merespons (timeout)
- 🟡 **Unknown**: Status belum diketahui

#### Status Information
- **Last Seen**: Timestamp terakhir device online
- **Heartbeat Interval**: Frekuensi check device (default: 30s)
- **MAC Address**: Alamat hardware device
- **Connection Status**: MQTT connection state

### Logs & Troubleshooting

#### Melihat Logs Aplikasi
```bash
# Real-time logs
tail -f logs/voice_relay_$(date +%Y%m%d).log

# Search specific errors
grep "ERROR" logs/voice_relay_$(date +%Y%m%d).log
```

#### Common Issues & Solutions

##### Voice Commands Tidak Berfungsi
**Symptoms**: Command diakui tapi device tidak merespons
**Solutions**:
- Periksa koneksi MQTT broker
- Pastikan device fisik tersambung
- Check PIN configuration
- Verify device power supply

##### Speech Recognition Gagal
**Symptoms**: "Could not understand audio"
**Solutions**:
- Periksa koneksi internet (Google API)
- Upgrade ke USB microphone
- Kurangi background noise
- Ucapkan lebih jelas

##### Device Status "Offline"
**Symptoms**: Device tampil offline terus menerus
**Solutions**:
- Check physical device connection
- Verify MQTT broker running
- Restart device hardware
- Check network connectivity

## 🎛️ Advanced Features

### Device Discovery
1. Klik **"Discover Devices"**
2. Sistem akan scan jaringan untuk device baru
3. Device baru akan muncul di dropdown
4. Konfigurasi device baru seperti biasa

### Bulk Operations
- Saat ini belum support bulk operations
- Edit/delete per device individual
- Future: bulk import/export configurations

### Custom Voice Commands
- Sistem menggunakan predefined commands
- Tidak support custom commands saat ini
- Future: user-defined command patterns

## 🔒 Security & Safety

### Best Practices
- ✅ Jaga keamanan MQTT broker
- ✅ Gunakan password untuk web interface (jika diperlukan)
- ✅ Monitor logs untuk aktivitas mencurigakan
- ✅ Update sistem secara berkala
- ✅ Backup configurations regularly

### Safety Precautions
- ⚠️ Pastikan device relay kompatibel dengan beban
- ⚠️ Jangan overload electrical circuits
- ⚠️ Monitor temperature device saat continuous use
- ⚠️ Gunakan surge protectors
- ⚠️ Regular maintenance check

## 📱 Mobile Access

### Local Network Access
```bash
# Find your IP address
ifconfig  # macOS/Linux
ipconfig  # Windows

# Access from mobile browser
http://[YOUR_IP]:8000
```

### Remote Access (Advanced)
- Setup VPN untuk secure remote access
- Configure reverse proxy (nginx)
- Use HTTPS untuk encrypted communication
- Implement authentication

## 🔄 Backup & Restore

### Backup Configurations
```bash
# Copy configuration file
cp JSON/automationVoiceConfig.json backup/config_$(date +%Y%m%d).json
```

### Restore Configurations
```bash
# Restore from backup
cp backup/config_20231201.json JSON/automationVoiceConfig.json

# Restart application
# Configurations will be loaded automatically
```

## 📞 Support & Help

### Getting Help
1. **Check Logs**: Lihat `logs/` directory untuk error details
2. **Test Components**: Gunakan "Test Command" untuk isolate issues
3. **Restart Services**: Restart aplikasi jika ada masalah
4. **Check Network**: Pastikan MQTT dan internet connection

### Common Support Questions

#### Q: Voice commands tidak dideteksi?
A: Check microphone permissions dan test dengan "Test Command" button.

#### Q: Device tidak merespons?
A: Verify MQTT connection dan check device physical connection.

#### Q: Speech recognition error?
A: Pastikan internet connection stabil dan coba USB microphone.

#### Q: Bagaimana reset semua configurations?
A: Stop aplikasi, delete `JSON/automationVoiceConfig.json`, restart aplikasi.

## 🎯 Tips & Tricks

### Productivity Tips
- Gunakan nama objek yang konsisten
- Group devices by room/location
- Test semua commands secara berkala
- Monitor device status regularly
- Backup configurations sebelum major changes

### Performance Optimization
- Gunakan USB microphone untuk best results
- Keep environment quiet during voice commands
- Close unnecessary applications
- Monitor system resources
- Regular system maintenance

---

**Happy Voice Controlling! 🎉**
