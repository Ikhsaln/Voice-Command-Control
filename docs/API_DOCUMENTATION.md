# 🔌 API Documentation - Voice Control Relay System

Dokumentasi lengkap REST API untuk sistem kontrol relay berbasis suara.

## 📋 Overview

API ini menyediakan interface lengkap untuk:
- Manajemen device dan konfigurasi
- Kontrol voice recognition
- Monitoring status sistem
- Device discovery dan heartbeat

**Base URL**: `http://localhost:8000` (default)
**Content-Type**: `application/json`

## 🔐 Authentication

Saat ini API tidak memerlukan authentication. Untuk production, sebaiknya implementasikan:
- API Key authentication
- JWT tokens
- Basic HTTP authentication

## 📚 API Endpoints

### Device Management

#### GET /api/devices
Mengambil daftar semua device yang terdeteksi.

**Response:**
```json
{
  "success": true,
  "devices": [
    {
      "device_name": "RelayMini1",
      "part_number": "RELAYMINI",
      "mac": "70:f7:54:cb:7a:93",
      "status": "online",
      "last_seen": "2023-12-01 10:30:00",
      "address": 37,
      "device_bus": 0
    }
  ]
}
```

#### GET /api/devices/{device_name}
Mengambil detail device spesifik.

**Parameters:**
- `device_name` (string): Nama device

**Response:**
```json
{
  "success": true,
  "device": {
    "device_name": "RelayMini1",
    "part_number": "RELAYMINI",
    "mac": "70:f7:54:cb:7a:93",
    "status": "online",
    "last_seen": "2023-12-01 10:30:00",
    "address": 37,
    "device_bus": 0,
    "available_pins": [1, 2, 3, 4, 5, 6]
  }
}
```

#### POST /api/devices/discover
Melakukan discovery device baru di jaringan.

**Response:**
```json
{
  "success": true,
  "message": "Device discovery started",
  "devices_found": 2
}
```

### Configuration Management

#### GET /api/configurations
Mengambil semua konfigurasi voice control.

**Response:**
```json
{
  "success": true,
  "configurations": [
    {
      "id": "config_001",
      "device_name": "RelayMini1",
      "object_name": "lampu utama",
      "description": "Lampu utama ruangan tamu",
      "part_number": "RELAYMINI",
      "pin": 1,
      "address": 37,
      "device_bus": 0,
      "mac": "70:f7:54:cb:7a:93"
    }
  ]
}
```

#### POST /api/configurations
Membuat konfigurasi baru.

**Request Body:**
```json
{
  "device_name": "RelayMini1",
  "object_name": "lampu utama",
  "description": "Lampu utama ruangan tamu",
  "pin": 1
}
```

**Response:**
```json
{
  "success": true,
  "message": "Configuration created successfully",
  "configuration": {
    "id": "config_001",
    "device_name": "RelayMini1",
    "object_name": "lampu utama",
    "description": "Lampu utama ruangan tamu",
    "pin": 1,
    "address": 37,
    "device_bus": 0,
    "mac": "70:f7:54:cb:7a:93"
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "PIN 1 is already in use on device RelayMini1"
}
```

#### PUT /api/configurations/{id}
Update konfigurasi existing.

**Parameters:**
- `id` (string): Configuration ID

**Request Body:**
```json
{
  "object_name": "lampu tamu",
  "description": "Lampu tamu ruangan tamu",
  "pin": 2
}
```

**Response:**
```json
{
  "success": true,
  "message": "Configuration updated successfully",
  "configuration": { ... }
}
```

#### DELETE /api/configurations/{id}
Menghapus konfigurasi.

**Parameters:**
- `id` (string): Configuration ID

**Response:**
```json
{
  "success": true,
  "message": "Configuration deleted successfully"
}
```

### Voice Control

#### POST /api/voice/start
Memulai voice control recognition.

**Response:**
```json
{
  "success": true,
  "message": "Voice control started",
  "status": "active"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "No microphone available"
}
```

#### POST /api/voice/stop
Menghentikan voice control recognition.

**Response:**
```json
{
  "success": true,
  "message": "Voice control stopped",
  "status": "inactive"
}
```

