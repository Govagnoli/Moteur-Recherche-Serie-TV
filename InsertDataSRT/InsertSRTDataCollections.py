from glob import glob
from os.path import join
from pandas import read_csv
from pymongo.errors import ConnectionFailure
from BDD.Connexion import Connexion
from BDD.MDP import authentification
import sys
sys.path.insert(0,".")

# Constante vers le chemin relatif du répertoire des fichiers CSV TF-IDF multilangues (en et fr mélangé)
DIR_CSV = "../StockageFic/CSVConcat"

# chemin_ficCSV est un fichier du répertoire DIR_CSV
# Récupère tous les mots du fichier csv passé en paramètre et associe pour chaque mot, le nom de la série où le mot a été récupéré et son poids.
# Chaque mot devient une clé du dictionnaire mots valeur retour. À chaque clé se voir associé une liste avec le nom de la série et son poid dans le fichier lu
# Exemple format d'un mot : {'Le' : [{'Breacking Bad' : 15.02}, {'Blake' : 15.02}]}
def associerMotsToSeries(cheminFicCSV):
    mots = {}
    dfMots = read_csv(cheminFicCSV, encoding='utf-8')
    for index, row in dfMots.iterrows():
        mot = row['mots']  
        mots[mot] = [{"titre": str(row['serie']), "poids": float(row['poids'])}] 
    return mots

# Renvoie une liste de dictionnaire. Les clés de tous les dictionnaires correspondent à tous les mots de fichiers sous-titres lémmatisés.
# Utilise la fonction associerMotsToSeries() pour extraire les mots d'un fichier csv du répertoire DIR_CSV
def AllMotsToSeries(): 
    listDicAssocierMotsToSerie = []
    for chemin_ficCSV in glob.glob(join(DIR_CSV, '*.csv')): 
        listDicAssocierMotsToSerie.append(associerMotsToSeries(chemin_ficCSV))
    return listDicAssocierMotsToSerie

# listDicAssocierMotsToSeries prend comme valeurs le résultat de la fonction AllMotsToSeries()
# concatMotsSerie() permet de regrouper les mêmes mots ensemble. En concaténant la valeur associé à ces mots.
# La fonction retourne un dictionnaire. suivant le même format que associerMotsToSeries()
def concatMotsSerie(listDicAssocierMotsToSeries):
    dictionnaireDesMotsConcat={}
    for dic in listDicAssocierMotsToSeries:
        for mot, titre in dic.items():
            if mot in dictionnaireDesMotsConcat:
                dictionnaireDesMotsConcat[mot].extend(titre)
            else:
                dictionnaireDesMotsConcat[mot] = titre
    return dictionnaireDesMotsConcat

# Insert les données retourné par la fonction concatMotsSerie() dans la base de données MongoDb
def insertCollectionMots_Series():
    connexion = Connexion("SAE_S5", "Mots_Series")
    collection = connexion.getCollection()
    MotsJson = concatMotsSerie(AllMotsToSeries())
    Mots = list(MotsJson.keys())
    for mot in Mots:
        jsonFormat = {"mot": str(mot), "series": MotsJson[mot]}
        collection.insert_one(jsonFormat)
    connexion.closeConnexion()

# Retourne un dictionnaire python contenant les information de la série provenant du fichier csv concaténé d'une série. "titre" (titre de la série), "mots" (liste des mots de la série accompagné de leur poid)
# exemple : {"titre": "Breaking Bad", "mots": [{"mot": "drogue", "poids": 150}, {"mot": "bleu", "poids": 15}]}
# cheminFicCSV est un string correspondant au chemin d'accès vers le fichier csv de la série
def associerSeriesToMots(cheminFicCSV):
    serie = {}
    dfMots = read_csv(cheminFicCSV, encoding='utf-8')
    listMots = []
    for index, ligne in dfMots.iterrows():
        mot = ligne["mots"]
        poids = ligne["poids"]
        listMots.append({"mot": str(mot), "poids": float(poids)})
    titre = dfMots["serie"][1]
    serie["titre"] = str(titre)
    serie["mots"] = listMots
    return serie

# Insert les données dans la collection Series_Mots de mongodb
# Chaque ligne correspond aux informations retourné par la fonction associerSeriesToMots()
# On insert donc autant de données que de fichier csv (Cela correspond aux nombre de séries traitées dans notre cas 127 et non 128 car la série journeyman est vide)
def insertCollectionSeries_Mots():
    try:
        connexion = Connexion("SAE_S5", "Series_Mots")
    except ConnectionFailure as erreur:
        print("Une erreur de connexion à la base de données s'est produite :", erreur)
    collection = connexion.getCollection()
    for cheminFicCSV in glob.glob(join(DIR_CSV, "*.csv")):
        titre_mots = associerSeriesToMots(cheminFicCSV)
        collection.insert_one(titre_mots)
    connexion.closeConnexion()

def ajoutSerieInHistoUser(username:str, mdp:str, titre:str):
    id = authentification(username, mdp)
    if not id:
        raise ConnectionError("Nom utilisateur ou mot de passe incorrect")    
    historique = recupSeriesInHistoUser(username, mdp)
    if titre in historique:
        return
    try:
        connexion = Connexion("SAE_S5", "Utilisateur")
    except ConnectionFailure as erreur:
        print("Une erreur de connexion à la base de données s'est produite :", erreur)
    collection = connexion.getCollection()
    
    collection.update_one(
        {"identifiant": id},
        {"$push": {"historique": titre}}
    )
    connexion.closeConnexion()
    
def recupSeriesInHistoUser(username:str, mdp:str):
    id = authentification(username, mdp)
    if not id:
        raise ConnectionError("Nom utilisateur ou mot de passe incorrect")
    try:
        connexion = Connexion("SAE_S5", "Utilisateur")
    except ConnectionFailure as erreur:
        print("Une erreur de connexion à la base de données s'est produite :", erreur)
    collection = connexion.getCollection()
    utilisateur = collection.find_one({"identifiant": id}, {"_id":0, "historique":1})
    historique = utilisateur.get("historique", [])
    connexion.closeConnexion()
    return historique