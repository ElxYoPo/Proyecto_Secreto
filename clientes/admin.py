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
    print("|======== Acceso a herramientas de administrador ========|")
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
    elif mensaje.endswith("comun"):
        input("Esta cuenta corresponde a un usuario comun y no puede acceder a este menu. Pulse cualquier tecla para continuar")
        showLoginScreen()
    os.system('clear')
    return user

def handleFirstOption(username):
    os.system('clear')
    print("|============= Complete los campos =============|")
    name = input("Ingrese el nombre del juego: ")
    publisher = input("Ingrese el publisher asociado al juego: ")
    desarrolladora = input("Ingrese la desarrolladora asociada al juego: ")
    plataforma = input("Ingrese la plataforma asociada al juego: ")
    genero = input("Ingrese el genero asociado al juego: ")
    enviarDatos(sock, name + "--" + publisher + "--" + desarrolladora + "--" + plataforma + "--" + genero, "dvnaj" )
    serv, mensaje=escucharBus(sock)
    if mensaje.endswith("AlreadyExists"):
        input("El juego ya existe en la base de datos. Presione [Enter] para continuar...")
        os.system('clear')
    elif mensaje.endswith("NoAdded"):
        input("Hubo un error al agregar el juego. Presione [Enter] para continuar...")
        os.system('clear')
    input(f"{mensaje}, presione [Enter] para continuar...")
    os.system('clear')

def handleSecondOption():
    os.system('clear')
    print("|============= Complete los campos =============|")
    name = input("Ingrese el nombre del juego: ")
    enviarDatos(sock, name,  "dvnej" )
    serv, mensaje=escucharBus(sock)
    if mensaje.endswith("NoJuego"):
        input("El juego no existe o se ha eliminado previamente de la base de datos. Presione [Enter] para continuar...")
        os.system('clear')
    elif mensaje.endswith("NoDeleted"):
        input("Hubo un error al eliminar el juego. Presione [Enter] para continuar...")
        os.system('clear')
    input(f"{mensaje}, presione [Enter] para continuar...")
    os.system('clear')

def handleThirdOption(username):
    os.system('clear')
    print("|============= Complete los campos =============|")
    name = input("Ingrese el nombre de usuario a desactivar: ")
    confirma = input(f"Seguro que quiere desactivar {name}? Y/N")
    while confirma.upper() != "Y" and confirma.upper() != "N":
        confirma = input("Teclee \"Y\" para confirmar la accion y \"N\" para abortarla")
    if confirma.upper() == "Y":
        enviarDatos(sock, name, "dvndc" )
        serv, mensaje=escucharBus(sock)
        if mensaje.endswith("Error"):
            input("Ha ocurrido un error inesperado, presione [Enter] para continuar...")
            os.system('clear')
        elif mensaje.endswith("NoUser"):
            input("No se ha encontrado al usuario especificado, presione [Enter] para continuar...")
            os.system('clear')
        elif mensaje.endswith("Admin"):
            input("No puede activar o desactivar un usuario administrador o a si mismo, presione [Enter] para continuar...")
            os.system('clear')
        elif mensaje.endswith("SiDeac"):
            input("El usuario especificado ya esta desactivado, presione [Enter] para continuar...")
            os.system('clear')
        else:
            input(f"{mensaje}, presione [Enter] para continuar...")
            os.system('clear')
    elif confirma.upper() == "N":
        input("Se ha abortado la acción, presione [Enter] para continuar...")
        os.system('clear')

def handleFourthOption(username):
    os.system('clear')
    print("|============= Complete los campos =============|")
    name = input("Ingrese el nombre de usuario a desactivar: ")
    confirma = input(f"Seguro que quiere desactivar {name}? Y/N")
    while confirma.upper() != "Y" and confirma.upper() != "N":
        confirma = input("Teclee \"Y\" para confirmar la accion y \"N\" para abortarla")
    if confirma.upper() == "Y":
        enviarDatos(sock, name, "dvndc" )
        serv, mensaje=escucharBus(sock)
        if mensaje.endswith("Error"):
            input("Ha ocurrido un error inesperado, presione [Enter] para continuar...")
            os.system('clear')
        elif mensaje.endswith("NoUser"):
            input("No se ha encontrado al usuario especificado, presione [Enter] para continuar...")
            os.system('clear')
        elif mensaje.endswith("Admin"):
            input("No puede activar o desactivar un usuario administrador o a si mismo, presione [Enter] para continuar...")
            os.system('clear')
        elif mensaje.endswith("NoDeac"):
            input("El usuario especificado ya esta desactivado, presione [Enter] para continuar...")
            os.system('clear')
        else:
            input(f"{mensaje}, presione [Enter] para continuar...")
            os.system('clear')
    elif confirma.upper() == "N":
        input("Se ha abortado la acción, presione [Enter] para continuar...")
        os.system('clear')

def showMenuScreen():
    while True:
        print("|=============== Menu de ADMINISTRADOR ===============|")
        print(" 1.- Agregar un juego en el sistema")
        print(" 2.- Eliminar un juego del sistema")
        print(" 3.- Desactivar una cuenta")
        print(" 4.- Reactivar una cuenta desactivada")
        print(" 5.- Salir")
        select = input(" Opcion: ")
        if(select.isnumeric() and int(select)<=6):
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
            os.system('clear')
        elif(select == 2):
            handleSecondOption()
            os.system('clear')
        elif(select == 3):
            handleThirdOption(username)
            os.system('clear')
        elif(select == 4):
            handleThirdOption(username)
            os.system('clear')
        elif(select == 5):
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