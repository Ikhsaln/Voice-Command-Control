# 🔧 Troubleshooting Guide - Voice Control Relay System

Panduan lengkap untuk mengatasi masalah umum pada sistem voice control relay.

## 🚨 Quick Diagnosis

### Step 1: Check System Status
```bash
# Check if application is running
curl http://localhost:8000/api/status

# Check MQTT connection
curl http://localhost:8000/api/status/mqtt

# Check voice control status
curl http://localhost:8000/api/voice/status
```

### Step 2: Review Logs
```bash
# View recent logs
tail -50 logs/voice_relay_$(date +%Y%m%d).log

# Search for errors
grep "ERROR" logs/voice_relay_$(date +%Y%m%d).log

# Search for specific issues
grep "microphone\|MQTT\|voice" logs/voice_relay_$(date +%Y%m%d).log
```

### Step 3: Test Components
```bash
# Test microphone
python -c "
import speech_recognition as sr
r = sr.Recognizer()
with sr.Microphone() as source:
    print('Microphone OK')
"

# Test MQTT
python -c "
import paho.mqtt.client as mqtt
client = mqtt.Client()
try:
    client.connect('localhost', 1883, 5)
    print('MQTT OK')
except:
    print('MQTT Failed')
"
```

## 🎙️ Microphone Issues

### Problem: "No microphone found" / "Audio device not available"

**Symptoms:**
- Voice control fails to start
- Error: "OSError: No Default Input Device Available"
- Logs show: "No audio device available"

**Solutions:**

#### 1. Check System Permissions (macOS)
```bash
# Check microphone permissions
# System Settings → Privacy & Security → Microphone
# Ensure Terminal and Python are checked
```

#### 2. Test Audio Devices
```bash
# List available microphones
python -c "
import speech_recognition as sr
mics = sr.Microphone.list_microphone_names()
for i, name in enumerate(mics):
    print(f'{i}: {name}')
"

# Test specific microphone
python -c "
import speech_recognition as sr
r = sr.Recognizer()
with sr.Microphone(device_index=0) as source:  # Try different indices
    print('Testing microphone...')
    audio = r.listen(source, timeout=3)
    print('Microphone working!')
"
```

#### 3. Audio Settings (macOS)
- Go to **System Settings → Sound → Input**
- Select your microphone
- Adjust **Input volume** to 70-80%
- Test with **Voice Memos** app

#### 4. Hardware Solutions
- Try different USB port
- Use powered USB hub if microphone needs more power
- Test with different microphone
- Check microphone cable/connection

### Problem: "Could not understand audio" / Poor recognition

**Symptoms:**
- Speech detected but not understood
- Commands work sometimes, fail others
- Background noise affects recognition

**Solutions:**

#### 1. Environment Optimization
- **Reduce background noise** (close windows, turn off fans)
- **Speak closer** to microphone (15-30 cm)
- **Speak clearly** and at normal volume
- **Test in quiet room**

#### 2. Microphone Quality
```bash
# Test with different microphones
# Recommended: USB condenser microphone
# Avoid: Built-in laptop mic for production use
```

#### 3. Speech Recognition Settings
```python
# Adjust in voice_control.py
recognizer.energy_threshold = 200  # Lower = more sensitive
recognizer.pause_threshold = 1.0   # Longer pause detection
recognizer.dynamic_energy_threshold = True
```

#### 4. Network Check
```bash
# Test internet connection (Google API needs internet)
ping -c 3 google.com

# Check DNS resolution
nslookup speech.googleapis.com
```

### Problem: Voice commands work in test but not live

**Symptoms:**
- Test command works perfectly
- Live voice recognition fails
- Logs show successful parsing but execution fails

**Solutions:**

#### 1. Check MQTT Connection
```bash
# Test MQTT broker
mosquitto_pub -h localhost -t test -m "hello"

# Check broker status
netstat -an | grep 1883
```

#### 2. Verify Device Configuration
```bash
# Check configurations
curl http://localhost:8000/api/configurations

# Verify device connectivity
curl http://localhost:8000/api/devices
```

#### 3. Test Device Control Directly
```bash
# Control device via API
curl -X POST http://localhost:8000/api/control/RelayMini1/1 \
  -H "Content-Type: application/json" \
  -d '{"action": "on"}'
```

## 🔗 MQTT Connection Issues

### Problem: "MQTT connection failed" / "Broker not reachable"

**Symptoms:**
- Device control doesn't work
- Status shows "MQTT disconnected"
- Logs show connection errors

**Solutions:**

#### 1. Start MQTT Broker
```bash
# macOS with Homebrew
brew services start mosquitto

# Or run manually
/usr/local/sbin/mosquitto -c /usr/local/etc/mosquitto/mosquitto.conf

# Check if running
ps aux | grep mosquitto
```

