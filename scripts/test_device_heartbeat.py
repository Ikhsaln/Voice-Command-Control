#!/usr/bin/env python3
"""
Test script to simulate device heartbeats for testing device status monitoring.
This script simulates devices sending periodic heartbeats via MQTT.
"""

import json
import time
import threading
from datetime import datetime

from middleware.mqtt_handler import MQTTHandler
from middleware.logging import setup_logging, log_simple

class DeviceHeartbeatSimulator:
    def __init__(self):
        self.mqtt = MQTTHandler(client_id="device_simulator")
        self.devices = [
            {
                "mac": "70:f7:54:cb:7a:93",
                "name": "RelayMini1",
                "part_number": "RELAYMINI",
                "heartbeat_interval": 30
            },
            {
                "mac": "70:f7:54:cb:7a:94",
                "name": "Relay1",
                "part_number": "RELAY",
                "heartbeat_interval": 30
            }
        ]
        self.running = False
        self.threads = []

    def send_heartbeat(self, device):
        """Send heartbeat for a specific device"""
        while self.running:
            try:
                heartbeat_payload = {
                    "timestamp": datetime.now().isoformat() + "Z",
                    "device_name": device["name"],
                    "part_number": device["part_number"],
                    "status": "online"
                }

                topic = f"device/heartbeat/{device['mac']}"
                success = self.mqtt.publish(topic, heartbeat_payload)

                if success:
                    log_simple(f"Sent heartbeat for {device['name']} ({device['mac']})", "INFO")
                else:
                    log_simple(f"Failed to send heartbeat for {device['name']}", "ERROR")

            except Exception as e:
                log_simple(f"Error sending heartbeat for {device['name']}: {e}", "ERROR")

            # Wait for next heartbeat interval
            time.sleep(device["heartbeat_interval"])

    def send_device_announcement(self, device):
        """Send device announcement"""
        try:
            announcement_payload = {
                "name": device["name"],
                "part_number": device["part_number"],
                "mac": device["mac"],
                "timestamp": datetime.now().isoformat() + "Z",
                "status": "online"
            }

            topic = f"device/announce/{device['mac']}"
            success = self.mqtt.publish(topic, announcement_payload)

            if success:
                log_simple(f"Sent announcement for {device['name']} ({device['mac']})", "INFO")
            else:
                log_simple(f"Failed to send announcement for {device['name']}", "ERROR")

        except Exception as e:
            log_simple(f"Error sending announcement for {device['name']}: {e}", "ERROR")

    def start_simulation(self):
        """Start the device heartbeat simulation"""
        log_simple("Starting device heartbeat simulation", "INFO")

        if not self.mqtt.connect():
            log_simple("Failed to connect to MQTT broker", "ERROR")
            return False

        self.running = True

        # Send initial announcements
        for device in self.devices:
            self.send_device_announcement(device)
            time.sleep(1)  # Small delay between announcements

        # Start heartbeat threads
        for device in self.devices:
            thread = threading.Thread(target=self.send_heartbeat, args=(device,), daemon=True)
            thread.start()
            self.threads.append(thread)

        log_simple(f"Device simulation started for {len(self.devices)} devices", "SUCCESS")
        log_simple("Devices will send heartbeats every 30 seconds", "INFO")
        return True

    def stop_simulation(self):
        """Stop the device heartbeat simulation"""
        log_simple("Stopping device heartbeat simulation", "INFO")
        self.running = False

        # Wait for threads to finish
        for thread in self.threads:
            thread.join(timeout=5)

        self.mqtt.disconnect()
        log_simple("Device heartbeat simulation stopped", "SUCCESS")

def main():
    """Main function"""
    simulator = DeviceHeartbeatSimulator()

    try:
        if simulator.start_simulation():
            log_simple("Press Ctrl+C to stop simulation", "INFO")

            # Keep running
            while True:
                time.sleep(1)

    except KeyboardInterrupt:
        simulator.stop_simulation()
    except Exception as e:
        log_simple(f"Error in simulation: {e}", "ERROR")
        simulator.stop_simulation()

if __name__ == "__main__":
    main()
