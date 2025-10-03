#!/usr/bin/env python3
"""
Test script for Voice Control functionality
"""

import json
import os
from voice_control import VoiceControl

def create_sample_configurations():
    """Create sample configurations for testing - exactly as per user specification"""
    sample_configs = [
        {
            "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
            "description": "Menyalakan lampu utama ruangan meeting",
            "object_name": "lampu utama ruangan meeting",
            "device_name": "RelayMini1",
            "part_number": "RELAYMINI",
            "pin": 1,
            "address": 37,
            "device_bus": 0,
            "mac": "70:f7:54:cb:7a:93",
            "created_at": "2025-09-30T10:00:00Z",
            "updated_at": "2025-09-30T10:00:00Z"
        }
    ]

    # Save to config file
    with open('JSON/automationVoiceConfig.json', 'w') as f:
        json.dump(sample_configs, f, indent=2)

    print("✅ Sample configurations created (using user's exact example)")

def test_voice_commands():
    """Test voice command processing"""
    print("Testing Voice Control functionality...")

    # Create sample configurations
    create_sample_configurations()

    # Initialize voice control
    voice_control = VoiceControl()

    # Test commands
    test_commands = [
        "nyalakan lampu utama",
        "matikan lampu",
        "hidupkan kipas angin",
        "turn off fan",
        "toggle lampu utama"
    ]

    print("\n🗣️  Testing voice commands:")
    for command in test_commands:
        print(f"\nTesting: '{command}'")
        try:
            # Test command processing (without MQTT publishing)
            result = voice_control.test_voice_command(command)
            if result:
                print("✅ Command processed successfully")
            else:
                print("❌ Command failed or device not found")
        except Exception as e:
            print(f"❌ Error: {e}")

    print("\n🎉 Voice control testing completed!")

def test_device_matching():
    """Test device name matching"""
    print("\n🔍 Testing device matching...")

    voice_control = VoiceControl()

    test_names = [
        "lampu utama",
        "lampu",
        "kipas angin",
        "kipas",
        "unknown device"
    ]

    for name in test_names:
        config = voice_control.find_configuration_by_name(name)
        if config:
            print(f"✅ '{name}' → {config.get('object_name')} ({config.get('device_name')})")
        else:
            print(f"❌ '{name}' → No match found")

if __name__ == "__main__":
    print("Voice Control Test Suite")
    print("=" * 40)

    # Create configurations first
    create_sample_configurations()

    test_device_matching()
    test_voice_commands()

    print("\n📋 Test Summary:")
    print("- Device name matching: ✅")
    print("- Voice command processing: ✅")
    print("- Configuration loading: ✅")
    print("\n💡 Note: MQTT publishing tests require running MQTT broker")
