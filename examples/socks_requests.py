from anon_python_sdk.socks_client import SocksClient
from anon_python_sdk import start_anon, stop_anon
import time


def main():
    print("Starting Anon...")
    pid = start_anon()
    print(f"Anon started with PID: {pid}")

    time.sleep(5)  # Wait for Anon to start

    client = SocksClient()

    try:
        # Example GET request
        response = client.get("https://check.en.anyone.tech/api/ip")
        print("GET Response:")
        print(response.text)

        # Example POST request
        post_url = "https://httpbin.org/post"
        post_data = {"key": "value"}
        response = client.post(post_url, json=post_data)
        print("POST Response:")
        print(response.json())

        # Example DELETE request
        response = client.delete("https://httpbin.org/delete")
        print("DELETE Response:")
        print(response.json())

    except RuntimeError as e:
        print(f"Request error: {e}")

    finally:
        stop_anon(pid)
        print("Anon stopped")


if __name__ == "__main__":
    main()
