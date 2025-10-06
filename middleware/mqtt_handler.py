"""
MQTT Handler Module
Provides MQTT client functionality for publishing and subscribing to topics.
"""

import json
import paho.mqtt.client as mqtt
import time
from typing import Optional, Callable, Any

from .logging import log_simple

class MQTTHandler:
    """
    MQTT client handler for voice relay system.
    Manages connection, publishing, and subscribing to MQTT topics.
    """

    def __init__(self, broker: str = "localhost", port: int = 1884, client_id: str = "voice_relay"):
        """
        Initialize MQTT client.

        Args:
            broker: MQTT broker address
            port: MQTT broker port
            client_id: Unique client identifier
        """
        self.broker = broker
        self.port = port
        self.client_id = client_id
        # Use VERSION1 for better compatibility with MQTT X
        self.client = mqtt.Client(client_id=client_id, callback_api_version=mqtt.CallbackAPIVersion.VERSION1)
        self.connected = False

        # Setup callbacks
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            self.connected = True
            log_simple(f"Connected to MQTT broker {self.broker}:{self.port}", "SUCCESS")
        else:
            log_simple(f"Failed to connect to MQTT broker, return code {rc}", "ERROR")

    def on_disconnect(self, client, userdata, rc, properties=None, reasoncodes=None):
        self.connected = False
        log_simple("Disconnected from MQTT broker", "WARNING")

    def on_message(self, client, userdata, msg):
        """Default message handler - can be overridden"""
        log_simple(f"Received message on topic {msg.topic}: {msg.payload.decode()}", "INFO")

    def connect(self):
        """Connect to MQTT broker"""
        try:
            # Set additional connection options for better compatibility
            self.client.will_set("client/status", "offline", qos=1, retain=True)
            self.client.connect(self.broker, self.port, keepalive=30)  # Reduced keepalive for compatibility
            self.client.loop_start()

            # Publish online status
            if self.connected:
                self.client.publish("client/status", "online", qos=1, retain=True)

            # Wait for connection
            timeout = 10
            while not self.connected and timeout > 0:
                time.sleep(0.1)
                timeout -= 0.1
            return self.connected
        except Exception as e:
            log_simple(f"Error connecting to MQTT broker: {e}", "ERROR")
            return False

    def disconnect(self):
        """Disconnect from MQTT broker"""
        if self.connected:
            self.client.loop_stop()
            self.client.disconnect()
            self.connected = False

    def publish(self, topic, payload, qos=1, retain=False):
        """Publish message to topic with structured payload"""
        if not self.connected:
            log_simple("Not connected to MQTT broker", "ERROR")
            return False

        try:
            # Ensure payload is JSON string
            if isinstance(payload, dict):
                payload = json.dumps(payload)
            elif not isinstance(payload, str):
                payload = str(payload)

            result = self.client.publish(topic, payload, qos=qos, retain=retain)
            result.wait_for_publish()
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                log_simple(f"Published to {topic}: {payload}", "INFO")
                return True
            else:
                log_simple(f"Failed to publish to {topic}, error code: {result.rc}", "ERROR")
                return False
        except Exception as e:
            log_simple(f"Error publishing to {topic}: {e}", "ERROR")
            return False

    def subscribe(self, topic, qos=1):
        """Subscribe to topic"""
        if not self.connected:
            log_simple("Not connected to MQTT broker", "ERROR")
            return False

        try:
            result = self.client.subscribe(topic, qos)
            if result[0] == mqtt.MQTT_ERR_SUCCESS:
                log_simple(f"Subscribed to {topic}", "SUCCESS")
                return True
            else:
                log_simple(f"Failed to subscribe to {topic}, error code: {result[0]}", "ERROR")
                return False
        except Exception as e:
            log_simple(f"Error subscribing to {topic}: {e}", "ERROR")
            return False

    def unsubscribe(self, topic):
        """Unsubscribe from topic"""
        if not self.connected:
            log_simple("Not connected to MQTT broker", "ERROR")
            return False

        try:
            result = self.client.unsubscribe(topic)
            if result[0] == mqtt.MQTT_ERR_SUCCESS:
                log_simple(f"Unsubscribed from {topic}", "SUCCESS")
                return True
            else:
                log_simple(f"Failed to unsubscribe from {topic}, error code: {result[0]}", "ERROR")
                return False
        except Exception as e:
            log_simple(f"Error unsubscribing from {topic}: {e}", "ERROR")
            return False
