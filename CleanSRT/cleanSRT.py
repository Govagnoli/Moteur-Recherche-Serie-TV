import re
import string
from langdetect import detect
import glob
from tqdm import tqdm
import os
import spacy
import string

DIR_SOUS_TITRES = "..\StockageFic\sous-titres"
DIR_SOUS_TITRES_CLEAN_TRIER_LANGUE = "../StockageFic/Mots_VO_VF/"
DIR_SOUS_TITRES_CLEAN = "../StockageFic/Mots/"

# Créer un fichier (si innexistant) et écrit le texte "texte". Si le fichier existe ajoute à la suite du fichier le texte "texte"
def ecrireText(nomDuFichier, texte):
  try:
    with open(nomDuFichier, 'a', encoding='utf-8') as fichier:
      # Écrire chaque mot suivi d'une nouvelle ligne dans le fichier
      for mot in texte:
        fichier.write(mot + ' ')
    return True
  except Exception as e:
    print(f"Une erreur s'est produite : {e}")
    return False

# input_file : fichier srt sur lequel on applique le traitement
# Supprime les parasites d'un fichier srt "input_file" (n° sous-titrage et timestamps)
def suppr_parasites_srt(input_file):
    with open(input_file, 'r', encoding='latin-1') as file:
        lines = file.readlines()
    output_lines = []
    subtitle_text = []
    for line in lines:
        line = line.strip()
        # Utiliser une expression régulière pour identifier les numéros de sous-titrage
        if re.match(r'^\d+$', line):
            continue  # Ignorer les numéros de sous-titrage
        # Si la ligne est vide, cela signifie la fin d'un sous-titre, alors on ajoute le texte au résultat
        if not line:
            subtitle_text = ' '.join(subtitle_text)  # Convertir la liste en une seule chaîne de caractères
            # Supprimer la ponctuation du texte
            subtitle_text = ''.join([char if char not in string.punctuation or char == "'" else ' ' for char in subtitle_text])
            output_lines.append(subtitle_text)
            subtitle_text = []  # Réinitialiser le texte du sous-titre
        else:
            # Supprimer les timelines (horodatages) avec une expression régulière
            line = re.sub(r'\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+', '', line)
            line = re.sub(r'<.*?>', '', line)
            subtitle_text.append(line)
    return output_lines

# Supprime la ponctuation d'un string "chaine"
def supprimer_ponctuation(chaine):
    return chaine.translate(str.maketrans('', '', string.punctuation))

# input_file : fichier sub sur lequel on applique le traitement
# Supprime les parasites d'un fichier sub (ponctuation et chiffre entre accolades)
def suppr_parasites_sub(input_file):
    texte_retourne = []
    with open(input_file, 'r', encoding='latin-1') as file:
        lignes = file.readlines()
    for ligne in lignes:
        ligne = ligne.strip()
        if ligne:
            ligne = re.sub(r'^{\d+}{\d+}', '', ligne)
            ligne = re.sub(r'<.*?>', '', ligne)
            texte_retourne.append(ligne)
    # Supprimer la ponctuation du texte
    texte_retourne = [supprimer_ponctuation(ligne) for ligne in texte_retourne]
    return texte_retourne

# transforme une liste python "list" en un string
def transform_list_to_text(list):
    texte = ""
    for ligne in list:
        texte += ligne+' '
    return texte

# cheminDir : Repertoire ciblé
# extension : l'extension d'un fichier
# Retourne le nombre de fichier srt dans un répertoire
def nbrFic(cheminDir, extension):
  nbrFic = 0
  for fichier in os.listdir(cheminDir):
    # Vérifiez si le fichier a l'extension .srt
    if fichier.endswith(extension):
        nbrFic += 1
  return nbrFic

# text : texte en string à lemmatisé
# langue : langue du texte
# retourne une une liste de mot lemmatisé (traite l'anglais et le français uniquement)
def lemmatize_words_with_pos(text, langue):
    if langue=="fr":
        nlp = spacy.load("fr_core_news_sm")
    else:
        nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    list_lemmatizer = [token.lemma_ for token in doc]
    # Supprime les indices vides
    return [mot for mot in list_lemmatizer if mot.strip() != '']

# chemin_dir_serie : Repertoire d'une série
# nom_dir : nom du répertoire
# extension : extension voulant être parcouru dans le répertoire ciblé
# Ecrit dans un fichier txt l'ensemble des mots d'une série (avec la même extension). Les fichiers seront trié par série et par langue
def parcoursFichierTrierParLangue(chemin_dir_serie, nom_dir, extension='*.srt'):
    total_iteration_Serie = nbrFic(chemin_dir_serie, extension[1:])
    sous_progress_bar = tqdm(total=total_iteration_Serie, desc="Chargement", unit="it")
    texteFinal =""
    for chemin_fichier_srt in glob.glob(os.path.join(chemin_dir_serie, extension)):
        fichier_srt = os.path.basename(chemin_fichier_srt)
        chemin_fichier_clean = f"{DIR_SOUS_TITRES_CLEAN_TRIER_LANGUE}{nom_dir}_"
        if extension == "*.sub":
            texteFinal = suppr_parasites_sub(chemin_fichier_srt)
        elif extension == "*.srt" or extension == "*.vo":
           texteFinal = suppr_parasites_srt(chemin_fichier_srt)
        texteFinalStr = transform_list_to_text(texteFinal)
        try:
            langue = detect(texteFinalStr)
        except Exception as e:
           print(f"Le texte : {chemin_fichier_srt} ;fin texte. erreur {e}")
        if langue != "fr" and langue != "en":
            print(f"{fichier_srt} Langue non prise en charge. Le fichier est en : {langue}")
            continue
        texteFinal = lemmatize_words_with_pos(texteFinalStr, langue)
        if not ecrireText(f"{chemin_fichier_clean}{langue}.txt", texteFinal):
            print(f"Erreur écriture pour le fichier : {fichier_srt}")
        sous_progress_bar.update(1)
    sous_progress_bar.close()
    sous_progress_bar = None

# Parcours les fichier srt de chaque série, stock par série les mots en vf et en anglais. Les mots sont traité de tel sorte à ce qu'ils soient lémmatisés.
# WARNING : fonction longue a exécuter (un fichier prend entre 1s et 1.40s à être traité)
def Mots_EN_FR():
    total_iterations = len(os.listdir(DIR_SOUS_TITRES))
    progress_bar = tqdm(total=total_iterations, desc="Chargement", unit="it")
    # Liste des répertoires présent dans ../sous-titres
    for nom_dir in os.listdir(DIR_SOUS_TITRES):
        chemin_dir_serie = os.path.join(DIR_SOUS_TITRES, nom_dir)
        # Parcours .srt
        print(f"\nParcours fichier .srt\n")
        parcoursFichierTrierParLangue(chemin_dir_serie, nom_dir)
        # Parcours .vo
        print(f"\nParcours fichier .vo\n")
        parcoursFichierTrierParLangue(chemin_dir_serie, nom_dir, extension='*.vo')
        # Parcours .sub
        print(f"\nParcours fichier .sub\n")
        parcoursFichierTrierParLangue(chemin_dir_serie, nom_dir, extension='*.sub')
        progress_bar.update(1)
    progress_bar.close()