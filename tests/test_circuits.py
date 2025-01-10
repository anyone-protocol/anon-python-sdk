from anon_python_sdk import start_anon, stop_anon, get_anon_circuits

def test_get_anon_circuits():
    circuits = get_anon_circuits()
    assert isinstance(circuits, list), "Circuits should be returned as a list"
    print(f"Circuits fetched: {circuits}")

