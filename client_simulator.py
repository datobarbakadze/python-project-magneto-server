import socket
import sys
import time
host, port = "192.168.16.100", 9999

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((host, port))
    print(sock.getsockname())
except:
    print("Can't connect")
# time.sleep(3)
# sock.close()
while True:
    val = input("Message to send: ")
    # Connect to server_container and send data


    try:
        sock.sendall(bytes(val + "\n", "utf-8"))
    except:
        print("Can't send")

    rec = sock.recv(1024)
    print(rec)
    # Receive data from the server_container and shut down
