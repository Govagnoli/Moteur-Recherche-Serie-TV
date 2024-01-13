from pandas import DataFrame
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import sys
from pymongo.errors import ConnectionFailure
from os.path import join
sys.path.insert(0,".")
from BDD.Connexion import Connexion
CHEMIN_STOCKAGE_MATRIX_SIMILARITE_csv = join("../../StockageFic/Matrix_Similarite/similarite.csv")

# Retourne une liste de dictionnaires. Chaque dictionnaire correspond à une série stocké dans la base de données.
# Un dictionnaire contient une clé titre et mots. Le titre référence le titre de la série et la clé mots (lémmatisé) contient une liste de mots associé à son poid TFIDF.
# Donc, chaque élément, de la liste retournée, référence le nom de la série ainsi que tous les mots lémmatisé des sous-titres associé à leur TFIDF
def allSerieToMots():
    try:
        connexion = Connexion("SAE_S5", "Series_Mots")
        collection = connexion.getCollection()
        series_data = list(collection.find())  #Récupère toute ma collection Series_Mots
        return [dict(serie) for serie in series_data] # Créer une liste de dictionnaire. Chaque dictionnaire contient le nom de la série ainsi que la liste mots de la série
    except ConnectionFailure as erreur:
        print("Une erreur de connexion à la base de données s'est produite :", erreur)
    finally:
        connexion.closeConnexion()  # Fermez la connexion ici

# Retourne une liste. Chaque élément correspond à un titre de série.
def allTitres():
    series_data = allSerieToMots()
    titres = []
    for serie in series_data:
        titres.append(serie["titre"])
    return titres

# titre est un string devant référencer le nom d'une série dans la base de données
# Renvoie la liste des mots lémmatisé d'une série
def listMotsDUneSerie(titre):
    series_data = allSerieToMots()
    mots=[]
    for serie in series_data:
        if serie["titre"] == titre :
            for motPoids in serie["mots"]:
                mots.append(motPoids["mot"])
            return mots
    return mots

# Retourne une liste. Chaque élément correspond à un mot lémmatisé. 
# L'ensemble des éléments de la liste correspondent aux mots écrit dans les fichier sous-titres.
def listMotsParSerie():
    listMots = []
    titres = allTitres()
    for titre in titres : 
        listMots.append(listMotsDUneSerie(titre))
    return listMots

# Créer une matrice de similarité entre les séries.
# Chaque ligne référence une série. Chaque colonne référence une série
# la valeur ij d'un élément de la matrice correspond à la similarité de la série i avec la série j
# La valeur ij est calculé en fonction du TF-IDF de la série i avec le TF-IDF de la série j
# La matrice de similarité est ensuite enregistré sous forme de fichier csv pour pouvoir être réutilisé et chargé rapidement par la suite.
# La chemin d'enregistrement de la matrice est spécifié par la constante "CHEMIN_STOCKAGE_MATRIX_SIMILARITE_csv"
def creationMatriceSimilarite():
    series_names = allTitres()
    lemmatized_texts = listMotsParSerie()
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([" ".join(mots) for mots in lemmatized_texts])
    similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
    similarity_df = DataFrame(similarity_matrix, index=series_names, columns=series_names)
    similarity_df.to_csv(CHEMIN_STOCKAGE_MATRIX_SIMILARITE_csv)
   
# creationMatriceSimilarite() Créer la matrice de similarité