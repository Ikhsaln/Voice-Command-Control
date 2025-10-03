"""
Network Utilities Module
Provides functions for network interface detection and MAC address retrieval.
"""

import subprocess
from typing import Optional

from .logging import log_simple

def get_active_mac_address() -> str:
    """
    Get MAC address from active network interface.
    Prioritizes wlan0 (Linux WiFi), eth0 (Linux Ethernet), en0 (macOS WiFi), en1 (macOS Ethernet).

    Returns:
        MAC address string or default "00:00:00:00:00:00" if not found
    """
    # Priority: en1 (macOS active) > en0 (macOS WiFi) > wlan0 (Linux WiFi) > eth0 (Linux Ethernet)
    interfaces = ['en1', 'en0', 'wlan0', 'eth0']

    # First try: Use ifconfig (most reliable on embedded systems)
    try:
        log_simple("Checking network interfaces with ifconfig", "INFO")
        ifconfig_result = subprocess.run(['ifconfig'], capture_output=True, text=True, timeout=5)
        if ifconfig_result.returncode == 0:
            lines = ifconfig_result.stdout.split('\n')
            current_interface = None
            for line in lines:
                line = line.strip()
                # Look for interface name (line that starts with interface name and ends with colon)
                if line and not line.startswith(' ') and not line.startswith('\t') and line.endswith(':'):
                    current_interface = line[:-1].strip()  # Remove the colon
                # Look for ether (MAC address) in the interface block
                elif current_interface and current_interface in interfaces and 'ether ' in line:
                    mac_match = line.split('ether ')[1].split()[0].strip()
                    # Validate MAC address format
                    if len(mac_match.split(':')) == 6 and len(mac_match) == 17:
                        # Check if interface is active by looking for status: active or RUNNING
                        interface_block_start = None
                        for i, check_line in enumerate(lines):
                            if check_line.strip().startswith(f'{current_interface}:'):
                                interface_block_start = i
                                break

                        if interface_block_start is not None:
                            is_active = False
                            # Check the next few lines for status or RUNNING
                            for i in range(interface_block_start, min(interface_block_start + 10, len(lines))):
                                check_line = lines[i].strip()
                                if 'status: active' in check_line or 'RUNNING' in check_line:
                                    is_active = True
                                    break
                                # Stop at next interface
                                if check_line and not check_line.startswith(' ') and not check_line.startswith('\t') and ':' in check_line and i > interface_block_start:
                                    break

                            if is_active:
                                log_simple(f"Found active MAC address from {current_interface}: {mac_match}", "SUCCESS")
                                return mac_match
                            else:
                                log_simple(f"Interface {current_interface} is not active", "WARNING")
    except Exception as e:
        log_simple(f"ifconfig method failed: {e}", "ERROR")

    # Second try: Use sysfs method
    for interface in interfaces:
        try:
            # Check if interface exists and is up
            operstate_path = f'/sys/class/net/{interface}/operstate'
            address_path = f'/sys/class/net/{interface}/address'

            # Check operstate
            with open(operstate_path, 'r') as f:
                operstate = f.read().strip()

            if operstate == 'up':
                # Get MAC address
                with open(address_path, 'r') as f:
                    mac_address = f.read().strip()

                # Validate MAC address format
                if len(mac_address.split(':')) == 6 and len(mac_address) == 17:
                    log_simple(f"Found active MAC address from {interface} (sysfs): {mac_address}", "SUCCESS")
                    return mac_address
                else:
                    log_simple(f"Invalid MAC format from {interface}: {mac_address}", "WARNING")
            else:
                log_simple(f"Interface {interface} operstate is {operstate}", "WARNING")
        except (FileNotFoundError, PermissionError, Exception) as e:
            log_simple(f"Failed to get MAC from {interface} (sysfs): {e}", "WARNING")
            continue

    # Fallback to default if no active interface found
    log_simple("No active network interface found, using default MAC", "WARNING")
    return "00:00:00:00:00:00"
