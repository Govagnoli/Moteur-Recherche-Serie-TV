from os import path
from pandas import read_csv
import re
import sys
sys.path.insert(0,".")
from Recherche.fonctionRecherche import recommendations, barreDeRecherche

def obtenir_texte_utilisateur():
    texte_utilisateur = input("Recherchez votre série : ")
    # texte_banalise = re.sub(r"[^a-zA-Z0-9\s]", "", texte_utilisateur)
    return texte_utilisateur

def main():
    barre_recherche = obtenir_texte_utilisateur()
    series_retournees = barreDeRecherche(barre_recherche) 
    print(f"Les séries recommandées en fonction de votre recherche :\n{series_retournees}\n")

    # historique_series = ["breakingbad", "lost"]
    # series_recommandees = recommendations(historique_series, top_n=5) # 5 correspond aux nombre de séries voulant être recommandé en fonction de chaque série vue
    # for titre, series_recommandees in series_recommandees.items():
    #     print(f"Parce que vous avez vue : {titre}\n{series_recommandees}\n")    

if __name__ == "__main__":
    main()