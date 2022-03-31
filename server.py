import socket

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('', 8080))

while True:
        socket.listen(5)
        client, adress = socket.accept()
        client2, adress2 = socket.accept()

        print("{} connected".format(adress))
        print("{} connected".format(adress2))

        response = client.recv(255)
        response2 = client2.recv(255)
        if response != "":
                print(response)
        client.sendall(response)
        if response2 != "":
                print(response2)
        client2.sendall(response2)
        client2.sendall(response)
        client.sendall(response2)
print ("Close")
client.close()
stock.close()