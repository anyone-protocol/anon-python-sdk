from anon_python_sdk import ControlClient, AnonRunner, AnonConfig, RelayInfo
import time


# Create a configuration
config = AnonConfig(
    auto_terms_agreement=True,
    socks_port=0
)

# Initialize and start the runner
runner = AnonRunner(config)
runner.start()

time.sleep(10)  # Wait for Anon to start

client = ControlClient()

try:
    client.connect()
    circuits = client.get_circuits()
    
    print("Get info about relay from circuit:", circuits[0])

    # Get relay info from the first relay in the first circuit
    relay_fingerprint = circuits[0].path[0].fingerprint
    relay_info = client.get_relay_info(relay_fingerprint)
    print(f"Relay [0] info: {relay_info}")

finally:
    client.close()

    runner.stop()