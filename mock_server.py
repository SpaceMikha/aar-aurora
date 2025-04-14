import socket
import threading
from datetime import datetime

COLOR_CYAN = "\033[96m"
COLOR_RESET = "\033[0m"

HOST = '0.0.0.0'
PORT = 1130

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

    try:
        with conn:
            while True:
                data = conn.recv(1024).decode().strip()
                if not data:
                    break

                print(f"[MOCK] Received: {data}")

                if data.startswith("#TR"):
                    response = "#TR;\nSPADE31 A320 LEBL LERT FL320\nRCH251 KC135 ETAD LERT FL250\n"
                elif data.startswith("#FP SPADE31"):
                    response = (
                        "SPADE31\n"
                        "DEP: LEBL\n"
                        "ARR: LERT\n"
                        "ALT: FL320\n"
                        "TYP: A320\n"
                        "REMARKS: AAR RECEIVER\n"
                        "ROUTE: DCT MUR DCT AAR DCT LERT\n"
                    )
                elif data.startswith("#FP RCH251"):
                    response = (
                        "RCH251\n"
                        "DEP: ETAD\n"
                        "ARR: LERT\n"
                        "ALT: FL250\n"
                        "TYP: KC135\n"
                        "REMARKS: TANKER SUPPORT AAR\n"
                        "ROUTE: DCT GOLGI DCT AAR13 DCT LERT\n"
                    )
                elif data.startswith("#TRPOS SPADE31"):
                    response = "SPADE31 422507N 0082945E 250 FL320 270 360\n"
                else:
                    response = "#UNKNOWN;\n"

                conn.sendall(response.encode())
    except Exception as e:
        print(f"[ERROR] {e}")

    print(f"[MOCK] Connection closed from {addr}")

def start_mock_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[MOCK] Aurora simulated server is running on {HOST}:{PORT}")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_mock_server()
