import socket

hote = "91.162.90.187"
port = 16384

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((hote, port))

print ("Connection on {}".format(port))
socket.send("formation2022".encode())

# data = socket.recv(1024)
# print(f"Received {data!r}")

print ("Close")
socket.close()