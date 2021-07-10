import socket
import socket, sys, json
from typing import Counter
import json

with open("./SecurityDatabase/noEsExcel.json") as DB:
    database = json.load(DB)
    DB.close()

usuarios = database['usuarios']
biblioteca = database['biblioteca']
juegos = database['juegos']
categorias = database['categorias']
catPorJuego = database['catPorJuego']

# print(usuarios)
# print(catPorJuego)

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

#Generacion de la transaccion
def enviarTransaccion(sock,contenido, servicio):
    
    #construccion de la transaccion
    transaccionLen = len(contenido) + len(servicio)
    largoText = str((transaccionLen).zfill(5)) # zfill rellena con ceros a la izquierda hasta llegar a 5

    transaccion = largoText + servicio + contenido
    print("Servicio: transaccion-",transaccion)
    sock.sendall(transaccion.encode())
    #00010sinitdvnsu seguir editando xd
    
def registrarUsuario(registro):
    print("registrar ", registro)



    # Validar que el usuario no exista
    # cursor = conexion.execute("SELECT nombre FROM usuario WHERE nombre = ?", (registro["usuario"],))
    # resultado = cursor.fetchone()
    # if resultado == None: # Inicia el proceso de registro
    #     if registro["rol"] in ["1","2"]:
    #         rol = "cliente" if registro["rol"] == "1" else "administrador"
    #         # conexion.execute("INSERT INTO usuario (nombre, rol) VALUES(?,?)",(registro["usuario"],rol))
    #         # conexion.commit()
    #         respuesta = {"respuesta":"Se registrado correctamente"}
    #         enviarTransaccion(sock,json.dumps(respuesta), SERVICIO)
    #     else:
    #         respuesta = {"respuesta":"No se ha podido registrar al usuario"}
    #         enviarTransaccion(sock,json.dumps(respuesta), SERVICIO)
    # else: # si el usuario ya esta registrado
    #     respuesta = {"respuesta":"El usuario ya está registrado"}
    #     enviarTransaccion(sock,json.dumps(respuesta), SERVICIO)


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

    enviarTransaccion(sock, "dvnsu","sinit")
    # crearBase()
    serv, msg = escucharBus(sock)
    if serv =="sinit" and msg[:2]=="OK":
        print("Servicio: Servicio iniciado con exito")
    else:
        print("Servicio: No se pudo iniciar el servicio")

    while True:
        serv, msg=escucharBus(sock) # editar func
        print(serv, msg)
        if serv == "signp":
            registrarUsuario(json.loads(msg)) # editar func

    print('Cerrando conexión')
    sock.close()