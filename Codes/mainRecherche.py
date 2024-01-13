from re import sub
import sys
sys.path.insert(0,".")
from Recherche.fonctionRecherche import recommendations, barreDeRecherche
from BDD.MDP import authentification
from InsertDataSRT.InsertSRTDataCollections import ajoutSerieInHistoUser, recupSeriesInHistoUser

def obtenir_texte_utilisateur(texte):
    texte_utilisateur = input(texte)
    texte_banalise = sub(r"[^a-zA-Z0-9\s]", "", texte_utilisateur)
    return texte_banalise

def seConnecter():
    recommancer = input("Voulez vous vous connecter Y/n ?")
    if recommancer=="n":
        print("Echec de connexion")
        return None
    username = obtenir_texte_utilisateur("Entrez votre nom utilisateur : ")
    mdp = obtenir_texte_utilisateur("Entrez votre mot de passe : ")
    id = authentification(username, mdp)
    if not id:
        print("Mot de passe ou nom utilisateur incorrect.")
        seConnecter()
    print(f"\nBon retour parmis nous {id}\n")
    return id, mdp

def main():
    barre_recherche = obtenir_texte_utilisateur("Recherchez votre série : ")
    series_retournees = barreDeRecherche(barre_recherche) 
    print(f"Les séries recommandées en fonction de votre recherche sont :\n{series_retournees}\n")    
    
    print("\nConnecté vous: \n")
    id, mdp = seConnecter()
    if not id or not mdp:
        exit()

    # Lorsque vous regarder une série vous incrémenter une liste de série associé à votre compte utilisateur. Ici voud devriez avoir au minima la série lost et breaking bad associé à votre compte
    historique_series = ["breakingbad", "lost"] 
    for serie in historique_series:
        try:
            ajoutSerieInHistoUser(id, mdp, serie) 
        except ConnectionError as e:
            print("Echec de connexion")
            exit()
    
    historique = recupSeriesInHistoUser(id, mdp)

    series_recommandees = recommendations(historique, top_n=5) # 5 correspond aux nombre de séries voulant être recommandé en fonction de chaque série vue
    for titre, series_recommandees in series_recommandees.items():
        print(f"Parce que vous avez vue : {titre}\n{series_recommandees}\n")    

if __name__ == "__main__":
    main()