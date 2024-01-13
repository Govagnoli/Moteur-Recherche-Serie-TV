from os import getcwd
from os.path import join
from numpy import save
import simplemma
from pymongo.errors import ConnectionFailure 
import sys
from pandas import DataFrame, read_csv
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
sys.path.insert(0,"./Codes")
from BDD.Connexion import Connexion
barre_de_recherche = "skyler"

# CHEMIN_STOCKAGE_MATRIX_SIMILARITE = "..\../StockageFic\Matrix_Similarite\similarite.csv"
CHEMIN_STOCKAGE_MATRIX_SIMILARITE = join("../StockageFic/Matrix_Similarite/similarite.csv")

# texteRecherche est le string recherché par l'utilisateur
# La fonction va renvoyer la liste des mots lématisés rentrer par l'utilisateur
def lemmatizeListMotsRecherche(texteRecherche):
    if not isinstance(texteRecherche, str):
        raise ValueError("Le paramètre de fonction motsRecherche doit-être un string. Le string recherché par l'utilisateur.")
    motsLemmatize = []
    texteRecherche = texteRecherche.lower()
    mots = texteRecherche.split()
    for mot in mots:
        motsLemmatize.append(simplemma.lemmatize(mot, lang=('fr', 'en')))
    return motsLemmatize

# texteRecherche : Texte saisie par l'utilisateur lors de sa recherche.
# Si retourne true à l'indice 0 du tableau. Alors le texte saisie correspond au titre d'une série dans la base de données. L'indice 1 du tableau correspond au titre 
# Si retourne false à l'indice 0 du tableau. Alors le texte saisie correspond pas au titre d'une série de la base de données.
# Permet de savoir si l'utilisateur recherche avec un nom de série plutôt que par mots clés
def rechercheTitreInDB(texteRecherche):
    connexion = Connexion("SAE_S5", "Mots_Series")
    collection = connexion.getCollection()
    titreClean = texteRecherche.lower()
    titreClean = texteRecherche.replace(" ", "")
    documents = collection.find({"series.titre": titreClean}, {"_id":0})
    if len(list(documents))>0:
        connexion.closeConnexion()
        return [True, titreClean]
    connexion.closeConnexion()
    return [False, titreClean]

# texteRecherche est le string recherché par l'utilisateur
# Retourne de toutes les correspondances entre les mots recherché par l'utilisateur et les mots présents dans la base de données.
# L'élément retourné est une liste de dictionnaire. Chaque dictionnaire est un document de la base de données.
def rechercheMotsInDB(texteRecherche):
    motsLemmatize = lemmatizeListMotsRecherche(texteRecherche)
    connexion = Connexion("SAE_S5", "Mots_Series")
    collection = connexion.getCollection()
    motsEtSeries = []
    for mot in motsLemmatize:
        documents = collection.find({"mot": mot}, {"_id":0})
        for document in documents:
            motsEtSeries.append(document)
    connexion.closeConnexion()
    return motsEtSeries

# texteRecherche est le string recherché par l'utilisateur
# Retourne un dictionnaire contenant en clé le titre de chaque série ayant une correspondance avec les mots recherché par l'utilisateur.
# La fonction associe pour chaque titre une liste du poids des mots recherché par l'utilisateur.
def dicTitrePoids(texteRecherche):
    motsEtSeries = rechercheMotsInDB(texteRecherche)
    TitresEtPoids = {}
    for document in motsEtSeries:
        for serie in document["series"]:
            titre = serie["titre"]
            poids = serie["poids"]
            if titre in TitresEtPoids:
                TitresEtPoids[titre].append(poids)
            else :
                TitresEtPoids[titre] = []
                TitresEtPoids[titre].append(poids)
    return TitresEtPoids

# texteRecherche est le string recherché par l'utilisateur
# Fait la somme des poids associé à un titre de série
# Renvoie une liste des titres de séries trié par ordre décroissant de poids
def plusHautPoids(texteRecherche):
    TitresEtPoids = dicTitrePoids(texteRecherche)
    TitresEtSumPoids = {}
    for titre, poids in TitresEtPoids.items():
        TitresEtSumPoids[titre] = sum(poids)
    return sorted(TitresEtSumPoids, key=TitresEtSumPoids.get, reverse=True)

# texteRecherche est le string recherché par l'utilisateur
# Renvoie une liste de séries pertinentes associé au texte recherché par l'utilisateur. 
def barreDeRecherche(texteRecherche):
    seriesLiees = plusHautPoids(texteRecherche)
    isTitreRecherche = rechercheTitreInDB(texteRecherche)
    if isTitreRecherche[0]:
        return deplacerTitreIndice0(isTitreRecherche[1], seriesLiees) 
    return seriesLiees

# titreADeplacer est un string présent dans la liste de string titres
# titreADeplacer va être repositionné à l'indice 0 de la liste sans pour autant le dupliquer dans la liste
# Retourne la liste modifié
def deplacerTitreIndice0(titreADeplacer, titres):
    if titreADeplacer in titres:
        index = titres.index(titreADeplacer)
        titres.pop(index)
        titres.insert(0, titreADeplacer)
        return titres
    titres.insert(0, titreADeplacer)
    return titres

# Récupère toutes les données des 127 séries stocké dans la collection Series_mots et renvoie un dictionnaire
def allSerieToMots():
    try:
        connexion = Connexion("SAE_S5", "Series_Mots")
        collection = connexion.getCollection()
        series_data = list(collection.find())  # Convertir le curseur en liste de dictionnaires
        return [dict(serie) for serie in series_data] # Convertir les objets MongoDB en dictionnaires Python
    except ConnectionFailure as erreur:
        print("Une erreur de connexion à la base de données s'est produite :", erreur)
    finally:
        connexion.closeConnexion()  # Fermez la connexion ici

# On entraine un model de langage sur l'ensemble des mots des séries. L'objectif de l'entrainement consiste à connaitre la similarité entre chacune des séries.
# Stock dans un fichier npy (numpy en binaire) la matrix de similarité calculé par le model cosine_similarity de scikit-learn
def entrainementModelRecommandation(series_data=allSerieToMots()):
    tfidf_vectorizer = TfidfVectorizer()
    series_texts = [' '.join(mot['mot'] for mot in serie["mots"]) for serie in series_data] # Concatène l'ensemble des mots des séries (lémmatisé)
    tfidf_matrix = tfidf_vectorizer.fit_transform(series_texts)
    similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)
    save(CHEMIN_STOCKAGE_MATRIX_SIMILARITE, similarities)

# Fonction pour obtenir les séries recommandées en fonction de la série donnée
def recommendations(titres_series, top_n=126):
    series_data = allSerieToMots()
    similarites = DataFrame()
    try:
        print(getcwd())
        similarites = read_csv(CHEMIN_STOCKAGE_MATRIX_SIMILARITE, index_col=0)
    except Exception as e:
        print(f"Erreur, matrice de similarité introuvable:\n{e}")
    series_recommandees = {}
    for titre in titres_series:
        similarities_with_reference = similarites.loc[titre]
        most_similar_series = similarities_with_reference.sort_values(ascending=False)
        top_n_similar_series = most_similar_series.iloc[1:top_n]
        series_recommandees[titre] = top_n_similar_series
    return series_recommandees