from anon_python_sdk import Controller, AnonRunner, AnonConfig


# Create a configuration
config = AnonConfig(
    auto_terms_agreement=True
)

# Initialize and start the runner
runner = AnonRunner(config)
runner.start()

client = Controller.from_port()

try:
    client.authenticate()
    circuits = client.get_circuits()
    for circuit in circuits:
        print(f"Circuit ID: {circuit.id}")
        print(f"  Time Created: {circuit.created}")
        print("  Path:")
        for relay in circuit.path:
            print(
                f"    Fingerprint: {relay.fingerprint}, Nickname: {relay.nickname}")
finally:
    client.close()
    runner.stop()
