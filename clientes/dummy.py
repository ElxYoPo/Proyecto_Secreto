# menu = """    
# □□□□□□□□□□□□□□□□□ Usuario Común □□□□□□□□□□□□□□□□□
# □ 1.- Realizar una reseña                       □
# □ 2.- Obtener reseña                            □
# □ 3.- Agregar juego a la colección              □
# □ 4.- Consultar Colección                       □
# □ 5.- Eliminar juego de la colección            □
# □ 6.- Salir                                     □
# □□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□"""


# print(menu)


name = input(" asd ")
review = input(" asd ")
stars = input(" asd ")

if(name and review and stars and stars.isdigit() and  0 <= int(stars) <= 10 ):
    print("exito")