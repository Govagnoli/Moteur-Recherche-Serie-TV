from glob import glob
from pathlib import Path
import re
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

CHEMIN_MOTS_VO_VF = "..\StockageFic\Mots_VO_VF"
CHEMIN_Stockage_CSV_TFIDF = "..\StockageFic\TFIDF"

# Renvoie la liste du nom des fichiers textes du répertoire CHEMIN_MOTS_VO_VF 
def listFicMotsVOVF():
    tous_fichiers_txt =[]
    for cheminfichier in glob(os.path.join(CHEMIN_MOTS_VO_VF, "*.txt")) : #Path(CHEMIN_MOTS_VO_VF).rglob("*.txt")
        tous_fichiers_txt.append(os.path.basename(cheminfichier))
    return tous_fichiers_txt

# retourne une liste avec pour chaque indice le contenu d'un fichier texte du répertoire CHEMIN_MOTS_VO_VF
def listTxtTousFic():
    textesDesFichiers = []
    tous_fichiers_txt = listFicMotsVOVF()
    for fichier_txt in tous_fichiers_txt:
        with open(os.path.join(CHEMIN_MOTS_VO_VF, fichier_txt), encoding='utf-8') as f:
            texteFichier = f.read()
        textesDesFichiers.append(texteFichier)
    return textesDesFichiers

# Retourne dans un dictionnaire le model entrainé par TfidfVectorizer de scikit-learn ainsi que sa matrice 
def TfIdfDesFichiers():
    vectoriseur = TfidfVectorizer(stop_words=None, use_idf=True, norm=None, strip_accents="unicode")
    documents_transformes = vectoriseur.fit_transform(listTxtTousFic())
    return {"model" :vectoriseur, "matrice" : documents_transformes.toarray()}

# Génère un fichier csv pour chaque fichier texte de CHEMIN_MOTS_VO_VF
# Les fichiers csv contiendront : la liste des mots de la série associé à leur poid TFIDF ainsi que le titre de la série
def genererCSV_TFIDF(rep_sortie = CHEMIN_Stockage_CSV_TFIDF) :
    listeFic = listFicMotsVOVF()
    Path(rep_sortie).mkdir(parents=True, exist_ok=True) # créer le répertoire rep_sortie qui contiendra les fichier csv générés
    modelEtMatrice = TfIdfDesFichiers()
    for index, motsSeries in enumerate(modelEtMatrice["matrice"]):
        # Associe un mot à sont poids
        tuple_mot_poids = list(zip(modelEtMatrice["model"].get_feature_names_out(), motsSeries))
        # Créer un df à partir de tuple_mot_poids et sort les éléments par poids décroissant
        df_mots_poids = pd.DataFrame.from_records(tuple_mot_poids, columns=['mots', 'poids']).sort_values(by='poids', ascending=False).reset_index(drop=True)
        #supprime tout les mots ayant un poids = 0
        df_mots_poids = df_mots_poids.loc[df_mots_poids['poids'] > 0]
        nomFichier = listeFic[index]
        titreSerie  = re.match(r"^(.*?)_(.*?)$", nomFichier).group(1)
        df_mots_poids['serie'] = titreSerie
        # enregistrer les résultats dans un document CSV, en utilisant
        df_mots_poids.to_csv(os.path.join(CHEMIN_Stockage_CSV_TFIDF, nomFichier.replace(".txt", ".csv")))