import os
from stem.control import Controller
import time

def is_anon_running(pid):
    """
    Check if a process with the given PID is running.
    Args:
        pid (int): Process ID of the Anon process.
    Returns:
        bool: True if the process is running, False otherwise.
    """
    try:
        os.kill(pid, 0)  # No signal is sent, just checks if the PID is valid
        return True
    except OSError:
        return False

def wait_for_control_port(port=9051, timeout=10):
    """
    Wait for the control port to become accessible.
    Args:
        port (int): Control port to check.
        timeout (int): Maximum time to wait in seconds.
    Returns:
        bool: True if the control port is accessible, False otherwise.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with Controller.from_port(port=port) as controller:
                controller.authenticate()  # Test connection
                return True
        except Exception:
            time.sleep(1)
    raise TimeoutError(f"Control port {port} did not become accessible within {timeout} seconds.")

def get_anon_circuits(control_port=9051):
    """
    Fetch the list of circuits from the Anon control port.
    Args:
        pid (int): Process ID of the Anon process.
        control_port (int): Port where the control service is listening.
    Returns:
        list: A list of circuits currently established in Anon.
    """
    # if not is_anon_running(pid):
    #     raise RuntimeError(f"Anon process with PID {pid} is not running.")

    # Wait for the control port to be ready
    wait_for_control_port(control_port)

    # Fetch circuits from the control port
    circuits = []
    try:
        with Controller.from_port(port=control_port) as controller:
            controller.authenticate()  # Use cookie authentication
            circuits = controller.get_circuits()
            print(f"Raw circuits: {circuits}")

        # Parse and return circuit information
        return [
            {
                "id": circuit.id,
                "status": circuit.status,
                "path": [
                    {
                        "fingerprint": entry.fingerprint,
                        "nickname": entry.nickname,
                    }
                    for entry in circuit.path
                ],
            }
            for circuit in circuits
        ]
    except Exception as e:
        print(f"Error fetching circuits from Anon: {e}")
        return []
