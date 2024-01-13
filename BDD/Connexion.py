from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Class Connexion (design pattern : Singleton)
# Prend en paramètre Nomdb et NomCollection correspondant respectivement au nom de la base de données et au nom de la collection (en string) qu'on souhaite se connecter.
class Connexion:
    _instance = None
    Nomdb = ""
    NomCollection = ""
    db = None
    collection = None
    client = None

    # Nomdb : Nom de la base de données
    # NomCollection : Nom de la collection
    # Etabli une connexion avec une instance unique
    def __new__(cls, Nomdb, NomCollection):
        cls.Nomdb = Nomdb
        cls.NomCollection = NomCollection
        if cls._instance is None:
            cls._instance = super(Connexion, cls).__new__(cls)
            cls._instance.initialiserConnexion()
        return cls._instance
    
    # initialise la connexion à la base de données
    def initialiserConnexion(self):
        try :
            self.client = MongoClient("mongodb://localhost:27017/")  # Remplacez l'URL par celle de votre base de données si nécessaire
            database = self.client[self.Nomdb]
            self.db = database
            self.collection = database[self.NomCollection]
        except ConnectionFailure as erreur:
            print("Une erreur de connexion à la base de données s'est produite :", erreur)

    # Permet de fermer une connexion
    def closeConnexion(self):
        if self._instance is not None:
            self.client.close()
            self.reset()
            return True
        return False
    
    # Permet de réinitialiser l'instance de connexion
    @classmethod
    def reset(cls):
        cls._instance = None
        
    # Getter retourne l'object collection
    def getCollection(self):
        if self.collection is not None:
            return self.collection
        return None
    # Getter retourne l'object db
    def getDatabase(self):
        if self.db is not None:
            return self.db
        return None
    # Getter retourne le nom de la bd
    def getNomDb(self):
        if self.db != "":
            return self.Nomdb
        return None
    # Getter retourne le nom de la collection
    def getNomCollection(self):
        if self.NomCollection != "":
            return self.NomCollection
        return None