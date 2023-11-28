# Permet de dézipper récursivement tous les fichiers compresser dans le répertoire sous-titres (cheminRacine). S'exécute avec powerShell Attention la série sixfeetunder devient corrompus après l'utilisation de ce programme

# Chemin vers le répertoire parent contenant tous les répertoires_série
$cheminRacine = "C:\Users\eliot\Desktop\SAE\S5\StockageFic\sous-titres"

#Dézip récursivement tous les répertoire présent dans sous-titres
Get-ChildItem -Path $cheminRacine -Recurse -Filter "*.zip" | ForEach-Object { Expand-Archive -LiteralPath $_.FullName -DestinationPath $_.DirectoryName }

# Obtenez la liste des répertoires de séries
$series = Get-ChildItem -Path $cheminRacine -Directory

# Parcourez chaque répertoire de série
foreach ($serie in $series) {
    # Obtenez la liste des répertoires de saisons dans le répertoire de série actuel
    $saisons = Get-ChildItem -Path $serie.FullName -Directory
    
    # Parcourez chaque répertoire de saison
    foreach ($saison in $saisons) {
        # Copiez le contenu de la saison dans le répertoire de série
        Move-Item -Path "$($saison.FullName)\*" -Destination $serie.FullName -Force
        
        # Supprimez le répertoire de saison
        Remove-Item -Path $saison.FullName -Recurse -Force
    }
    Remove-Item -Path "$($serie.FullName)\*.zip" -Force
}