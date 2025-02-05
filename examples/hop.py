from anon_python_sdk import ControlClient, AnonRunner, AnonConfig, SocksClient

print("Starting Anon...")
# Create a configuration
config = AnonConfig(
    auto_terms_agreement=True,
    display_log=False,
)

# Initialize and start the runner
runner = AnonRunner(config)
runner.start()

client = ControlClient()
socks = SocksClient()

try:
    print("Connecting to Control Port...")
    client.connect()

    print("Creating a new circuit through specified relays...")

    entry = "ECBFED17DB39601E6F39A1B8E0C432A0A6DDB752"
    mid = "B788C3437B75946E287BDB367587F1E17B91D40E"
    exit = "0D0588878AA61605406CD40A80655CC595C11607"

    #m_circuit_id = client.create_circuit([entry, mid, exit]) # 0.22115588188171387
    m_circuit_id = client.create_circuit([mid, exit]) #0.1490919589996338
    #m_circuit_id = client.create_circuit([exit])
    print(f"New circuit created with ID: {m_circuit_id}")
    m_circuit = client.get_circuit(m_circuit_id)

    # https://check.en.anyone.tech/api/ip 
    # http://ip-api.com/json/
    check = lambda socks: socks.get("http://ip-api.com/json") 
    resp = client.scan(m_circuit_id, check, socks)

    print(resp.text)

    print(f"Manual Circuit ID: {m_circuit.id}, Status: {m_circuit.status}, Path: {m_circuit.path}")

    print("Closing the manual circuit...")
    client.close_circuit(m_circuit_id)
    print(f"Manual circuit {m_circuit_id} closed successfully.")

finally:
    client.close()
    print("ControlClient connection closed.")

    print("Stopping Anon...")
    runner.stop()
