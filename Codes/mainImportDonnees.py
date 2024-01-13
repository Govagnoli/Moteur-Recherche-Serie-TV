import sys
sys.path.insert(0,".")
from CleanSRT.cleanSRT import Mots_EN_FR
from Recherche.TFIDF import genererCSV_TFIDF
from InsertDataSRT.export_concat import concatCSV
from InsertDataSRT.InsertSRTDataCollections import insertCollectionMots_Series, insertCollectionSeries_Mots

def main():
    # Création fichier txt contenant tous les mots lémmatisé des séries. Chaque série se voit attribuer au moins un fichier txt (un en fr et l'autre en anglais)
    Mots_EN_FR()

    # Génère un fichier CSV par fichier txt précédemment créé. Chaque fichier comporte la liste des mots (sans doublons) associé à un poid et la série ou ce mot apparait.
    genererCSV_TFIDF()

    # Concatène les fichiers CSV de la même série (mix anglais et français)
    concatCSV()

    # Créer une collection (si innexistant) dans la base mongodb local de l'ordinateur.
    # Collection Series_Mot. Chaque ligne correspond à une série (titre) et se voit associé la liste des mots utilisé dans la série. (utilisé pour la recommandation) 
    insertCollectionSeries_Mots()

    # Créer une collection (si innexistant) dans la base mongodb local de l'ordinateur.
    # Collection Mots_Series. Chaque ligne correspond à un mot utilisé dans les fichiers srt (il n'y a pas de doublons). Chaque mot est associé à une liste de série ou a été utilisé ce mot (utilisé pour la barre de recherche) 
    insertCollectionMots_Series()
    
if __name__ == "__main__":
    main()