#### GET /api/voice/status
Mengecek status voice control.

**Response:**
```json
{
  "success": true,
  "status": "active",
  "microphone_available": true,
  "last_command": "nyalakan lampu utama",
  "last_command_time": "2023-12-01 10:35:00"
}
```

#### POST /api/voice/test
Test voice command tanpa real device control.

**Request Body:**
```json
{
  "command": "nyalakan lampu utama"
}
```

**Response:**
```json
{
  "success": true,
  "command": "nyalakan lampu utama",
  "action": "on",
  "object_name": "lampu utama",
  "device_found": true,
  "device_name": "RelayMini1",
  "pin": 1,
  "mqtt_payload": {
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
    "Timestamp": "2023-12-01 10:35:00"
  }
}
```

### System Status & Monitoring

#### GET /api/status
Mengambil status keseluruhan sistem.

**Response:**
```json
{
  "success": true,
  "system": {
    "version": "1.0.0",
    "uptime": "2 hours 15 minutes",
    "python_version": "3.9.7",
    "platform": "macOS-12.1"
  },
  "services": {
    "flask": "running",
    "mqtt": "connected",
    "voice_control": "active"
  },
  "statistics": {
    "total_devices": 3,
    "active_configurations": 5,
    "total_commands_processed": 127,
    "success_rate": 94.5
  }
}
```

#### GET /api/status/mqtt
Mengecek status koneksi MQTT.

**Response:**
```json
{
  "success": true,
  "mqtt": {
    "connected": true,
    "broker": "localhost",
    "port": 1883,
    "client_id": "voice_control_main",
    "last_ping": "2023-12-01 10:35:00",
    "connection_time": "2023-12-01 08:20:00"
  }
}
```

#### GET /api/status/devices
Status semua device yang terdeteksi.

**Response:**
```json
{
  "success": true,
  "devices": [
    {
      "device_name": "RelayMini1",
      "status": "online",
      "last_heartbeat": "2023-12-01 10:34:45",
      "uptime": "2 hours 15 minutes",
      "mac": "70:f7:54:cb:7a:93"
    },
    {
      "device_name": "Relay1",
      "status": "offline",
      "last_heartbeat": "2023-12-01 10:30:00",
      "uptime": "1 hour 45 minutes",
      "mac": "70:f7:54:cb:7a:94"
    }
  ]
}
```

### Device Control (Direct)

#### POST /api/control/{device_name}/{pin}
Kontrol device relay secara langsung.

**Parameters:**
- `device_name` (string): Nama device
- `pin` (integer): PIN number (1-8)

**Request Body:**
```json
{
  "action": "on",  // "on", "off", "toggle"
  "value": 1       // 1 = on, 0 = off (optional, auto-set based on action)
}
```

**Response:**
```json
{
  "success": true,
  "message": "Device controlled successfully",
  "device_name": "RelayMini1",
  "pin": 1,
  "action": "on",
  "mqtt_payload": { ... }
}
```

**Examples:**
```bash
# Turn on PIN 1
curl -X POST http://localhost:8000/api/control/RelayMini1/1 \
  -H "Content-Type: application/json" \
  -d '{"action": "on"}'

# Turn off PIN 2
curl -X POST http://localhost:8000/api/control/RelayMini1/2 \
  -H "Content-Type: application/json" \
  -d '{"action": "off"}'

# Toggle PIN 3
curl -X POST http://localhost:8000/api/control/RelayMini1/3 \
  -H "Content-Type: application/json" \
  -d '{"action": "toggle"}'
```

## 📊 Response Codes

### Success Codes
- **200 OK**: Request berhasil diproses
- **201 Created**: Resource berhasil dibuat

### Error Codes
- **400 Bad Request**: Parameter tidak valid
- **404 Not Found**: Resource tidak ditemukan
- **409 Conflict**: Conflict dengan resource existing
- **500 Internal Server Error**: Error server

### Error Response Format
```json
{
  "success": false,
  "error": "Error description",
  "code": 400,
  "timestamp": "2023-12-01 10:35:00"
}
```

## 🔄 Rate Limiting

