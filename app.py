"""
Flask Web Application for Voice Relay Control
Provides REST API endpoints for managing voice-controlled relay devices.
"""

from flask import Flask, render_template, request, jsonify
import json
import uuid
import os
import threading

from middleware.mqtt_handler import MQTTHandler
from middleware.logging import setup_logging, log_simple
from middleware.network_utils import get_active_mac_address
from AutomationVoice import AutomationVoice
from voice_control import VoiceControl

app = Flask(__name__)
logger = setup_logging()

# Global variables for service management
mqtt_client = None
automation_voice = None
available_devices = [
    # Sample devices for testing
    {
        "name": "RelayMini1",
        "part_number": "RELAYMINI",
        "address": 37,
        "device_bus": 0,
        "mac": "70:f7:54:cb:7a:93"
    },
    {
        "name": "Relay1",
        "part_number": "RELAY",
        "address": 38,
        "device_bus": 0,
        "mac": "70:f7:54:cb:7a:94"
    }
]
voice_control = None
voice_thread = None

def init_mqtt():
    """Initialize MQTT client"""
    global mqtt_client
    mqtt_client = MQTTHandler(client_id="automation_voice_frontend")

    # Setup message handler
    mqtt_client.client.on_message = on_mqtt_message

    if mqtt_client.connect():
        # Subscribe to available devices topic
        mqtt_client.subscribe("MODULAR_DEVICE/AVAILABLES")
        log_simple("Frontend MQTT client connected and subscribed", "SUCCESS")
        return True
    else:
        log_simple("Failed to connect frontend MQTT client", "ERROR")
        return False

def on_mqtt_message(client, userdata, msg):
    """Handle incoming MQTT messages"""
    global available_devices
    try:
        topic = msg.topic
        payload = json.loads(msg.payload.decode())

        if topic == "MODULAR_DEVICE/AVAILABLES":
            # Filter devices with part_number RELAYMINI or RELAY
            filtered_devices = [
                device for device in payload
                if device.get('part_number', '').upper() in ['RELAYMINI', 'RELAY']
            ]
            available_devices = filtered_devices
            log_simple(f"Updated available devices: {len(filtered_devices)} devices", "INFO")

    except Exception as e:
        log_simple(f"Error processing MQTT message: {e}", "ERROR")

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/devices/available')
def get_available_devices():
    """Get available devices for dropdown"""
    return jsonify({
        'status': 'success',
        'devices': available_devices
    })

