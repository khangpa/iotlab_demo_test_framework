def test_gateway_create_network(telnet_gateway):
    telnet_gateway.send_and_wait_for_response("network leave", "leave 0x")
    telnet_gateway.send_and_wait_for_response("plugin network-creator form 1 0xABCD 0 11", "NWK Creator: Form: 0x00")