import argparse
from datetime import datetime
from random import normalvariate
import struct
import sys
import time
import traceback

import pigpio
from nrf24 import *

if __name__ == "__main__":    
    print("Python NRF24 Simple Sender Example.")
    
    # Parse command line argument.
    parser = argparse.ArgumentParser(prog="simple-sender.py", description="Simple NRF24 Sender Example.")
    parser.add_argument('-n', '--hostname', type=str, default='localhost', help="Hostname for the Raspberry running the pigpio daemon.")
    parser.add_argument('-p', '--port', type=int, default=8888, help="Port number of the pigpio daemon.")
    parser.add_argument('address', type=str, nargs='?', default='1SNSR', help="Address to send to (3 to 5 ASCII characters).")
    
    args = parser.parse_args()
    hostname = args.hostname
    port = args.port
    address = args.address


    # Connect to pigpiod
    print(f'Connecting to GPIO daemon on {hostname}:{port} ...')
    pi = pigpio.pi(hostname, port)
    if not pi.connected:
        print("Not connected to Raspberry Pi ... goodbye.")
        sys.exit()

    nrf = NRF24(pi, ce=17, payload_size=RF24_PAYLOAD.DYNAMIC, channel=100, data_rate=RF24_DATA_RATE.RATE_250KBPS, pa_level=RF24_PA.LOW)
    nrf.set_address_bytes(len(address))
    nrf.open_writing_pipe(address)
    
    # Display the content of NRF24L01 device registers.
    nrf.show_registers()

    try:
        print(f'Send to {address}')
        count = 0
        while True:
            
            pl = input("Enter what you wanna send: ")
            payload = pl.encode()

            # Send the payload to the address specified above.
            nrf.reset_packages_lost()
            nrf.send(payload)
            try:
                nrf.wait_until_sent()
            except TimeoutError:
                print('Timeout waiting for transmission to complete.')
                # Wait 10 seconds before sending the next reading.
                time.sleep(10)
                continue
            
            if nrf.get_packages_lost() == 0:
                print(f"Success: lost={nrf.get_packages_lost()}, retries={nrf.get_retries()}")
            else:
                print(f"Error: lost={nrf.get_packages_lost()}, retries={nrf.get_retries()}")

            # Wait 10 seconds before sending the next reading.
            time.sleep(0.1)
    except:
        traceback.print_exc()
        nrf.power_down()
        pi.stop()





