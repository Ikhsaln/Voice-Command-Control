"""
Automation Voice Service
Manages voice control configurations for relay devices via MQTT.
"""

import json
import uuid
import os
import threading
import time
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, List

from middleware.mqtt_handler import MQTTHandler
from middleware.logging import setup_logging, log_simple
from middleware.network_utils import get_active_mac_address

class AutomationVoice:
    def __init__(self, config_file="JSON/automationVoiceConfig.json"):
        self.config_file = config_file
        self.mqtt = MQTTHandler(client_id="automation_voice")
        self.logger = setup_logging()
        self.ensure_config_file()
        self.device_status = {}  # Cache for device status
        self.status_monitor_thread = None
        self.monitoring_active = False

        # Setup MQTT message handler
        self.mqtt.client.on_message = self.on_mqtt_message

    def ensure_config_file(self):
        """Ensure configuration file exists"""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        if not os.path.exists(self.config_file):
            with open(self.config_file, 'w') as f:
                json.dump([], f, indent=2)

    def load_config(self):
        """Load configuration from file"""
        try:
            with open(self.config_file, 'r') as f:
                data = json.load(f)
                # Ensure it's a list, convert old format if needed
                if isinstance(data, dict) and "configurations" in data:
                    return data["configurations"]
                elif isinstance(data, list):
                    return data
                else:
                    return []
        except (FileNotFoundError, json.JSONDecodeError) as e:
            log_simple(f"Error loading config: {e}", "ERROR")
            return []

    def save_config(self, config):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            log_simple(f"Error saving config: {e}", "ERROR")
            return False

    def create_configuration(self, data):
        """Create new configuration"""
        config = self.load_config()

        # Generate unique ID
        new_id = str(uuid.uuid4())

        # Get MAC address
        mac = get_active_mac_address()

        # Create configuration entry
        current_time = datetime.now(timezone.utc)
        entry = {
            "id": new_id,
            "desc": data.get("desc", ""),
            "object_name": data.get("object_name", ""),
            "device_name": data.get("device_name", ""),
            "part_number": data.get("part_number", ""),
            "pin": int(data.get("pin", "1").replace("PIN", "")),
            "address": int(data.get("address", 0)),
            "device_bus": int(data.get("bus", 0)),
            "mac": mac,
            "created_at": current_time.isoformat() + "Z",
            "updated_at": current_time.isoformat() + "Z"
        }

        config.append(entry)

        if self.save_config(config):
            log_simple(f"Created configuration with ID: {new_id}", "SUCCESS")
            return {"status": "success", "id": new_id, "data": entry}
        else:
            return {"status": "error", "message": "Failed to save configuration"}

    def read_configurations(self, filters=None):
        """Read configurations with optional filters"""
        configurations = self.load_config()

        if filters:
            # Apply filters if provided
            filtered = []
            for conf in configurations:
                match = True
                for key, value in filters.items():
                    if key in conf and str(conf[key]).lower() != str(value).lower():
                        match = False
                        break
                if match:
                    filtered.append(conf)
            configurations = filtered

        return {"status": "success", "data": configurations}

    def update_configuration(self, config_id, data):
        """Update existing configuration"""
        configurations = self.load_config()

        for i, conf in enumerate(configurations):
            if conf["id"] == config_id:
                # Update fields
                for key, value in data.items():
                    if key in ["device_name", "desc", "object_name", "pin", "address", "bus", "part_number", "mac"]:
                        if key == "object_name":
                            conf["object_name"] = value
                        else:
                            conf[key] = value

                # Update timestamp
                current_time = datetime.now(timezone.utc)
                conf['updated_at'] = current_time.isoformat() + "Z"

                if self.save_config(configurations):
                    log_simple(f"Updated configuration with ID: {config_id}", "SUCCESS")
                    return {"status": "success", "id": config_id, "data": conf}
                else:
                    return {"status": "error", "message": "Failed to save configuration"}

        return {"status": "error", "message": "Configuration not found"}

    def delete_configuration(self, config_id):
        """Delete configuration"""
        configurations = self.load_config()

        for i, conf in enumerate(configurations):
            if conf["id"] == config_id:
                deleted = configurations.pop(i)
                if self.save_config(configurations):
                    log_simple(f"Deleted configuration with ID: {config_id}", "SUCCESS")
                    return {"status": "success", "id": config_id, "data": deleted}
                else:
                    return {"status": "error", "message": "Failed to save configuration"}

        return {"status": "error", "message": "Configuration not found"}

    def update_device_status(self, mac_address, status, last_seen=None):
        """Update device status in configuration"""
        try:
            configurations = self.load_config()
            updated = False
            current_time = datetime.now(timezone.utc)

            for config in configurations:
                if config.get('mac') == mac_address:
                    config['status'] = status
                    if last_seen:
                        config['last_seen'] = last_seen
                    else:
                        config['last_seen'] = current_time.isoformat() + "Z"
                    config['updated_at'] = current_time.isoformat() + "Z"
                    updated = True
                    log_simple(f"Updated status for device {mac_address}: {status}", "INFO")

            if updated:
                self.save_config(configurations)
                # Update cache
                self.device_status[mac_address] = {
                    'status': status,
                    'last_seen': last_seen or (current_time.isoformat() + "Z")
                }

            return updated
        except Exception as e:
            log_simple(f"Error updating device status: {e}", "ERROR")
            return False

    def get_device_status(self, mac_address):
        """Get current device status"""
        # Check cache first
        if mac_address in self.device_status:
            return self.device_status[mac_address]

        # Check configuration file
        configurations = self.load_config()
        for config in configurations:
            if config.get('mac') == mac_address:
                return {
                    'status': config.get('status', 'unknown'),
                    'last_seen': config.get('last_seen', None)
                }

        return {'status': 'unknown', 'last_seen': None}

    def check_device_timeout(self):
        """Check for devices that haven't sent heartbeat recently"""
        try:
            configurations = self.load_config()
            current_time = datetime.now(timezone.utc)
            updated = False

            for config in configurations:
                last_seen_str = config.get('last_seen')
                heartbeat_interval = config.get('heartbeat_interval', 30)

                if last_seen_str and config.get('status') == 'online':
                    try:
                        last_seen = datetime.fromisoformat(last_seen_str.replace('Z', '+00:00'))
                        time_diff = (current_time - last_seen).total_seconds()

                        # If no heartbeat for 2x interval + 10 seconds, mark as offline
                        if time_diff > (heartbeat_interval * 2) + 10:
                            config['status'] = 'offline'
                            config['updated_at'] = current_time.isoformat() + "Z"
                            updated = True
                            log_simple(f"Device {config.get('mac')} marked offline due to timeout", "WARNING")
                    except ValueError as e:
                        log_simple(f"Invalid last_seen format for device {config.get('mac')}: {e}", "ERROR")

            if updated:
                self.save_config(configurations)

        except Exception as e:
            log_simple(f"Error checking device timeout: {e}", "ERROR")

    def start_status_monitoring(self):
        """Start device status monitoring thread"""
        if self.monitoring_active:
            return

        self.monitoring_active = True
        self.status_monitor_thread = threading.Thread(target=self._status_monitor_loop, daemon=True)
        self.status_monitor_thread.start()
        log_simple("Device status monitoring started", "INFO")

    def stop_status_monitoring(self):
        """Stop device status monitoring"""
        self.monitoring_active = False
        if self.status_monitor_thread:
            self.status_monitor_thread.join(timeout=5)
        log_simple("Device status monitoring stopped", "INFO")

    def _status_monitor_loop(self):
        """Background thread for monitoring device status"""
        while self.monitoring_active:
            try:
                self.check_device_timeout()
                time.sleep(10)  # Check every 10 seconds
            except Exception as e:
                log_simple(f"Error in status monitor loop: {e}", "ERROR")
                time.sleep(5)

    def discover_devices(self):
        """Send device discovery request via MQTT"""
        try:
            current_time = datetime.now(timezone.utc)
            discovery_payload = {
                "request": "all",
                "timestamp": current_time.isoformat() + "Z"
            }
            success = self.mqtt.publish("device/discovery", discovery_payload)
            if success:
                log_simple("Device discovery request sent", "INFO")
            else:
                log_simple("Failed to send device discovery request", "ERROR")
            return success
        except Exception as e:
            log_simple(f"Error sending device discovery: {e}", "ERROR")
            return False

    def on_mqtt_message(self, client, userdata, msg):
        """Handle incoming MQTT messages"""
        try:
            topic = msg.topic
            payload = json.loads(msg.payload.decode())

            log_simple(f"Received MQTT message on topic: {topic}", "INFO")

            # Handle device heartbeat
            if topic.startswith("device/heartbeat/"):
                mac_address = topic.split("/")[-1]
                last_seen = payload.get("timestamp", datetime.now(timezone.utc).isoformat() + "Z")
                self.update_device_status(mac_address, "online", last_seen)
                return

            # Handle device announcements (discovery responses)
            elif topic.startswith("device/announce/"):
                mac_address = topic.split("/")[-1]
                self.update_device_status(mac_address, "online")
                log_simple(f"Device announced: {mac_address}", "INFO")
                return

            # Handle device status updates
            elif topic.startswith("device/status/"):
                mac_address = topic.split("/")[-1]
                status = payload.get("status", "unknown")
                last_seen = payload.get("timestamp")
                self.update_device_status(mac_address, status, last_seen)
                return

            response_topic = "response/automation_voice/result"
            response = {}

            if topic == "command/automation_voice/create":
                response = self.create_configuration(payload)
            elif topic == "command/automation_voice/read":
                filters = payload.get("filters", None)
                response = self.read_configurations(filters)
            elif topic == "command/automation_voice/update":
                config_id = payload.get("id")
                data = payload.get("data", {})
                if config_id:
                    response = self.update_configuration(config_id, data)
                else:
                    response = {"status": "error", "message": "ID required for update"}
            elif topic == "command/automation_voice/delete":
                config_id = payload.get("id")
                if config_id:
                    response = self.delete_configuration(config_id)
                else:
                    response = {"status": "error", "message": "ID required for delete"}
            else:
                response = {"status": "error", "message": "Unknown command"}

            # Publish response
            self.mqtt.publish(response_topic, response)

        except json.JSONDecodeError:
            log_simple("Invalid JSON payload received", "ERROR")
            error_response = {"status": "error", "message": "Invalid JSON payload"}
            self.mqtt.publish("response/automation_voice/result", error_response)
        except Exception as e:
            log_simple(f"Error processing MQTT message: {e}", "ERROR")
            error_response = {"status": "error", "message": str(e)}
            self.mqtt.publish("response/automation_voice/result", error_response)

    def start(self):
        """Start the automation voice service"""
        log_simple("Starting Automation Voice service", "INFO")

        # Connect to MQTT
        if not self.mqtt.connect():
            log_simple("Failed to connect to MQTT broker", "ERROR")
            return False

        # Subscribe to command topics
        topics = [
            "command/automation_voice/create",
            "command/automation_voice/read",
            "command/automation_voice/update",
            "command/automation_voice/delete",
            # Device status topics
            "device/heartbeat/+",  # Heartbeat from devices
            "device/announce/+",   # Device announcements
            "device/status/+",     # Device status updates
            "device/discovery"     # Discovery requests
        ]

        for topic in topics:
            self.mqtt.subscribe(topic)

        # Start device status monitoring
        self.start_status_monitoring()

        log_simple("Automation Voice service started successfully", "SUCCESS")
        return True

    def stop(self):
        """Stop the automation voice service"""
        log_simple("Stopping Automation Voice service", "INFO")
        self.stop_status_monitoring()
        self.mqtt.disconnect()
        log_simple("Automation Voice service stopped", "SUCCESS")

if __name__ == "__main__":
    # Example usage
    automation = AutomationVoice()

    if automation.start():
        try:
            # Keep running
            while True:
                pass
        except KeyboardInterrupt:
            automation.stop()
    else:
        log_simple("Failed to start Automation Voice service", "ERROR")
