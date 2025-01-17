from anon_python_sdk import ControlClient
from anon_python_sdk import start_anon, stop_anon
from time

print("Starting Anon...")
pid = start_anon()
print(f"Anon started with PID: {pid}")

time.sleep(5)  # Wait for Anon to start

client = ControlClient()

try:
    client.connect()
    circuits = client.get_circuits()
    for circuit in circuits:
        print(f"Circuit ID: {circuit.id}, Status: {circuit.status}")
        print(f"  Purpose: {circuit.purpose}")
        print(f"  Time Created: {circuit.time_created}")
        print("  Path:")
        for relay in circuit.path:
            print(f"    Fingerprint: {relay.fingerprint}, Nickname: {relay.nickname}")
finally:
    client.close()

    print("Stopping Anon...")
    stop_anon(pid)