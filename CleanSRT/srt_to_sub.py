import glob
import os

DIR_SOUS_TITRES = "..\StockageFic\srt_sub"

# dir_mauvaise_extension : répertoire créer contenant l'ensemble des fichier srt à transformer en sub
# Transforme tous les fichiers srt d'un répertoire en sub. Utilisé pour les fichiers ".srt" devant être en ".sub"
def transformToutSrtEnSub(dir_mauvaise_extension=DIR_SOUS_TITRES):
    for chemin_fichier_srt in glob.glob(os.path.join(dir_mauvaise_extension, "*.srt")):
        chemin_fichier_sub = chemin_fichier_srt.replace(".srt", ".sub")
        os.rename(chemin_fichier_srt, chemin_fichier_sub)

transformToutSrtEnSub()