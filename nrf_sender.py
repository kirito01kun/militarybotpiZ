import traceback
import time
import pigpio
from nrf24 import *

MAX_TEMP = None

def send_nrf(message, hostname='localhost', port=8888, address='1SNSR'):
    # Connect to pigpiod
    global MAX_TEMP

    print("I'm being called with the Msg:" + message)
    pi = pigpio.pi(hostname, port)
    if not pi.connected:
        print("Not connected to Raspberry Pi ... goodbye.")
        return

    # Initialize NRF24
    nrf = NRF24(pi, ce=17, payload_size=RF24_PAYLOAD.DYNAMIC, channel=100, data_rate=RF24_DATA_RATE.RATE_250KBPS, pa_level=RF24_PA.LOW)
    nrf.set_address_bytes(len(address))
    nrf.open_writing_pipe(address)
    nrf.open_reading_pipe(RF24_RX_ADDR.P1, address)

    try:
        # Encode message
        payload = message.encode()

        # Send payload
        nrf.reset_packages_lost()
        nrf.send(payload)
        nrf.wait_until_sent()

        if nrf.get_packages_lost() == 0:
            print(f"Success: lost={nrf.get_packages_lost()}, retries={nrf.get_retries()}")
        else:
            print(f"Error: lost={nrf.get_packages_lost()}, retries={nrf.get_retries()}")

        # Wait for response
        start_time = time.time()
        while time.time() - start_time < 3:  # Wait for 1 second for response
            if nrf.data_ready():
                pipe = nrf.data_pipe()
                response = nrf.get_payload().decode()
                MAX_TEMP = response
                break  # Exit loop once response received

        time.sleep(0.1)  # Adjust the sleep time as needed

    except Exception as e:
        traceback.print_exc()
    finally:
        nrf.power_down()
        pi.stop()

if __name__ == "__main__":
    # Example usage: send_nrf("Your message here")
    pass  # When executing as main, do nothing
