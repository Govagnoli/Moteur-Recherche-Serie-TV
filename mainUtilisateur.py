import sys
sys.path.insert(0,".")
from BDD.MDP import creationCompte, authentification
from InsertDataSRT.InsertSRTDataCollections import ajoutSerieInHistoUser, recupSeriesInHistoUser
from re import sub

def obtenir_texte_utilisateur(texte):
    texte_utilisateur = input(texte)
    texte_banalise = sub(r"[^a-zA-Z0-9\s]", "", texte_utilisateur)
    return texte_banalise

def creerCompte():
    recommancer = input("Voulez vous Creer un compte Y/n ?")
    if recommancer=='n':
        print("Abandon création compte")
        return None
    username = obtenir_texte_utilisateur("Entrez votre nom utilisateur : ")
    mdp = obtenir_texte_utilisateur("Entrez votre mot de passe : ")
    try:
        creationCompte(username, mdp)
    except ValueError as e:
        print("Le nom utilisateur Existe déjà")
        creerCompte()
    print(f"Bienvenue {username}") 

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
    print(f"Bon retour parmis nous {id}")
    return id, mdp

def main():
    print("Créer votre compte: \n")
    creerCompte()

    print("\nConnecté vous: \n")
    id, mdp = seConnecter()

    if not id or not mdp:
        exit()
    
    serieVueMaintenant = "lost"
    print(f"Vous venez de voir {serieVueMaintenant}.")
    try:
        ajoutSerieInHistoUser(id, mdp, serieVueMaintenant)
    except ConnectionError as e:
        print("Echec de connexion")
        exit()
    
    print(f"\nNous allons maintenant regarder votre historique. Vous devriez trouver {serieVueMaintenant} à la fin de la liste. (A moins que la série soit déjà présente dans la liste)")
    historique = recupSeriesInHistoUser(id, mdp)
    print(historique)

if __name__ == "__main__":
    main()