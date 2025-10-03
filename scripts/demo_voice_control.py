#!/usr/bin/env python3
"""
Demonstration of Voice Control for Relay Automation
Shows the complete flow as specified by user requirements
"""

import json
from voice_control import VoiceControl

def demonstrate_voice_control_flow():
    """Demonstrate the complete voice control flow"""

    print("🎤 Command Voice Relay Control - Speech to Text")
    print("=" * 60)

    # Step 1: Create sample configuration (exactly as per user specification)
    print("\n📋 Step 1: Sample Configuration (from automationVoiceConfig.json)")
    sample_config = {
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

    print(json.dumps(sample_config, indent=2))

    # Save to file
    with open('JSON/automationVoiceConfig.json', 'w') as f:
        json.dump([sample_config], f, indent=2)

    # Step 2: Initialize voice control
    print("\n🎙️  Step 2: Initialize Voice Control System")
    voice_control = VoiceControl()
    print("✅ Voice control system initialized")

    # Step 3: Demonstrate command analysis
    print("\n🧠 Step 3: Command Analysis - 'nyalakan lampu utama ruangan meeting'")
    test_command = "nyalakan lampu utama ruangan meeting"

    print(f"Input command: '{test_command}'")

    # Analyze command action
    action = voice_control.analyze_command_action(test_command.lower())
    print(f"→ Action detected: '{action}' → Boolean data: {1 if action == 'on' else 0}")

    # Extract object name
    object_name = voice_control.extract_object_name(test_command.lower(), action)
    print(f"→ Object extracted: '{object_name}'")

    # Step 4: Find configuration using object_name as key
    print("\n🔍 Step 4: Configuration Lookup using object_name as key")
    config = voice_control.find_configuration_by_object_name(object_name)
    if config:
        print("✅ Configuration found:")
        print(f"   - object_name: {config['object_name']}")
        print(f"   - device_name: {config['device_name']}")
        print(f"   - pin: {config['pin']}")
        print(f"   - address: {config['address']}")
        print(f"   - device_bus: {config['device_bus']}")
        print(f"   - mac: {config['mac']}")
        print(f"   - part_number: {config['part_number']}")

    # Step 5: Create MQTT payload
    print("\n📡 Step 5: Create MQTT Payload for topic 'modular'")
    if config:
        payload = {
            "mac": config.get('mac'),
            "protocol_type": "Modular",
            "device": config.get('part_number'),
            "function": "write",
            "value": {
                "pin": config.get('pin'),
                "data": 1 if action == "on" else 0
            },
            "address": config.get('address'),
            "device_bus": config.get('device_bus'),
            "Timestamp": "2025-09-29 20:15:00"
        }

        print("✅ MQTT Payload created:")
        print(json.dumps(payload, indent=2))

        print("\n📤 Step 6: Publish to MQTT topic 'modular'")
        print("✅ Payload would be published to MQTT broker")
        print("✅ Relay device would receive control command")

    print("\n🎉 Demonstration completed successfully!")
    print("\n📝 Summary:")
    print("- ✅ Command analysis: 'nyalakan' → action='on' → data=1")
    print("- ✅ Object extraction: 'lampu utama ruangan meeting'")
    print("- ✅ Configuration lookup using object_name as key")
    print("- ✅ Pin data extraction: pin=1")
    print("- ✅ MQTT payload creation with all required fields")
    print("- ✅ Ready for MQTT publishing to 'modular' topic")

if __name__ == "__main__":
    demonstrate_voice_control_flow()
