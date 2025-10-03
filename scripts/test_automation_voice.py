#!/usr/bin/env python3
"""
Test script for AutomationVoice CRUD operations
"""

import json
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from AutomationVoice import AutomationVoice

def test_crud_operations():
    """Test CRUD operations without MQTT"""
    print("Testing AutomationVoice CRUD operations...")

    # Initialize
    automation = AutomationVoice()

    # Test CREATE
    print("\n1. Testing CREATE operation...")
    create_data = {
        "device_name": "Test Relay 1",
        "desc": "Test description",
        "objectName": "relay1",
        "pin": "1",
        "address": "32",
        "bus": "0",
        "part_number": "RELAYMINI"
    }

    result = automation.create_configuration(create_data)
    print(f"Create result: {json.dumps(result, indent=2)}")

    if result["status"] == "success":
        config_id = result["id"]
        print(f"Created configuration with ID: {config_id}")

        # Test READ
        print("\n2. Testing READ operation...")
        read_result = automation.read_configurations()
        print(f"Read all configurations: {len(read_result['data'])} found")

        # Test UPDATE
        print("\n3. Testing UPDATE operation...")
        update_data = {
            "device_name": "Updated Test Relay 1",
            "desc": "Updated description"
        }
        update_result = automation.update_configuration(config_id, update_data)
        print(f"Update result: {json.dumps(update_result, indent=2)}")

        # Test READ with filters
        print("\n4. Testing READ with filters...")
        filter_result = automation.read_configurations({"device_name": "Updated Test Relay 1"})
        print(f"Filtered read result: {len(filter_result['data'])} found")

        # Test DELETE
        print("\n5. Testing DELETE operation...")
        delete_result = automation.delete_configuration(config_id)
        print(f"Delete result: {json.dumps(delete_result, indent=2)}")

        # Verify deletion
        print("\n6. Verifying deletion...")
        final_read = automation.read_configurations()
        print(f"Final configuration count: {len(final_read['data'])}")

        print("\n✅ All CRUD operations completed successfully!")

    else:
        print("❌ Create operation failed")
        return False

    return True

def test_uuid_and_mac():
    """Test UUID generation and MAC address retrieval"""
    print("\nTesting UUID and MAC address...")

    import uuid
    from middleware.network_utils import get_active_mac_address

    # Test UUID
    test_uuid = str(uuid.uuid4())
    print(f"Generated UUID: {test_uuid}")
    print(f"UUID length: {len(test_uuid)}")

    # Test MAC
    mac = get_active_mac_address()
    print(f"Retrieved MAC address: {mac}")
    print(f"MAC format valid: {len(mac.split(':')) == 6 and len(mac) == 17}")

    return True

if __name__ == "__main__":
    print("Starting AutomationVoice tests...")

    # Test UUID and MAC
    test_uuid_and_mac()

    # Test CRUD
    success = test_crud_operations()

    if success:
        print("\n🎉 All tests passed!")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)
