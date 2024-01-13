from re import match
from pandas import concat, read_csv
from pathlib import Path
from os.path import basename, join

DIR_CSV = "../StockageFic/TFIDF"
DIR_CSV_CONCAT = "../StockageFic/CSVConcat"

# Concatènes les fichiers CSV d'une même série. Permet de créer un fichier csv par série et ne classe plus par langue détecté.
def concatCSV():
    allTitres = {}
    for fichierCSV in Path(DIR_CSV).rglob("*.csv"):
        regex = r"^(.*?)_(.*?)$"
        titre = match(regex, str(basename(fichierCSV))).group(1)
        if(titre in allTitres):
            en_csv = join(DIR_CSV, f"{titre}_en.csv")
            fr_csv = join(DIR_CSV, f"{titre}_fr.csv")
            concat([read_csv(en_csv), read_csv(fr_csv)]).to_csv(f"{DIR_CSV_CONCAT}/{titre}.csv", index=False)
        else:
            allTitres[titre] = True
            read_csv(fichierCSV).to_csv(f"{DIR_CSV_CONCAT}/{titre}.csv", index=False)

