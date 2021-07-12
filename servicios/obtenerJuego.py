import socket
import socket, sys, json
from typing import Counter
from mongotest import post_juegos
import json

postJuego = post_juegos()

def iniciarServicio(sock,contenido, servicio):
    #construccion de la transaccion
    transaccionLen = len(contenido) + len(servicio)
    largoText = str((transaccionLen)).zfill(5) # zfill rellena con ceros a la izquierda hasta llegar a 5
    transaccion = largoText + servicio + contenido
    print("Servicio: transaccion-",transaccion)
    sock.sendall(transaccion.encode())
    #00010sinitdvnac seguir editando xd
    
def obtenerInfoJuego(registro):
    obtain = postJuego.find_one({"nombre": registro})
    obs = postJuego.find({"nombre": {f"$eq:{registro}"}})
    print(obs)
    if obtain:
        sendData = "--"+obtain["nombre"]+"--"+obtain["publisher"]+"--"+obtain["desarrolladora"]+"--"+obtain["plataforma"]+"--"+obtain["genero"]
        print(sendData)
        iniciarServicio(sock,sendData, "dvnoj") #mandar msg confirmando el insert
    else:
        iniciarServicio(sock,"--No se encuentra el juego", "dvnoj") #mandar msg confirmando el insert



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

    iniciarServicio(sock, "dvnoj","sinit")
    serv, msg = escucharBus(sock)
    if serv =="sinit" and msg[:2]=="OK":
        print("Servicio: Servicio iniciado con exito")
    else:
        print("Servicio: No se pudo iniciar el servicio")

    while True:
        serv, msg=escucharBus(sock) # editar func
        print(serv, msg)
        if serv == "dvnoj":
            obtenerInfoJuego(msg) # editar func

    print('Cerrando conexión')
    sock.close()