##Commande à faire 

python3.8 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
#pour enregistrer les données des vidéos de input dans output ( lors du lancement une page youtube s'ouvre puis se ferme qui permet d'aller chercher les commentaires)
python scrapper.py --input input.json --output output.json

##TEST
#pour faire les tests
python -m pytest tests

#Test réaliser sur les fonctions pour les commentaires, la description et les Liens exceptionnels de la description
#Pas de test pour les likes car ils changent trop souvent
#Pas de test pour  ecrireoutput car rien n'est retourné et le but est d'écrire dans le json 
#Pas de test pour ecrire car rien n'est retourné

#Pytest-cov ne fonctionne pas 

##Condition pour le choix des vidéos
la vidéo doit avoir des Commentaires




