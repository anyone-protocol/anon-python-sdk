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

    # Fancy print for relay info
    print(f"\n[Relay Info]\n")
    print(f"Nickname: {relay_info.nickname}")
    print(f"Fingerprint: {relay_info.fingerprint}")
    print(f"IP: {relay_info.ip}")
    print(f"OR Port: {relay_info.or_port}")
    print(f"Flags: {', '.join(relay_info.flags)}")
    print(f"Bandwidth: {relay_info.bandwidth} bytes/sec")

finally:
    client.close()

    runner.stop()