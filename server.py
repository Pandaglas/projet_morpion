import socket
import time

#******************************************************
#
#                VARIABLES GLOBALES
#
#******************************************************

# Datas Camille
ip="91.162.90.187"
port=16384
#ip="127.0.0.1"
#port=24124

#******************************************************
#
#                     METHODES
#
#******************************************************



#******************************************************
#
#                      MAIN
#
#******************************************************
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((ip, port))

socket.listen(5)

# Connexion au client1
client1, address1 = socket.accept()
print("{} connected".format(address1))
client1.send(("J1"+","+"x").encode())

# Connexion au client2
client2, adress2 = socket.accept()
print("{} connected".format(adress2))
client2.send(("J2"+","+"o").encode())

time.sleep(0.5)
# Envoi notif de début de jeu
client1.send("start".encode())
client2.send("start".encode())

try:
    
    continue_game=True
    while continue_game:
        # J1 to J2
        response=client1.recv(255).decode()
        if (response==""):
            continue_game=False
            print("Socket client1 fermée")
        else:
            client2.send(response.encode())
            print("J1 to J2 : "+response)

          
        # J2 to J1
        if(continue_game):
            response=client2.recv(255).decode()
            if (response==""):
                continue_game=False
                print("Socket client2 fermée")
            else:
                client1.send(response.encode())
                print("J2 to J1 : "+response)
    

    print ("Close")
    client1.close()
    client2.close()

except: 
    print ("Close")
    client1.close()
    client2.close()