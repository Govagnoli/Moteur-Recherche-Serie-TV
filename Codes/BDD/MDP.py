import bcrypt
from Connexion import Connexion
utilisateur = "utilisateur"
administrateur = "administrateur"

# Permet de créer un nouvel utilisateur dans la base de données.
# Si le nom existe déjà alors la fonction lève l'erreur ValueError
# Renvoie True si l'utilisateur à été ajouté et lève ConnectionError si une erreur à eu lieu lors de la connexion
def creationCompte(username, mdp, role=utilisateur):
    connexion = Connexion("SAE_S5", "Utilisateur")
    collection = connexion.getCollection()
    nbrDocuments = collection.count_documents ({"identifiant": username})
    if(nbrDocuments>0):
        raise ValueError("Erreur, nom utilisateur déjà existant.")
    nouvel_utilisateur = {
        "identifiant": username,
        "mdp": str(hash_mdp(mdp)),
        "role": role
    }
    insertion_user = collection.insert_one(nouvel_utilisateur)
    if insertion_user.inserted_id:
        return True
    else:
        raise ConnectionError("Erreur lors de la création du compte. Veuillez réessayer de nouveau.")

# Hash un mot de passe (mdp) avec l'algorithme bcrypt
# renvoi le mot de passe hashed
def hash_mdp(mdp):
    salt = bcrypt.gensalt()
    hash_mdp= bcrypt.hashpw(mdp.encode('utf-8'), salt)
    return hash_mdp.decode('utf-8')

# Permet d'authentifier un utilisateur en fonction de son identifiant (username) et son mot de passe (mdp)
# Renvoi True si l'utilisateur existe et que le mdp renseigné est correct. Sinon renvoi False
def authentification(username, mdp):
    mdp = mdp.encode('utf-8')
    connexion = Connexion("SAE_S5", "Utilisateur")
    collection = connexion.getCollection()
    nbrDocuments = collection.count_documents({"identifiant": username})
    user_curseur = collection.find({"identifiant": username}, {"_id":0, "identifiant":1, "mdp": 1, "role":1})
    if(nbrDocuments<1):
        return False
    mdp_bdd_hash = str(user_curseur[0].get("mdp")).encode('utf-8')
    print(f"mdp_bdd_hash : {mdp_bdd_hash}, mdp : {mdp}")
    if bcrypt.checkpw(mdp, mdp_bdd_hash):
        return True
    else:
        return False