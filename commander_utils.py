import subprocess
import json
COMMANDER_PATH = "/home/khpham/SimplicityStudio_v5/developer/adapter_packs/commander" #update commander path if need
def flash_firmware(ip_address, firmware_path):
    try:
        result = subprocess.run([f'{COMMANDER_PATH}/commander', 'flash', firmware_path, '--ip', ip_address], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output =  result.stdout.decode()
        print(output)
        if "Error" in output:
            return False
        return True
    except subprocess.CalledProcessError as e:
        return e.stderr.decode()

def erase_firmware(ip_address):
    try:
        result = subprocess.run([f'{COMMANDER_PATH}/commander', 'device', 'masserase', '--ip', ip_address], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output =  result.stdout.decode()
        print(output)
        if "Error" in output:
            return False
        return True
    except subprocess.CalledProcessError as e:
        return e.stderr.decode()

def get_device_info(ip_address):
    try:
        result = subprocess.run([f'{COMMANDER_PATH}/commander', 'device', 'info', '--ip', ip_address], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode()
    except subprocess.CalledProcessError as e:
        return e.stderr.decode()

def read_manifest():
    with open('firmware/manifest.json', 'r') as file:
        return json.load(file)

def write_manifest(data):
    with open('firmware/manifest.json', 'w') as file:
        json.dump(data, file, indent=4)
