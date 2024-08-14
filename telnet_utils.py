import telnetlib
import time

class TelnetConnection:
    def __init__(self, host, port=23, timeout=10):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.connection = None

    def connect(self):
        self.connection = telnetlib.Telnet(self.host, self.port, self.timeout)

    def login(self, username, password):
        """Login to the telnet session with a username and password."""
        self.connection.read_until(b"login: ")
        self.connection.write(username.encode('ascii') + b'\n')
        self.connection.read_until(b"Password: ")
        self.connection.write(password.encode('ascii') + b'\n')
        time.sleep(1)  # Wait for login to complete
        self.connection.read_very_eager()  # Clear the buffer

    def send_command(self, command):
        """Send a command via telnet."""
        self.connection.write(command.encode('ascii') + b'\n')

    def read_until(self,expect:str, timeout=10)-> bytes:
        """Read the response from the telnet connection."""
        expect = expect.encode()
        return self.connection.read_until(expect, timeout)

    def send_and_wait_for_response(self, command, expected_data, timeout=10):
        """Send a command and wait for the expected data in the response."""
        self.send_command(command)
        output = self.read_until(expected_data).decode(errors="ignore")
        print(f'debug: {output}')
        if expected_data:
            index_of_expected = output.find(expected_data)
            if not index_of_expected >= 0:
                raise TimeoutError(f"Expected data '{expected_data}' not received within {timeout} seconds")
        else:
            output = output[:index_of_expected + len(expected_data)]
        return output

    def close(self):
        """Close the telnet connection."""
        if self.connection:
            self.connection.close()