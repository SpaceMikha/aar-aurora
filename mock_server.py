#* This is a mock server so you don't need to necessarily be connected as ATC
# This script simulates an Aurora ATC server for testing purposes.
# It listens on TCP port 1130 and responds to specific Aurora protocol commands 
# such as #TR, #FP, and #TRPOS with mock flight data.

import socket
import threading
from datetime import datetime


COLOR_CYAN = "\033[96m"
COLOR_RESET = "\033[0m"


# Server configuration
# You can change the host and port if needed
HOST = '0.0.0.0'
PORT = 1130


#this function enables you to connect to the server from any PC (has to be connected to the same network as the server)
def handle_client(conn, addr):
    ip, port = addr
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"[MOCK] Connection from {addr}")

    
    welcome = (
        f"{COLOR_CYAN}Welcome!{COLOR_RESET} Connected to the Aurora Mock Server.\n"
        f"[{now}] Client: {COLOR_CYAN}{ip}:{port}{COLOR_RESET}\n"
        f"Try sending commands like: #TR, #FP SPADE31, or #TRPOS SPADE31\n\n"
    )
    conn.sendall(welcome.encode())

    with conn:
        while True:
            try:
                data = conn.recv(1024).decode().strip()
                if not data:
                    break
                print(f"[MOCK] Received: {data}")

                if data.startswith("#TR"):
                    response = "#TR;\nSPADE31 A320 LEBL LERT FL320\nRCH251 KC135 ETAD LERT FL250\n"
                elif data.startswith("#FP SPADE31"):
                    response = "SPADE31\nDEP: LEBL\nARR: LERT\nALT: FL320\nTYP: A320\nROUTE: DCT MUR DCT LOM DCT AAR\n"
                elif data.startswith("#TRPOS SPADE31"):
                    response = "SPADE31 422507N 0082945E 250 FL320 270 360\n"
                else:
                    response = "#UNKNOWN;\n"

                conn.sendall(response.encode())
            except:
                break
    print(f"[MOCK] Connection from {addr}")
    
    
    welcome = "Welcome! You are connected to the Aurora Mock Server.\n"
    conn.sendall(welcome.encode())

    with conn:
        while True:
            data = conn.recv(1024).decode().strip()
            if not data:
                break
            print(f"[MOCK] Received: {data}")
            
            if data.startswith("#TR"):
                response = "#TR;\nSPADE31 A320 LEBL LERT FL320\nRCH251 KC135 ETAD LERT FL250\n"
            elif data.startswith("#FP SPADE31"):
                response = "SPADE31\nDEP: LEBL\nARR: LERT\nALT: FL320\nTYP: A320\nROUTE: DCT MUR DCT LOM DCT AAR\n"
            elif data.startswith("#TRPOS SPADE31"):
                response = "SPADE31 422507N 0082945E 250 FL320 270 360\n"
            else:
                response = "#UNKNOWN;\n"

            conn.sendall(response.encode())
    print(f"[mock] connection from {addr}")
    with conn:
        while True:
            data = conn.recv(1024).decode().strip()
            if not data: 
                break
            print(f"[mock] received: {data}")
                
            if data.startswith("#TR"):
                response = "#TR;\nSPADE31 A320 LEBL LERT FL320\nRCH251 KC135 ETAD LERT FL250\n"
            elif data.startswith("#FP SPADE31"):
                response = "SPADE31\nDEP: LEBL\nARR: LERT\nALT: FL320\nTYP: A320\nROUTE: DCT MUR DCT LOM DCT AAR\n"
            elif data.startswith("#TRPOS SPADE31"):
                response = "SPADE31 422507N 0082945E 250 FL320 270 360\n"
            else:
                response = "#UNKNOWN;\n"
                
            conn.sendall(response.encode())

def start_mock_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[mock] Aurora simulated server is running on {HOST}:{PORT}")
    while True:
        conn, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()
        
if __name__ == "__main__":
    start_mock_server()