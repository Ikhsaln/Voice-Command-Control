#!/usr/bin/env python3
"""
Test script to simulate publishing device data to MQTT
"""

import json
import time
from middleware.mqtt_handler import MQTTHandler
from middleware.logging import setup_logging, log_simple

def publish_device_data():
    """Publish sample device data to MQTT"""
    logger = setup_logging()
    mqtt = MQTTHandler(client_id="device_publisher")

    if not mqtt.connect():
        log_simple("Failed to connect to MQTT broker", "ERROR")
        return False

    # Sample device data as provided
    device_data = [
        {
            "id": "",
            "name": "RelayMini1",
            "address": 37,
            "device_bus": 0,
            "part_number": "RELAYMINI",
            "mac": "00:00:00:00:00:00",
            "device_type": "Modular",
            "manufacturer": "IOT",
            "topic": "Limbah/Modular/relay_mini/1"
        },
        {
            "id": "",
            "name": "Drycontact1",
            "address": 35,
            "device_bus": 0,
            "part_number": "DRYCONTACT",
            "mac": "00:00:00:00:00:00",
            "device_type": "Modular",
            "manufacturer": "IOT",
            "topic": "Limbah/Modular/drycontact/1"
        }
    ]

    # Publish to MODULAR_DEVICE/AVAILABLES topic
    log_simple("Publishing device data to MQTT...", "INFO")

    success = mqtt.publish("MODULAR_DEVICE/AVAILABLES", device_data)

    if success:
        log_simple("Device data published successfully", "SUCCESS")
        # Keep connection alive for a moment
        time.sleep(2)
    else:
        log_simple("Failed to publish device data", "ERROR")

    mqtt.disconnect()
    return success

if __name__ == "__main__":
    print("Publishing sample device data to MQTT...")
    success = publish_device_data()
    if success:
        print("✅ Device data published successfully!")
        print("You can now access the frontend at http://localhost:5000")
    else:
        print("❌ Failed to publish device data")
        print("Make sure MQTT broker is running on localhost:1883")
