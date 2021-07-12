import socket
import socket, sys, json
from typing import Counter
from mongotest import get_database
import json

postUsers = get_database()

def iniciarServicio(sock,contenido, servicio):
    #construccion de la transaccion
    transaccionLen = len(contenido) + len(servicio)
    largoText = str((transaccionLen)).zfill(5) # zfill rellena con ceros a la izquierda hasta llegar a 5
    transaccion = largoText + servicio + contenido
    print("Servicio: transaccion-",transaccion)
    sock.sendall(transaccion.encode())
    #00010sinitdvnac seguir editando xd
    
def reactivarUser(registro):
    usuarito = postUsers.find_one({"usuario": registro})
    if not usuarito:
        print("el usuario no existe")
        iniciarServicio(sock, "NoUser", "dvnrc")
    elif usuarito["rol"] is "admin":
        print("el user es admin")
        iniciarServicio(sock, "Admin", "dvnrc")
    elif usuarito["rol"] == "comun": 
        if usuarito["activo"] is False:
            postUsers.replace_one({"usuario": registro}, {"usuario": registro, "password": usuarito["password"], "rol": usuarito["rol"], "activo": True})
            usuarito = postUsers.find_one({"usuario": registro})
            if usuarito["activo"] is False:
                print("no se reactivo")
                iniciarServicio(sock, "Error", "dvnrc")
            else:
                print("usuario reactivado")
                iniciarServicio(sock, "Se reactivo el usuario correctamente", "dvnrc")
        elif usuarito["activo"] is True:
            print("Esta activo el usuario")
            iniciarServicio(sock, "NoDeac", "dvnrc")
        else:
            print("No se leyo bien el estado")
            iniciarServicio(sock, "Error", "dvnrc")

def escucharBus(sock):
    cantidadRecibida = 0
    while True:
        data = sock.recv(4096)
        cantidadRecibida += len(data)
        transLen = int(data[:5].decode())
        nombreServicio = data[5:10].decode()
        msgTransaccion= data[10:5+transLen].decode()
        return nombreServicio, msgTransaccion

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

    iniciarServicio(sock, "dvnrc","sinit")
    serv, msg = escucharBus(sock)
    if serv =="sinit" and msg[:2]=="OK":
        print("Servicio: Servicio iniciado con exito")
    else:
        print("Servicio: No se pudo iniciar el servicio")

    while True:
        serv, msg=escucharBus(sock) # editar func
        print(serv, msg)
        if serv == "dvnrc":
            reactivarUser(msg) # editar func

    print('Cerrando conexión')
    sock.close()