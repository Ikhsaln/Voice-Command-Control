#!/usr/bin/env python3

import subprocess

def test_mac_detection():
    interfaces = ['en1', 'en0', 'wlan0', 'eth0']

    try:
        ifconfig_result = subprocess.run(['ifconfig'], capture_output=True, text=True, timeout=5)
        if ifconfig_result.returncode == 0:
            lines = ifconfig_result.stdout.split('\n')
            current_interface = None
            for line in lines:
                line = line.strip()
                print(f"Processing line: {line}")
                # Look for interface name (line that starts with interface name)
                if line and not line.startswith(' ') and not line.startswith('\t') and ':' in line:
                    current_interface = line.split(':')[0].strip()
                    print(f"Found interface: {current_interface}")
                # Look for ether (MAC address) in the interface block
                elif current_interface and current_interface in interfaces and 'ether ' in line:
                    mac_match = line.split('ether ')[1].split()[0].strip()
                    print(f"Found MAC for {current_interface}: {mac_match}")
                    # Validate MAC address format
                    if len(mac_match.split(':')) == 6 and len(mac_match) == 17:
                        print(f"Valid MAC format: {mac_match}")
                        # Check if interface is active
                        interface_block_start = None
                        for i, check_line in enumerate(lines):
                            if check_line.strip().startswith(f'{current_interface}:'):
                                interface_block_start = i
                                break

                        if interface_block_start is not None:
                            print(f"Checking interface block starting at line {interface_block_start}")
                            is_active = False
                            # Check the next few lines for status or RUNNING
                            for i in range(interface_block_start, min(interface_block_start + 10, len(lines))):
                                check_line = lines[i].strip()
                                print(f"Checking line {i}: {check_line}")
                                if 'status: active' in check_line or 'RUNNING' in check_line:
                                    is_active = True
                                    print(f"Interface {current_interface} is ACTIVE")
                                    break
                                # Stop at next interface
                                if check_line and not check_line.startswith(' ') and not check_line.startswith('\t') and ':' in check_line and i > interface_block_start:
                                    break

                            if is_active:
                                print(f"SUCCESS: Found active MAC address from {current_interface}: {mac_match}")
                                return mac_match
                            else:
                                print(f"Interface {current_interface} is not active")
    except Exception as e:
        print(f"Error: {e}")

    print("No active interface found")
    return "00:00:00:00:00:00"

if __name__ == "__main__":
    mac = test_mac_detection()
    print(f"Final MAC: {mac}")
