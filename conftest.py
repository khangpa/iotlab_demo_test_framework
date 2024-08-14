import pytest
import time
from telnet_utils import TelnetConnection
from commander_utils import flash_firmware, erase_firmware, read_manifest

@pytest.fixture(scope="session", autouse=True)
def setup_firmware():
    manifest = read_manifest()
    print("Running setup_firmware fixture")
    for device in manifest['devices']:
        ip_address = device['ip_address']
        firmware_path = f"firmware/{device['firmware']}"
        print(f"Erase firmware for device {ip_address}")
        erase_firmware(ip_address)
        time.sleep(1)
        print(f"Flashing firmware for device {ip_address}")
        flash_firmware(ip_address, firmware_path)
        time.sleep(5)

@pytest.fixture(scope="module")
def telnet_devices():
    devices = []
    manifest = read_manifest()
    for device_info in manifest['devices']:
        ip_address = device_info['ip_address']
        if device_info['device_role'] == "NCP":
            continue
        device = TelnetConnection(host=ip_address, port=4901)
        device.connect()
        devices.append(device)
    yield devices
    for device in devices:
        device.close()

@pytest.fixture(scope="session")
def telnet_gateway():
    gateway = TelnetConnection(host='192.168.1.3', port=23)  # Adjust IP according to your setup
    gateway.connect()
    gateway.login(username='pi', password='solutions')  # Replace with actual username and password
    gateway.send_and_wait_for_response("./Z3Gateway/build/debug/Z3Gateway -p /dev/ttyACM0", "Z3Gateway", timeout=30)
    yield gateway
    gateway.close()

