import re
import pandas as pd
from pathlib import Path
import os

DIR_CSV = "../StockageFic/TFIDF"
DIR_CSV_CONCAT = "../StockageFic/CSVConcat"

# Concatènes les fichiers CSV d'une même série. Permet de créer un fichier csv par série et ne classe plus par langue détecté.
def concatCSV():
    allTitres = {}
    for fichierCSV in Path(DIR_CSV).rglob("*.csv"):
        regex = r"^(.*?)_(.*?)$"
        titre = re.match(regex, str(os.path.basename(fichierCSV))).group(1)
        if(titre in allTitres):
            en_csv = os.path.join(DIR_CSV, f"{titre}_en.csv")
            fr_csv = os.path.join(DIR_CSV, f"{titre}_fr.csv")
            pd.concat([pd.read_csv(en_csv), pd.read_csv(fr_csv)]).to_csv(f"{DIR_CSV_CONCAT}/{titre}.csv", index=False)
        else:
            allTitres[titre] = True
            pd.read_csv(fichierCSV).to_csv(f"{DIR_CSV_CONCAT}/{titre}.csv", index=False)

