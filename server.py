import socket

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('', 8080))

socket.listen(5)

client1, adress1 = socket.accept()
print("{} connected".format(adress1))

client1.sendall(("j1"+","+"x").encode())

client2, adress2 = socket.accept()
print("{} connected".format(adress2))

client2.sendall(("j2"+","+"o").encode())

client1.sendall("start".encode())
client2.sendall("start".encode())

while True:
        response = client1.recv(255)
        response2 = client2.recv(255)
        if response != "":
                print(response)
        client1.sendall(response)
        if response2 != "":
                print(response2)
        client2.sendall(response2)
        client2.sendall(response)
        client1.sendall(response2)



print ("Close")
client.close()
stock.close()