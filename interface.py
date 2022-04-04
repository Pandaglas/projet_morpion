from cgitb import text
from faulthandler import disable
from http.client import OK
from tkinter import *
import socket
import re
import time
import tkinter
from turtle import update, width
from xmlrpc.client import boolean

#******************************************************
#
#                VARIABLES GLOBALES
#
#******************************************************

# Défini si l'utilisateur a les ronds ou les croix
rond_croix="o"

# Indique quel joueur est cette interface
joueur="j1"

# Indique si la partie a bien commencé
start="no"

#socket
socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Indique si c'est à ce client de jouer
your_turn=False

message_a_vous_de_jouer="A vous de jouer"
message_en_attente="En attente de l'adversaire"

# Datas Camille
ip="91.162.90.187"
port="16385"
#ip="127.0.0.1"
#port="24124"

# Sauvegarde temporaire positions signes
board=[]

# Indique si la partie est gagné ou égalité
gagne_perdu=""


#******************************************************
#
#                    FONCTIONS
#
#******************************************************

# Défini la colonne et la ligne sélectionnée
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

    
    global start
    if start=="start":
        global gagne_perdu
        if (gagne_perdu==""):
            emplacement_signe=str(ligne)+","+str(colonne)+";"

            # Ajoute le signe
            Ajoute_Croix_Rond(emplacement_signe[:-1],False)
            #global fen
            comp_fen.update()

            if (is_Filled()):
                gagne_perdu="fill;"

            if (Win()):
                gagne_perdu="win;" 
                Ajoute_Dans_Log("Vous avez gagné !!!!! :) ","SYSTEM")   

            emplacement_signe+=gagne_perdu

            #time.sleep(1)
            socket_client.send(emplacement_signe.encode())

            global joueur
            if (joueur=="J1"):
                Ajoute_Dans_Log(message_en_attente,"SYSTEM")
                comp_fen.update()
                
                response_value=socket_client.recv(1024).decode()
                print(response_value)

                Interpretation_Resultat(response_value)
                Ajoute_Dans_Log(message_a_vous_de_jouer,"SYSTEM")
            elif(joueur=="J2"):
                J2_Process()
        

# Interprète le résultat reçu de l'autre joueur
def Interpretation_Resultat(resultat: str) -> bool:
    tab_response_value=resultat.split(";")

    for value in tab_response_value:
        regex_emplacement="^[1-3],[1-3]$"
        if (re.match(regex_emplacement,value)):
            # Ajoute le signe de l'autre joueur
            Ajoute_Croix_Rond(str(value),True)
        elif(value=="win"):
            Ajoute_Dans_Log("Vous avez perdu !!!","SYSTEM")
            gagne_perdu=value
        elif(value=="fill"):
            Ajoute_Dans_Log("Egalité !","SYSTEM")
            gagne_perdu=value


# Défini si une croix ou un rond doit être affiché
def Ajoute_Croix_Rond(value: str,other_sign: bool):
    # Indique si le signe affiché doit être celui du joueur actuel ou de l'autre
    sign=""
    if ((other_sign == True and rond_croix == "x")
        or (other_sign == False and rond_croix == "o")):
        sign="o"
    else:
        sign="x"

    if (value!=""):
        ligne=int(value.split(",")[0])
        colonne=int(value.split(",")[1])

        # Ajoute dans la sauvegarde l'emplacement du signe
        global board
        board[ligne-1][colonne-1]=sign

        if (sign == "x"):
            set_Croix(colonne,ligne)
            Ajoute_Dans_Log("["+str(colonne)+","+str(ligne)+"] X","J1")
        elif(sign == "o"):
            set_Rond(colonne,ligne)
            Ajoute_Dans_Log("["+str(colonne)+","+str(ligne)+"] O","J2")

# Dessine une croix à l'endroit indiqué par les arguments
def set_Croix(colonne: int,ligne: int):
    x1=colonne*100-100+10
    x2=colonne*100-10
    y1=ligne*100-100+10
    y2=ligne*100-10

    comp_dessin.create_line(x1,y1,x2,y2,width=10,fill='red')
    comp_dessin.create_line(x1,y2,x2,y1,width=10,fill='red')

# Dessine un rond à l'endroid indiqué par les arguments
def set_Rond(colonne: int,ligne: int):
    x1=colonne*100-100+10
    x2=colonne*100-10
    y1=ligne*100-100+10
    y2=ligne*100-10

    comp_dessin.create_oval(x1,y1,x2,y2,width=10,outline='blue')

