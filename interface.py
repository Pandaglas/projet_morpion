from cgitb import text
from http.client import OK
from tkinter import *
import socket
import re

#******************************************************
#
#                VARIABLES GLOBALES
#
#******************************************************

# Défini si l'utilisateur a les ronds ou les croix
rond_croix="croix"

#******************************************************
#
#                    FONCTIONS
#
#******************************************************

def get_Colonne_Ligne(event):

    colonne=-1
    ligne=-1

    abscisse = event.x
    ordonnee = event.y
    #message.configure(text='Clic en X = {0} et Y = {1}'.format(abscisse, ordonnee))

    # Identification de la colonne 
    if (abscisse > 0 and abscisse < 100):
        colonne=1
    elif (abscisse > 100 and abscisse < 200):
        colonne=2
    elif (abscisse > 200 and abscisse < 300):
        colonne=3

    # Identification de la ligne
    if (ordonnee > 0 and ordonnee < 100):
        ligne=1
    elif (ordonnee > 100 and ordonnee < 200):
        ligne=2
    elif (ordonnee > 200 and ordonnee < 300):
        ligne=3

    # message.configure(text='Colonne = {0} et Ligne = {1}'.format(colonne, ligne))

    if (rond_croix == "croix"):
        set_Croix(colonne,ligne)
    elif(rond_croix == "rond"):
        set_Rond(colonne,ligne)


# Dessine une croix à l'endroit indiqué par les arguments
def set_Croix(colonne,ligne):
    x1=colonne*100-100+10
    x2=colonne*100-10
    y1=ligne*100-100+10
    y2=ligne*100-10

    dessin.create_line(x1,y1,x2,y2,width=10,fill='red')
    dessin.create_line(x1,y2,x2,y1,width=10,fill='red')


# Dessine un rond à l'endroid indiqué par les arguments
def set_Rond(colonne,ligne):
    x1=colonne*100-100+10
    x2=colonne*100-10
    y1=ligne*100-100+10
    y2=ligne*100-10

    dessin.create_oval(x1,y1,x2,y2,width=10,outline='blue')

# Connexion au serveur distant 
def Connexion():
    ipvalue=ip_serveur.get("1.0",END)
    ipvalue=ipvalue.split("\n")[0]
    portvalue=port_serveur.get("1.0",END)
    portvalue=portvalue.split("\n")[0]
    ipv4="^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    result=re.match(ipv4,ipvalue)
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if result:
        print(ipvalue)
        print(portvalue)
        socket_client.connect((ipvalue, int(portvalue)))
        message.configure(text="connected")


#******************************************************
#
#                      MAIN
#
#******************************************************

# Création de la fenêtre
fen=Tk()
fen.title("Morpion")

message=Label(fen, text='Ici du texte.')
message.grid(row = 0, column = 0, columnspan=2, padx=3, pady=3, sticky = W+E)

# Boutons
bouton_quitter = Button(fen, text='Quitter', command=fen.destroy)
bouton_quitter.grid(row = 2, column = 1, padx=3, pady=3, sticky = S+W+E)

bouton_connexion = Button(fen, text='Connexion', command=Connexion)
bouton_connexion.grid(row = 2, column = 0, padx=3, pady=3, sticky = S+W+E)

# Canevas
dessin=Canvas(fen, bg="white", width=301, height=301)
dessin.grid(row = 1, column = 0, columnspan = 2, padx=5, pady=5)

# Grille
lignes = []
for i in range(4):
    lignes.append(dessin.create_line(0, 100*i+2, 303, 100*i+2, width=3))
    lignes.append(dessin.create_line(100*i+2, 0, 100*i+2, 303, width=3))

# Infos de connexion
ip_serveur=Text(fen,height=1,width=20)
ip_serveur.grid(row=3,column=0)
# ip_serveur.pack()

#port_serveur
port_serveur=Text(fen,height=1,width=15)
port_serveur.grid(row=3,column=1)

dessin.bind('<Button-1>', get_Colonne_Ligne)
#bouton_connexion.bind('<Button-1>',Connexion)

fen.mainloop()