import socket

hote = "localhost"
port = 8080

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((hote, port))

# print ("Connection on {}".format(port))
# socket.send("test".encode())

data = socket.recv(1024)
print(f"Received {data!r}")

print ("Close")
socket.close()