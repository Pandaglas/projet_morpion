import socket
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('192.168.1.87', 16384))

socket.listen(5)
client1, address1 = socket.accept()
print("{} connected".format(address1))
client1.sendall(("J1"+","+"x").encode())


client2, adress2 = socket.accept()
print("{} connected".format(adress2))
client2.sendall(("J2"+","+"o").encode())

client1.sendall("start".encode())
client2.sendall("start".encode())

#while True:


 #       response = client1.recv(255)
  #      response2 = client2.recv(255)
   #     if response != "":
    #            print(response,"J1".encode())
    
     #   client1.sendall(response)
       
        
      #  if response2 != "":
              #  print(response2,"j2".encode())
    
    #    client2.sendall(response2)
     #   client2.sendall(response)
      #  client1.sendall(response2)
print ("Close")
client1.close()
client2.close()
#stock.close()