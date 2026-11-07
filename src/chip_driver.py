import time
import random

class ConnectivityChipDriver:

    def __init__(self, port: str = "SIMULATED", timeout: float = 2.0):
        self.port = port
        self.timeout = timeout
        self.is_connected = False
        self.current_mode = "IDLE"

    def connect(self) -> bool:
        """Simulate hardware initialization and handshake."""
        time.sleep(0.1)  # Simulate bus delay
        self.is_connected = True
        return True

    def disconnect(self) -> bool:
        self.is_connected = False
        self.current_mode = "IDLE"
        return True

    def send_at_command(self, command: str) -> str:
        """Send command to chip and parse response."""
        if not self.is_connected:
            raise ConnectionError("Chip is not connected via UART/SPI interface.")

        if command == "AT+RST":
            self.current_mode = "IDLE"
            return "OK"
        elif command.startswith("AT+WIFI_CONNECT="):
            # Parse parameters: AT+WIFI_CONNECT=SSID,PASS
            parts = command.split("=")[1].split(",")
            if len(parts) == 2 and parts[0] != "":
                self.current_mode = "WIFI_CONNECTED"
                return "WIFI_OK"
            return "ERROR_INVALID_PARAM"
        elif command == "AT+BLE_ADV_START":
            self.current_mode = "BLE_ADVERTISING"
            return "BLE_ADV_OK"
        elif command == "AT+GET_RSSI":
            # Simulate signal strength in dBm (-30 dBm to -90 dBm)
            return f"RSSI:{random.randint(-75, -40)}"

        return "ERROR_UNKNOWN_CMD"