import pytest
import logging

class TestConnectivityChip:

    def test_chip_reset_and_idle(self, chip_device):
        """Verify chip responds to reset command and enters IDLE state."""
        response = chip_device.send_at_command("AT+RST")
        assert response == "OK"
        assert chip_device.current_mode == "IDLE"

    @pytest.mark.parametrize("ssid,password,expected", [
        ("Home_Wi-Fi", "Pass1234!", "WIFI_OK"),
        ("Renesas_IoT_5G", "SecureKey99", "WIFI_OK"),
        ("", "EmptySSID", "ERROR_INVALID_PARAM"),
    ])
    def test_wifi_connection_modes(self, chip_device, ssid, password, expected):
        """Validate Wi-Fi connection handling with valid/invalid credentials."""
        cmd = f"AT+WIFI_CONNECT={ssid},{password}"
        response = chip_device.send_at_command(cmd)
        assert response == expected

        if expected == "WIFI_OK":
            assert chip_device.current_mode == "WIFI_CONNECTED"

    def test_ble_advertising_and_rssi(self, chip_device):
        """Validate BLE advertising initialization and signal strength readback."""
        adv_resp = chip_device.send_at_command("AT+BLE_ADV_START")
        assert adv_resp == "BLE_ADV_OK"

        rssi_resp = chip_device.send_at_command("AT+GET_RSSI")
        assert rssi_resp.startswith("RSSI:")

        # Extract numerical RSSI value and validate within operational threshold
        rssi_val = int(rssi_resp.split(":")[1])
        logging.info(f"Measured BLE RSSI: {rssi_val} dBm")
        assert -90 <= rssi_val <= -30, f"RSSI value {rssi_val} out of valid RF range."