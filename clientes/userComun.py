import socket, sys, json
from os import system, name
from prettytable import PrettyTable
import getpass
import os

def enviarDatos(sock,contenido, servicio):
    # Generacion de la transaccion
    # validacion de argumentos
    if len(servicio) < 5 or len(contenido) < 1:
        print("Error: los datos no se han ingresado correctamente")
        return

    transaccionLen = len(contenido) + len(servicio)
    largoText = str((transaccionLen)).zfill(5) # zfill rellena con ceros a la izquierda hasta llegar a 5
    
    transaccion = largoText + servicio + contenido
    # print("Servicio: transaccion-",transaccion)
    sock.sendall(transaccion.encode())

def escucharBus(sock):
    cantidadRecibida = 0
    
    while True:
        data = sock.recv(4096)
        cantidadRecibida += len(data)
        # print("data ricibida:",cantidadRecibida)
        # print('received {!r}'.format(data))
        transLen = int(data[:5].decode())
        nombreServicio = data[5:10].decode()
        msgTransaccion= data[10:5+transLen].decode()
        # print("tamaño de transaccion:",tamañoTransaccion)
        # print("msg:",msgTransaccion)
        return nombreServicio, msgTransaccion

def showLoginScreen():
    print("□□□□□□□□□□ Inicio sesión Usuario común □□□□□□□□□□")
    user = input("Usuario: ")
    password = getpass.getpass("Contrasenha: ")
    print(f"prueba usuario: {user} password: {password}")
    os.system('clear')

    enviarDatos(sock, user + " " + password, "dvnli" )
    serv, mensaje=escucharBus(sock)
    print(mensaje)
    if mensaje.endswith("NoUser") or mensaje.endswith("NoPass"):
        input("Usuario o contrasenha incorrectos. Pulse cualquier tecla para continuar")
        showLoginScreen()
    elif mensaje.endswith("NoActive"):
        input("Esta cuenta no se encuentra activa. Pulse cualquier tecla para continuar")
        showLoginScreen()
    elif mensaje.endswith("admin"):
        input("Esta cuenta corresponde al rol de administrador y no puede acceder a este menu. Pulse cualquier tecla para continuar")
        showLoginScreen()
    else:
        os.system('clear')
        return user

def handleFirstOption(username):

    while True:
        os.system('clear')
        print("□□□□□□□□□□ Completa los campos □□□□□□□□□□□□□□")
        name = input("Ingresa el nombre del juego: ")
        review = input("Ingresa tu resena: ")
        stars = input("Ingresa cantidad de estrellas [0-10]: ")
        if(name and review and stars and stars.isdigit() and  0 <= int(stars) <= 10 ):
            enviarDatos(sock, username + "--" + name + "--" + review + "--" + stars, "dvnar" )
            serv, mensaje=escucharBus(sock)
            input(f"{mensaje}, presione [Enter] para continuar...")
            os.system('clear')
            break
        else:
            print(" Verifique los datos ingresados")
            input(" presione [Enter] para continuar...")



def handleSecondOption():
    while True:
        os.system('clear')
        print("□□□□□□□□□□ Completa los campos □□□□□□□□□□□□□□")
        name = input("Ingresa el nombre del juego: ")
        if(name):
            enviarDatos(sock, name,  "dvnor" )
            break
        else:
            print( "Debe completar la información solicitada")
            input(" presione [Enter] para continuar...")

    
    serv, mensaje=escucharBus(sock)
    mensaje = mensaje.split('---')
    mensaje.pop(0) #elimina el OK
    table = PrettyTable()
    table.field_names = ["byUser", "Review","Stars"]
    for item in mensaje:
        msg = item.split('--')
        table.add_row([ msg[0], msg[1] , msg[2] ])
    print(table)
    input("presione [Enter] para continuar...")
    os.system('clear')

def handleThirdOption(username):
    while True:
        os.system('clear')
        print("□□□□□□□□□□ Completa los campos □□□□□□□□□□□□□□")
        name = input("Ingresa el nombre del juego: ")
        if(name):
            enviarDatos(sock, username+"--"+name,  "dvnac" )
            break
        else:
            print( "Debe completar la información solicitada")
            input(" presione [Enter] para continuar...")

    serv, mensaje=escucharBus(sock)
    print(mensaje)
    input("presione [Enter] para continuar...")

def handleFourOption(username):
    os.system('clear')
    print("□□□□□□□□□□ Completa los campos □□□□□□□□□□□□□□")
    enviarDatos(sock, username,  "dvnoc" )
    serv, mensaje=escucharBus(sock)
    print(mensaje)
    input("presione [Enter] para continuar...")
    os.system('clear')


def handleFiveOption(username):
    while True:
        os.system('clear')
        print("□□□□□□□□□□ Completa los campos □□□□□□□□□□□□□□")
        name = input("Ingresa el nombre del juego: ")
        if(name):
            enviarDatos(sock, username+"--"+name,  "dvnec" )
            break
        else:
            print( "Debe completar la información solicitada")
            input(" presione [Enter] para continuar...")
    serv, mensaje=escucharBus(sock)
    print(mensaje)
    
    input("presione [Enter] para continuar...")


def handleSixOption():
    while True:
        os.system('clear')
        print("□□□□□□□□□□ Completa los campos □□□□□□□□□□□□□□")
        name = input("Ingresa el nombre del juego: ")
        if(name):
            enviarDatos(sock, name,  "dvnoj" )
            break
        else:
            print( "Debe completar la información solicitada")
            input(" presione [Enter] para continuar...")
    serv, mensaje=escucharBus(sock)
    table = PrettyTable()
    table.field_names = ["Nombre", "Publisher","Desarroladora", "Plataforma", "Genero"]
    mensaje = mensaje.split('--')
    if(mensaje[0] == "OK"):
        table.add_row([ mensaje[1], mensaje[2] , mensaje[3], mensaje[4], mensaje[5] ])
        print(table)
    else:
        print(mensaje)
    input("presione [Enter] para continuar...")

def showMenuScreen():
    while True:
        menu = """    
□□□□□□□□□□□□□□□□□ Usuario Común □□□□□□□□□□□□□□□□□
□ 1.- Realizar una reseña                       □
□ 2.- Obtener reseña                            □
□ 3.- Agregar juego a la colección              □
□ 4.- Consultar Colección                       □
□ 5.- Eliminar juego de la colección            □
□ 6.- Obtener información de un juego           □
□ 7.- Salir                                     □
□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□"""
        print(menu)
        select = input("Opción: ")
        if(select.isnumeric() and int(select)<=7):
            os.system('clear')
            break
        else:
            os.system('clear')
    return int(select)


def handleUserParams():
    username = showLoginScreen()
    while True:
        os.system('clear')
        select = showMenuScreen()
        if(select == 1):
            handleFirstOption(username)
        elif(select == 2):
            handleSecondOption()
        elif(select == 3):
            handleThirdOption(username)
            os.system('clear')
        elif(select == 4):
            handleFourOption(username)
            os.system('clear')
        elif(select == 5):
            handleFiveOption(username)
            os.system('clear')
        elif(select == 6):
            handleSixOption()
        elif(select == 7):
            break

if __name__ == "__main__":

    try:
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = ('localhost', 5000)
        print('Servicio: Conectandose a {} en el puerto {}'.format(*server_address))
        sock.connect(server_address)

    except: 
        print("No se ha podido establecer la conexión")
        quit() 

    handleUserParams()