#### 2. Check Broker Configuration
```bash
# Test connection
mosquitto_pub -h localhost -t test -m "test message"

# Check broker logs
tail -f /usr/local/var/log/mosquitto/mosquitto.log
```

#### 3. Firewall Issues
```bash
# Check if port 1883 is open
netstat -an | grep 1883

# macOS firewall
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --listapps
```

#### 4. Network Configuration
```bash
# If using remote broker
ping your-mqtt-broker.com

# Test specific port
telnet your-mqtt-broker.com 1883
```

### Problem: MQTT connects but device doesn't respond

**Symptoms:**
- MQTT status "connected"
- Voice commands processed
- Device doesn't physically respond

**Solutions:**

#### 1. Check Device Power
- Ensure device is powered on
- Check power supply voltage
- Verify device indicators (LEDs)

#### 2. Verify Device Configuration
```json
// Check JSON/automationVoiceConfig.json
{
  "device_name": "RelayMini1",  // Must match MQTT topic
  "mac": "70:f7:54:cb:7a:93",   // Must match device MAC
  "pin": 1,                     // Must be available PIN
  "address": 37,                // Must match device address
  "device_bus": 0               // Must match device bus
}
```

#### 3. Test MQTT Payload
```bash
# Send test MQTT message
mosquitto_pub -h localhost -t modular -m '{
  "mac": "70:f7:54:cb:7a:93",
  "protocol_type": "Modular",
  "device": "RELAYMINI",
  "function": "write",
  "value": {"pin": 1, "data": 1},
  "address": 37,
  "device_bus": 0,
  "Timestamp": "'$(date +%Y-%m-%d\ %H:%M:%S)'"
}'
```

#### 4. Check Device Logs
- Access device web interface (if available)
- Check device MQTT subscription
- Verify device firmware version

## ⚙️ Configuration Issues

### Problem: "Configuration not found" / "Object name not recognized"

**Symptoms:**
- Voice command recognized but object not found
- "No configuration found for object" error

**Solutions:**

#### 1. Check Configuration File
```bash
# View current configurations
cat JSON/automationVoiceConfig.json | jq '.'

# Validate JSON syntax
python -c "
import json
with open('JSON/automationVoiceConfig.json') as f:
    data = json.load(f)
    print('JSON is valid')
"
```

#### 2. Verify Object Names
```bash
# List all configured objects
curl http://localhost:8000/api/configurations | jq '.[].object_name'

# Test object matching
python -c "
from voice_control import VoiceControl
vc = VoiceControl()
configs = vc.load_configurations()
for config in configs:
    print(f'Object: {config.get(\"object_name\")}')
"
```

#### 3. Fix Naming Issues
- Ensure object names are unique
- Use consistent naming (lowercase, no special chars)
- Avoid ambiguous names ("lamp", "light" vs "main lamp")

### Problem: PIN conflicts / "PIN already in use"

**Symptoms:**
- Cannot create new configuration
- Error: "PIN X is already in use"

**Solutions:**

#### 1. Check PIN Usage
```bash
# View PIN usage per device
curl http://localhost:8000/api/configurations | jq 'group_by(.device_name) | map({device: .[0].device_name, pins: map(.pin)})'

# Available PINs for RELAYMINI: 1-6
# Available PINs for RELAY: 1-8
```

#### 2. Free Up PINs
```bash
# Delete unused configurations
curl -X DELETE http://localhost:8000/api/configurations/CONFIG_ID

# Or reassign PINs
curl -X PUT http://localhost:8000/api/configurations/CONFIG_ID \
  -H "Content-Type: application/json" \
  -d '{"pin": 2}'
```

## 🌐 Web Interface Issues

### Problem: Cannot access web interface

**Symptoms:**
- Browser shows connection refused
- Port 8000 not accessible

**Solutions:**

#### 1. Check Application Status
```bash
# Check if app is running
ps aux | grep python | grep app.py

# Check port usage
netstat -an | grep 8000
```

#### 2. Start Application
```bash
# Start application
python app.py

# Or with specific host/port
FLASK_HOST=0.0.0.0 FLASK_PORT=8000 python app.py
```

#### 3. Firewall Issues
```bash
# macOS: Allow incoming connections
# System Settings → Firewall → Turn off temporarily for testing
```

#### 4. Network Access
```bash
# Find your IP address
ifconfig | grep inet

# Access from other devices
http://YOUR_IP:8000
```

### Problem: Web interface loads but buttons don't work

**Symptoms:**
- Page loads but JavaScript errors
- Buttons unresponsive
- Console shows errors