@app.route('/api/configurations', methods=['GET'])
def get_configurations():
    """Get all configurations"""
    try:
        with open('JSON/automationVoiceConfig.json', 'r') as f:
            data = json.load(f)
        # Handle both old format (with configurations key) and new format (direct array)
        if isinstance(data, dict) and 'configurations' in data:
            configurations = data['configurations']
        elif isinstance(data, list):
            configurations = data
        else:
            configurations = []
        return jsonify({
            'status': 'success',
            'data': configurations
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/api/configurations', methods=['POST'])
def create_configuration():
    """Create new configuration"""
    try:
        data = request.get_json()

        # Find selected device
        device_name = data.get('device_name')
        selected_device = None
        for device in available_devices:
            if device.get('name') == device_name:
                selected_device = device
                break

        if not selected_device:
            return jsonify({
                'status': 'error',
                'message': 'Device not found'
            })

        # Prepare configuration data
        config_data = {
            'device_name': device_name,
            'desc': data.get('desc', ''),
            'object_name': data.get('objectName', ''),  # This is correct
            'pin': data.get('pin', ''),
            'address': str(selected_device.get('address', '0')),
            'bus': str(selected_device.get('device_bus', '0')),
            'part_number': selected_device.get('part_number', ''),
            'mac': selected_device.get('mac', '00:00:00:00:00:00')
        }

        # Use AutomationVoice to create
        if automation_voice:
            result = automation_voice.create_configuration(config_data)
            return jsonify(result)
        else:
            return jsonify({
                'status': 'error',
                'message': 'AutomationVoice service not available'
            })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/api/configurations/<config_id>', methods=['PUT'])
def update_configuration(config_id):
    """Update configuration"""
    try:
        data = request.get_json()

        update_data = {
            'device_name': data.get('device_name'),
            'desc': data.get('desc'),
            'object_name': data.get('objectName', ''),
            'pin': data.get('pin')
        }

        if automation_voice:
            result = automation_voice.update_configuration(config_id, update_data)
            return jsonify(result)
        else:
            return jsonify({
                'status': 'error',
                'message': 'AutomationVoice service not available'
            })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/api/configurations/<config_id>', methods=['DELETE'])
def delete_configuration(config_id):
    """Delete configuration"""
    try:
        if automation_voice:
            result = automation_voice.delete_configuration(config_id)
            return jsonify(result)
        else:
            return jsonify({
                'status': 'error',
                'message': 'AutomationVoice service not available'
            })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/api/pins/<part_number>')
def get_pins_for_device(part_number):
    """Get available pins for device type"""
    pins = []
    if part_number.upper() == 'RELAYMINI':
        pins = [f'PIN{i}' for i in range(1, 7)]  # 6 pins
    elif part_number.upper() == 'RELAY':
        pins = [f'PIN{i}' for i in range(1, 9)]  # 8 pins

    return jsonify({
        'status': 'success',
        'pins': pins
    })

@app.route('/api/voice/start', methods=['POST'])
def start_voice_control():
    """Start voice control"""
    global voice_control, voice_thread

    try:
        if voice_control is None:
            voice_control = VoiceControl()

        if voice_control.start_voice_control():
            return jsonify({
                'status': 'success',
                'message': 'Voice control started'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to start voice control'
            })
    except Exception as e:
        log_simple(f"Error starting voice control: {e}", "ERROR")
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/api/voice/stop', methods=['POST'])
def stop_voice_control():
    """Stop voice control"""
    global voice_control

    try:
        if voice_control:
            voice_control.stop_voice_control()
            voice_control = None

        return jsonify({
            'status': 'success',
            'message': 'Voice control stopped'
        })
    except Exception as e:
        log_simple(f"Error stopping voice control: {e}", "ERROR")
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/api/voice/test', methods=['POST'])
def test_voice_command():
    """Test voice command processing"""
    try:
        data = request.get_json()
        command_text = data.get('command', '').strip()

        if not command_text:
            return jsonify({
                'status': 'error',
                'message': 'Command text is required'
            })

        # Create voice control instance if not exists
        global voice_control
        if voice_control is None:
            voice_control = VoiceControl()

        # Test the command
        success = voice_control.test_voice_command(command_text)

        return jsonify({
            'status': 'success' if success else 'warning',
            'message': f'Command processed: {command_text}',
            'success': success
        })

    except Exception as e:
        log_simple(f"Error testing voice command: {e}", "ERROR")
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/api/devices/status/<mac>')
def get_device_status(mac):
    """Get status for a specific device"""
    try:
        if automation_voice:
            status_info = automation_voice.get_device_status(mac)
            return jsonify({
                'status': 'success',
                'device_status': status_info['status'],
                'last_seen': status_info['last_seen']
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'AutomationVoice service not available'
            })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/api/devices/discover', methods=['POST'])
def discover_devices():
    """Trigger device discovery"""
    try:
        if automation_voice:
            success = automation_voice.discover_devices()
            return jsonify({
                'status': 'success' if success else 'error',
                'message': 'Device discovery initiated' if success else 'Failed to initiate discovery'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'AutomationVoice service not available'
            })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/api/status/mqtt')
def get_mqtt_status():
    """Get MQTT connection status"""
    try:
        # Check both MQTT clients
        frontend_connected = mqtt_client.connected if mqtt_client else False
        backend_connected = automation_voice.mqtt.connected if automation_voice and hasattr(automation_voice, 'mqtt') else False

        return jsonify({
            'status': 'success',
            'mqtt_connected': frontend_connected or backend_connected,
            'frontend_connected': frontend_connected,
            'backend_connected': backend_connected
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'mqtt_connected': False
        })

if __name__ == '__main__':
    # Initialize AutomationVoice service
    try:
        automation_voice = AutomationVoice()
        # Start the backend MQTT service
        if automation_voice.start():
            log_simple("AutomationVoice service initialized and started", "SUCCESS")
        else:
            log_simple("AutomationVoice service initialized but MQTT failed", "WARNING")
    except Exception as e:
        log_simple(f"Failed to initialize AutomationVoice: {e}", "ERROR")
        automation_voice = None

    # Initialize MQTT for frontend (optional for testing)
    mqtt_connected = init_mqtt()
    if not mqtt_connected:
        log_simple("MQTT not available, continuing without MQTT features", "WARNING")

    # Use port 8000 by default to avoid conflicts
    port = int(os.environ.get('PORT', 8000))
    host = os.environ.get('FLASK_HOST', '0.0.0.0')  # Bind to all interfaces for network access
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

    if debug_mode:
        log_simple("WARNING: Debug mode enabled - MQTT connections will cycle on file changes", "WARNING")
        log_simple("For production use: export FLASK_DEBUG=False", "INFO")

    log_simple(f"Starting Flask application on {host}:{port} (debug={debug_mode})", "INFO")
    log_simple(f"Access from other devices: http://{get_active_mac_address() or 'your-ip'}:{port}", "INFO")
    app.run(debug=debug_mode, host=host, port=port)
