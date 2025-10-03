#!/usr/bin/env python3
"""
Voice Control Module for Relay Automation
Provides speech-to-text functionality to control relays based on voice commands.
"""

import json
import time
import threading
import speech_recognition as sr
from datetime import datetime
from typing import Optional, Dict, Any

from middleware.mqtt_handler import MQTTHandler
from middleware.logging import setup_logging, log_simple

class VoiceControl:
    def __init__(self, config_file="JSON/automationVoiceConfig.json"):
        self.config_file = config_file
        self.mqtt = MQTTHandler(client_id="voice_control")
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        self.logger = setup_logging()

        # Voice commands mapping
        self.voice_commands = {
            # Indonesian commands
            "nyalakan": "on",
            "hidupkan": "on",
            "aktifkan": "on",
            "on": "on",
            "mati": "off",
            "matikan": "off",
            "padamkan": "off",
            "off": "off",
            "toggle": "toggle",
            "ubah": "toggle",
            "ganti": "toggle",

            # English commands
            "turn on": "on",
            "turn off": "off",
            "switch on": "on",
            "switch off": "off",
            "power on": "on",
            "power off": "off"
        }

    def load_configurations(self):
        """Load automation voice configurations"""
        try:
            with open(self.config_file, 'r') as f:
                data = json.load(f)
                # Ensure it's a list
                if isinstance(data, dict) and "configurations" in data:
                    return data["configurations"]
                elif isinstance(data, list):
                    return data
                else:
                    return []
        except (FileNotFoundError, json.JSONDecodeError) as e:
            log_simple(f"Error loading configurations: {e}", "ERROR")
            return []

    def find_configuration_by_name(self, name):
        """Find configuration by device name or object name"""
        configurations = self.load_configurations()
        name_lower = name.lower().strip()

        # Try exact match first
        for config in configurations:
            if (config.get('device_name', '').lower() == name_lower or
                config.get('object_name', '').lower() == name_lower):
                return config

        # Try partial match
        for config in configurations:
            if (name_lower in config.get('device_name', '').lower() or
                name_lower in config.get('object_name', '').lower() or
                name_lower in config.get('description', '').lower()):
                return config

        return None

    def analyze_command_action(self, text):
        """Analyze what action the command is requesting (on/off/toggle)"""
        # Check for each command type
        for command, action in self.voice_commands.items():
            if command in text:
                return action
        return None

    def extract_object_name(self, text, action):
        """Extract the object name from the command text"""
        # Sort commands by length (longest first) to match most specific commands
        sorted_commands = sorted(self.voice_commands.keys(), key=len, reverse=True)

        # Remove the action command from text to get the object name
        for command in sorted_commands:
            if command in text:
                # Remove the command and clean up the text
                object_text = text.replace(command, '').strip()
                # Remove extra spaces and return
                return ' '.join(object_text.split())
        return None

    def find_configuration_by_object_name(self, object_name):
        """Find configuration specifically by object_name field"""
        configurations = self.load_configurations()
        object_name_lower = object_name.lower().strip()

        # Exact match first
        for config in configurations:
            if config.get('object_name', '').lower() == object_name_lower:
                return config

        # Partial match
        for config in configurations:
            if object_name_lower in config.get('object_name', '').lower():
                return config

        return None

    def control_relay(self, config, action):
        """Control relay using MQTT"""
        try:
            # Determine data value based on action
            if action == "on":
                data_value = 1
            elif action == "off":
                data_value = 0
            elif action == "toggle":
                # For toggle, we could implement logic to check current state
                # For now, default to on
                data_value = 1
            else:
                log_simple(f"Unknown action: {action}", "ERROR")
                return False

            # Prepare MQTT payload
            payload = {
                "mac": config.get('mac', '00:00:00:00:00:00'),
                "protocol_type": "Modular",
                "device": config.get('part_number', 'RELAY'),
                "function": "write",
                "value": {
                    "pin": config.get('pin', 1),
                    "data": data_value
                },
                "address": config.get('address', 0),
                "device_bus": config.get('device_bus', 0),
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            # Publish to MQTT
            success = self.mqtt.publish("modular", payload)

            if success:
                device_name = config.get('object_name') or config.get('device_name')
                log_simple(f"Successfully controlled {device_name} - {action}", "SUCCESS")
                return True
            else:
                log_simple(f"Failed to publish control command for {config.get('device_name')}", "ERROR")
                return False

        except Exception as e:
            log_simple(f"Error controlling relay: {e}", "ERROR")
            return False

    def process_voice_command(self, text):
        """Process voice command and execute control"""
        text_lower = text.lower().strip()
        log_simple(f"Processing voice command: '{text}'", "INFO")

        # Step 1: Analyze command - what action is being requested (on/off → boolean 1/0)
        action = self.analyze_command_action(text_lower)
        if not action:
            log_simple(f"No valid action found in command: {text}", "WARNING")
            return False

        # Convert action to boolean data value
        data_value = 1 if action == "on" else 0
        log_simple(f"Command analysis: action='{action}' → data_value={data_value}", "INFO")

        # Step 2: Extract object name from command (what device to control)
        object_name = self.extract_object_name(text_lower, action)
        if not object_name:
            log_simple(f"Could not extract object name from: {text}", "WARNING")
            return False

        log_simple(f"Object extraction: '{object_name}'", "INFO")

        # Step 3: Find configuration using object_name as key
        config = self.find_configuration_by_object_name(object_name)
        if not config:
            log_simple(f"No configuration found for object: '{object_name}'", "WARNING")
            available_devices = [c.get('object_name', '') for c in self.load_configurations() if c.get('object_name')]
            log_simple(f"Available objects: {', '.join(available_devices)}", "INFO")
            return False

        # Step 4: Extract pin data from JSON configuration
        pin = config.get('pin', 1)
        log_simple(f"Configuration found: {config.get('object_name')} → pin {pin}", "INFO")

        # Step 5: Create MQTT payload and publish
        return self.control_relay(config, action)

    def listen_for_commands(self):
        """Listen for voice commands"""
        if hasattr(self, 'demo_mode') and self.demo_mode:
            # Demo mode - simulate voice control without microphone
            log_simple("Voice control running in DEMO mode", "INFO")
            log_simple("Demo commands available: 'nyalakan lampu', 'matikan lampu', 'toggle lampu'", "INFO")

            while self.is_listening:
                try:
                    # In demo mode, just wait and show status
                    time.sleep(2)
                    log_simple("Demo mode: Voice control active (use test_voice_command for testing)", "INFO")
                except Exception as e:
                    log_simple(f"Demo mode error: {e}", "ERROR")
                    break
        else:
            # Normal mode with microphone
            try:
                with sr.Microphone() as source:
                    log_simple("Adjusting for ambient noise...", "INFO")
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)

                    log_simple("Voice control activated. Say commands like 'turn on lamp' or 'matikan lampu'", "SUCCESS")

                    while self.is_listening:
                        try:
                            log_simple("Listening for command...", "INFO")
                            audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)

                            # Recognize speech
                            text = self.recognizer.recognize_google(audio, language='id-ID')
                            log_simple(f"Heard: {text}", "INFO")

                            # Process command
                            success = self.process_voice_command(text)

                            if success:
                                log_simple("Command executed successfully", "SUCCESS")
                            else:
                                log_simple("Command execution failed", "WARNING")

                        except sr.WaitTimeoutError:
                            # Timeout, continue listening
                            continue
                        except sr.UnknownValueError:
                            log_simple("Could not understand audio", "WARNING")
                            continue
                        except sr.RequestError as e:
                            log_simple(f"Speech recognition error: {e}", "ERROR")
                            time.sleep(1)
                            continue
                        except Exception as e:
                            log_simple(f"Unexpected error: {e}", "ERROR")
                            continue
            except Exception as e:
                log_simple(f"Failed to initialize microphone: {e}", "ERROR")
                log_simple("Falling back to demo mode", "WARNING")
                self.demo_mode = True
                # Recursively call in demo mode
                self.listen_for_commands()

    def start_voice_control(self):
        """Start voice control"""
        try:
            # First, check if we can access microphone
            log_simple("Checking audio device availability...", "INFO")
            with sr.Microphone() as source:
                # Try to access microphone briefly
                pass
            log_simple("Audio device available", "SUCCESS")
        except OSError as e:
            log_simple(f"No audio device available: {e}", "ERROR")
            log_simple("Voice control requires microphone access. Running in demo mode.", "WARNING")
            # Continue without actual voice recognition
            self.demo_mode = True
        except Exception as e:
            log_simple(f"Audio device check failed: {e}", "ERROR")
            log_simple("Voice control requires microphone access. Running in demo mode.", "WARNING")
            self.demo_mode = True

        # Connect to MQTT
        if not self.mqtt.connect():
            log_simple("Failed to connect to MQTT broker", "ERROR")
            return False

        self.is_listening = True

        # Start listening in a separate thread
        voice_thread = threading.Thread(target=self.listen_for_commands)
        voice_thread.daemon = True
        voice_thread.start()

        if hasattr(self, 'demo_mode') and self.demo_mode:
            log_simple("Voice control started in DEMO mode (no microphone required)", "SUCCESS")
            log_simple("Use test_voice_command() method for testing commands", "INFO")
        else:
            log_simple("Voice control started with microphone. Press Ctrl+C to stop.", "SUCCESS")

        return True

    def stop_voice_control(self):
        """Stop voice control"""
        self.is_listening = False
        self.mqtt.disconnect()
        log_simple("Voice control stopped", "SUCCESS")

    def test_voice_command(self, text):
        """Test voice command processing without MQTT"""
        log_simple(f"Testing voice command: {text}", "INFO")
        return self.process_voice_command(text)

def main():
    """Main function"""
    voice_control = VoiceControl()

    try:
        if voice_control.start_voice_control():
            # Keep running
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        voice_control.stop_voice_control()
    except Exception as e:
        log_simple(f"Error in main: {e}", "ERROR")
        voice_control.stop_voice_control()

if __name__ == "__main__":
    main()