**Solutions:**

#### 1. Check Browser Console
- Open Developer Tools (F12)
- Check Console tab for JavaScript errors
- Check Network tab for failed requests

#### 2. Clear Browser Cache
- Hard refresh: Cmd+Shift+R (macOS)
- Clear browser cache and cookies

#### 3. Test API Directly
```bash
# Test API endpoints
curl http://localhost:8000/api/status
curl http://localhost:8000/api/configurations
```

## 🔄 Device Discovery Issues

### Problem: Device discovery finds nothing

**Symptoms:**
- "Discover Devices" button doesn't find devices
- No devices in dropdown

**Solutions:**

#### 1. Check Network
```bash
# Ensure devices are on same network
arp -a  # List network devices

# Check device IP addresses
# Access device web interface to verify network settings
```

#### 2. MQTT Topics
```bash
# Subscribe to device topics
mosquitto_sub -h localhost -t "device/#"

# Check if devices are publishing
mosquitto_sub -h localhost -t "heartbeat/#"
```

#### 3. Device Configuration
- Ensure devices are configured for MQTT
- Check device MQTT broker settings
- Verify device firmware supports discovery

## 📊 Performance Issues

### Problem: System slow / high CPU usage

**Symptoms:**
- Voice recognition delayed
- Web interface slow
- High CPU usage

**Solutions:**

#### 1. Optimize Settings
```python
# In voice_control.py
recognizer.energy_threshold = 300  # Higher = less sensitive
recognizer.pause_threshold = 0.8   # Shorter = faster
```

#### 2. Resource Monitoring
```bash
# Check CPU usage
top -pid $(pgrep -f app.py)

# Check memory usage
ps aux | grep python
```

#### 3. Database Optimization
- JSON file suitable for <100 configurations
- For larger setups, consider SQLite database
- Implement caching for frequent queries

### Problem: Memory leaks / application crashes

**Symptoms:**
- Application crashes after hours of use
- Memory usage keeps increasing

**Solutions:**

#### 1. Update Dependencies
```bash
pip install --upgrade speechrecognition paho-mqtt flask
```

#### 2. Code Review
- Check for unclosed connections
- Verify proper exception handling
- Monitor thread usage

#### 3. Restart Policy
```bash
# Use process manager
pip install gunicorn
gunicorn -w 2 -b 0.0.0.0:8000 app:app --reload
```

## 🔧 Advanced Debugging

### Debug Mode
```bash
# Run with debug logging
FLASK_DEBUG=True python app.py

# Or set log level
LOG_LEVEL=DEBUG python app.py
```

### MQTT Debugging
```bash
# Monitor all MQTT traffic
mosquitto_sub -h localhost -t "#" -v

# Debug specific topics
mosquitto_sub -h localhost -t "modular" -v
mosquitto_sub -h localhost -t "heartbeat/#" -v
```

### Network Debugging
```bash
# Packet capture (requires tcpdump)
sudo tcpdump -i any port 1883 -w mqtt_traffic.pcap

# DNS resolution
dig speech.googleapis.com
```

### Performance Profiling
```python
# Add to app.py for profiling
from werkzeug.middleware.profiler import ProfilerMiddleware
app.wsgi_app = ProfilerMiddleware(app.wsgi_app, profile_dir='./profiles')
```

## 📞 Getting Help

### Support Checklist
- [ ] Include full error messages
- [ ] Attach relevant log files
- [ ] Describe steps to reproduce
- [ ] Include system information
- [ ] List recent changes made

### System Information
```bash
# Gather system info
python -c "
import platform, sys
print('OS:', platform.system(), platform.release())
print('Python:', sys.version)
print('Architecture:', platform.machine())
"

# List installed packages
pip list | grep -E "(flask|speech|paho|pyaudio)"
```

### Common Log Locations
- Application logs: `logs/voice_relay_YYYYMMDD.log`
- MQTT logs: `/usr/local/var/log/mosquitto/mosquitto.log`
- System logs: `/var/log/system.log` (macOS)

## 🚑 Emergency Recovery

### Complete Reset
```bash
# Stop application
pkill -f app.py

# Backup configurations
cp JSON/automationVoiceConfig.json backup/

# Reset to defaults
rm JSON/automationVoiceConfig.json
touch JSON/automationVoiceConfig.json
echo "[]" > JSON/automationVoiceConfig.json

# Restart application
python app.py
```

### Factory Reset Device
- Unplug device for 30 seconds
- Press and hold reset button while plugging back in
- Access device web interface for factory reset

---

**Remember**: Most issues can be resolved by checking logs, testing components individually, and verifying configurations. Start with simple tests and work your way up to complex scenarios.
