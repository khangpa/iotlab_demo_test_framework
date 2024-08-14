def test_device_telnet_commands(telnet_devices):
    for device in telnet_devices:
        print(f"IP: {device.host}")
        device.send_and_wait_for_response('help','print related commands.')

def test_telnet_gateway_command(telnet_gateway):
    telnet_gateway.send_and_wait_for_response('info','securityProfile')
