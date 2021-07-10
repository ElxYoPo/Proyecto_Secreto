def get_database():
    from pymongo import MongoClient
    MONGO_URI = "mongodb://uwvux4q3nizdduh0anv5:RNGokX3ElBEv7xE0AYkB@brsadfxyffl9s2t-mongodb.services.clever-cloud.com:27017/brsadfxyffl9s2t"
    cliente = MongoClient(MONGO_URI)
    db = cliente["brsadfxyffl9s2t"]
    coleccionUsuarios = db["usuarios"]
    # coleccion.insert_one({"usuario": "Prueba", "password": "prueba123"})
    return coleccionUsuarios

def post_resena():
    from pymongo import MongoClient
    MONGO_URI = "mongodb://uwvux4q3nizdduh0anv5:RNGokX3ElBEv7xE0AYkB@brsadfxyffl9s2t-mongodb.services.clever-cloud.com:27017/brsadfxyffl9s2t"
    cliente = MongoClient(MONGO_URI)
    db = cliente["brsadfxyffl9s2t"]
    resena = db["resena"]
    # coleccion.insert_one({"usuario": "Prueba", "password": "prueba123"})
    return resena

def post_coleccion():
    from pymongo import MongoClient
    MONGO_URI = "mongodb://uwvux4q3nizdduh0anv5:RNGokX3ElBEv7xE0AYkB@brsadfxyffl9s2t-mongodb.services.clever-cloud.com:27017/brsadfxyffl9s2t"
    cliente = MongoClient(MONGO_URI)
    db = cliente["brsadfxyffl9s2t"]
    colecciones = db["colecciones"]
    # coleccion.insert_one({"usuario": "Prueba", "password": "prueba123"})
    return colecciones

# # This is added so that many files can reuse the function get_database()
if __name__ == "__main__":    
    
    # Get the database
    dbname = get_database()
    print(dbname)