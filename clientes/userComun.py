import socket, sys, json
from os import system, name
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
    print("|=============== Bienvenido ===============|")
    user = input("Usuario: ")
    password = getpass.getpass("Contrasenha: ")
    print(f"prueba usuario: {user} password: {password}")
    os.system('cls')

    enviarDatos(sock, user + " " + password, "dvnli" )
    serv, mensaje=escucharBus(sock)

    print(mensaje)

    # msg =  json.loads(mensaje[2:]) # los 2 primeros caracteres son OK
    # print(serv, msg)
    # if msg["respuesta"] == "noNombre":
    #     input("No se ha encontrado el usuario. Presione una tecla para continuar")
    #     showLoginScreen()
    # elif msg["respuesta"] == "noPass":
    #     input("La contrasenha no coincide con el usuario. Presione una tecla para continuar")
    #     showLoginScreen()
    # else:
    #     print(msg["respuesta"])
    #     pass

    return user, password

def showMenuScreen():
    while True:
        print("|=============== Menu de usuario ===============|")
        print(" 1.- Realizar una resenha")
        print(" 2.- Obtener resenha")
        print(" 3.- Agregar juego a la coleccion")
        print(" 4.- Consultar Coleccion")
        print(" 5.- Eliminar juego de la coleccion")
        print(" 6.- Salir")
        select = input(" Opcion: ")
        if(select.isnumeric() and int(select)<=6):
            os.system('cls')
            break
        else:
            os.system('cls')
    return int(select)

def handleUserParams():

    showLoginScreen()
    while True:
        select = showMenuScreen()
        if(select == 1):
            name = input("Ingresa el nombre del juego: ")
            review = input("Ingresa tu reseÃ±a: ")
            stars = input("Ingresa cantidad de estrellas: ")
            os.system('cls')
        elif(select == 2):
            name = input("Ingresa el nombre del juego: ")
            os.system('cls')
        elif(select == 3):
            name = input("Ingresa el nombre del juego: ")
            os.system('cls')
        elif(select == 4):
            print("aca se obtienen la colecciÃ³n a partir del nombre de usuario: ")
            os.system('cls')
        elif(select == 5):
            name = input("Ingresa el nombre del juego: ")
            os.system('cls')
        elif(select == 6):
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