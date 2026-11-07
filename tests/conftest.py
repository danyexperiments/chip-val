import pytest
import logging
from src.chip_driver import ConnectivityChipDriver

# Configure custom logging for hardware telemetry
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def pytest_addoption(parser):
    """Add CLI flags to select real hardware vs simulation."""
    parser.addoption(
        "--port",
        action="store",
        default="SIMULATED",
        help="Target port for testing (e.g., SIMULATED, COM3, /dev/ttyUSB0)",
    )

@pytest.fixture(scope="session")
def chip_port(request):
    return request.config.getoption("--port")

@pytest.fixture(scope="function")
def chip_device(chip_port):
    """Fixture to manage chip initialization, hardware reset, and teardown."""
    logging.info(f"Initializing chip driver on port: {chip_port}")
    driver = ConnectivityChipDriver(port=chip_port)
    assert driver.connect(), "Failed to establish hardware communication."
    
    # Soft reset device before test execution
    driver.send_at_command("AT+RST")
    
    yield driver  # Provide chip instance to test
    
    # Teardown: Safely disconnect chip
    logging.info("Executing hardware teardown...")
    driver.send_at_command("AT+RST")
    driver.disconnect()