- **Default**: 100 requests per minute per IP
- **Voice Control**: 10 requests per minute (untuk mencegah spam)
- **Device Control**: 30 requests per minute per device

## 📝 Data Models

### Configuration Object
```json
{
  "id": "string (UUID)",
  "device_name": "string",
  "object_name": "string",
  "description": "string (optional)",
  "part_number": "string",
  "pin": "integer (1-8)",
  "address": "integer",
  "device_bus": "integer",
  "mac": "string (MAC address)"
}
```

### Device Object
```json
{
  "device_name": "string",
  "part_number": "string",
  "mac": "string",
  "status": "online|offline|unknown",
  "last_seen": "datetime string",
  "address": "integer",
  "device_bus": "integer",
  "available_pins": "array of integers"
}
```

### MQTT Payload
```json
{
  "mac": "string",
  "protocol_type": "Modular",
  "device": "string",
  "function": "write",
  "value": {
    "pin": "integer",
    "data": "integer (0|1)"
  },
  "address": "integer",
  "device_bus": "integer",
  "Timestamp": "datetime string"
}
```

## 🧪 Testing API

### Using cURL

```bash
# Get all configurations
curl http://localhost:8000/api/configurations

# Create new configuration
curl -X POST http://localhost:8000/api/configurations \
  -H "Content-Type: application/json" \
  -d '{
    "device_name": "RelayMini1",
    "object_name": "lampu utama",
    "pin": 1
  }'

# Test voice command
curl -X POST http://localhost:8000/api/voice/test \
  -H "Content-Type: application/json" \
  -d '{"command": "nyalakan lampu utama"}'

# Check system status
curl http://localhost:8000/api/status
```

### Using Python

```python
import requests

# Get configurations
response = requests.get('http://localhost:8000/api/configurations')
configs = response.json()

# Create configuration
new_config = {
    "device_name": "RelayMini1",
    "object_name": "lampu utama",
    "pin": 1
}
response = requests.post('http://localhost:8000/api/configurations', json=new_config)

# Test voice command
test_data = {"command": "nyalakan lampu utama"}
response = requests.post('http://localhost:8000/api/voice/test', json=test_data)
```

### Using JavaScript (Browser)

```javascript
// Get configurations
fetch('/api/configurations')
  .then(response => response.json())
  .then(data => console.log(data));

// Create configuration
fetch('/api/configurations', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    device_name: 'RelayMini1',
    object_name: 'lampu utama',
    pin: 1
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## 🔧 WebSocket Support (Future)

API ini akan mendukung WebSocket untuk real-time updates:
- Device status changes
- Voice command recognition
- System events
- Live logs streaming

## 📚 SDK & Libraries

### Python SDK (Planned)
```python
from voice_control_sdk import VoiceControlClient

client = VoiceControlClient('http://localhost:8000')

# Get configurations
configs = client.get_configurations()

# Control device
client.control_device('RelayMini1', 1, 'on')

# Test voice command
result = client.test_voice_command('nyalakan lampu utama')
```

### JavaScript SDK (Planned)
```javascript
import { VoiceControlAPI } from 'voice-control-sdk';

const api = new VoiceControlAPI('http://localhost:8000');

// Real-time updates
api.on('device_status', (device) => {
  console.log('Device status changed:', device);
});

// Control device
await api.controlDevice('RelayMini1', 1, 'on');
```

## 🔒 Security Considerations

### Production Deployment
1. **Enable HTTPS** untuk encrypted communication
2. **Implement authentication** (API keys, JWT)
3. **Add rate limiting** untuk prevent abuse
4. **Validate input** secara ketat
5. **Monitor logs** untuk suspicious activity

### Input Validation
- Device names: alphanumeric + underscore/hyphen
- Object names: letters, spaces, numbers (max 50 chars)
- PIN numbers: 1-8 only
- Commands: predefined whitelist only

## 📞 Support

Untuk pertanyaan API:
- Check response error messages
- Review application logs
- Test with simple requests first
- Use API testing tools (Postman, Insomnia)

---

**API Version**: 1.0.0
**Last Updated**: December 2023