# Connexion au serveur distant 
def Connexion():
    # Récupère l'ip
    ipvalue=comp_ip_serveur.get("1.0",END)
    ipvalue=ipvalue.split("\n")[0]
    # Récupère le port
    portvalue=comp_port_serveur.get("1.0",END)
    portvalue=portvalue.split("\n")[0]

    # Vérification si l'ip est bien de type ipv4
    ipv4="^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    result=re.match(ipv4,ipvalue)
    
    if result:
        socket_client.connect((ipvalue, int(portvalue)))
        
        data = socket_client.recv(1024).decode()
        print(data)
        
        global rond_croix
        rond_croix=data.split(",")[1]

        global joueur
        joueur=data.split(",")[0]
        
        comp_message.configure(text=joueur)
        Ajoute_Dans_Log("Connexion au serveur effectuée","SYSTEM")
        Ajoute_Dans_Log("Vous êtes "+joueur+", votre signe : "+rond_croix,"SYSTEM")
        comp_fen.update()

        #waiting for start
        global start
        start=socket_client.recv(1024).decode()

        if start=="start":
            Ajoute_Dans_Log("Second joueur trouvé","SYSTEM")
            Ajoute_Dans_Log("La partie commence !","SYSTEM")

            # Initialise le board
            create_board()

            if (joueur=="J2"):
                J2_Process()
            elif(joueur=="J1"):
                global your_turn
                your_turn=True
                Ajoute_Dans_Log(message_a_vous_de_jouer,"SYSTEM")
        else:
            Ajoute_Dans_Log("Problème dans la connexion","SYSTEM")

# Processus de jeu pour le joueur 2
# A la différence du J1 qui commence à jouer, le J2 attend d'abord la croix du J1 avant de jouer
# Il doit donc être d'abord en mode "réception" puis en mode "envoi" (sans réception ensuite)
def J2_Process():
    Ajoute_Dans_Log(message_en_attente,"SYSTEM")
    comp_fen.update()
    response_value=socket_client.recv(1024).decode()
    print(response_value)

    Interpretation_Resultat(response_value)
    Ajoute_Dans_Log(message_a_vous_de_jouer,"SYSTEM")

# Quitte la fenêtre en fermant la socket active
def quitter():
    socket_client.close()
    comp_fen.destroy()

# Ajoute une nouvelle ligne dans le composant de logs
def Ajoute_Dans_Log(texte: str,who: str):
    comp_log_msg.configure(state='normal')
    comp_log_msg.insert(INSERT,who+": "+texte+"\n")
    comp_log_msg.configure(state='disabled')
    comp_log_msg.see("end")

# Retourne True si le joueur a gagné la partie
def Win() -> bool:
    win = None
    global board

    n = len(board)

    # checking rows
    for i in range(n):
        win = True
        for j in range(n):
            if board[i][j] != rond_croix:
                win = False
                break
        if win:
            return win

    # checking columns
    for i in range(n):
        win = True
        for j in range(n):
            if board[j][i] != rond_croix:
                win = False
                break
        if win:
            return win

    # checking diagonals
    # Diagonale 1
    win = True
    for i in range(n):
        if board[i][i] != rond_croix:
            win = False
            break
    if win:
        return win

    # Diagonale 2
    win = True
    for i in range(n):
        if board[i][n - 1 - i] != rond_croix:
            win = False
            break
    if win:
        return win
    return False

# Retourne True si le plateau est rempli
def is_Filled() -> bool:
    global board
    for row in board:
        for item in row:
            if item == '-':
                return False
    return True

# Transforme le board en matrice [3,3]
def create_board():
    global board
    for i in range(3):
        row = []
        for j in range(3):
            row.append('-')
        board.append(row)

#******************************************************
#
#                      MAIN
#
#******************************************************

# Création de la fenêtre
comp_fen=Tk()
comp_fen.title("Morpion")

# Panneaux
comp_pw1=PanedWindow(orient=tkinter.HORIZONTAL)
comp_pw1.pack(fill=BOTH,expand=True)

comp_frame_left=Frame(comp_fen)
comp_frame_right=Frame(comp_fen)

comp_pw1.add(comp_frame_left)
comp_pw1.add(comp_frame_right)

comp_message=Label(comp_frame_left)
comp_message.grid(row = 0, column = 0, columnspan=2, padx=3, pady=3, sticky = W+E)

# Boutons
comp_bouton_quitter = Button(comp_frame_left, text='Quitter', command=quitter)
comp_bouton_quitter.grid(row = 2, column = 1, padx=3, pady=3, sticky = S+W+E)

comp_bouton_connexion = Button(comp_frame_left, text='Connexion', command=Connexion)
comp_bouton_connexion.grid(row = 2, column = 0, padx=3, pady=3, sticky = S+W+E)

# Canevas
comp_dessin=Canvas(comp_frame_left, bg="white", width=301, height=301)
comp_dessin.grid(row = 1, column = 0, columnspan = 2, padx=5, pady=5)

# Grille
lignes = []
for i in range(4):
    lignes.append(comp_dessin.create_line(0, 100*i+2, 303, 100*i+2, width=3))
    lignes.append(comp_dessin.create_line(100*i+2, 0, 100*i+2, 303, width=3))

# Infos de connexion
comp_ip_serveur=Text(comp_frame_left,height=1,width=20)
comp_ip_serveur.grid(row=3,column=0)
comp_ip_serveur.insert(END,ip)
# ip_serveur.pack()

#port_serveur
comp_port_serveur=Text(comp_frame_left,height=1,width=15)
comp_port_serveur.grid(row=3,column=1)
comp_port_serveur.insert(END,port)

#log
comp_log_msg=Text(comp_frame_right,height=24,width=40)
comp_log_msg.pack()

comp_dessin.bind('<Button-1>', get_Colonne_Ligne)


comp_fen.mainloop()