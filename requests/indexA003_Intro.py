"""
Lien : https://www.youtube.com/watch?v=q30GEwUe5gY :
Cours : How to Access Web APIs using Python Requests and JSON

# Liste des codes HTTP : 
# https://fr.wikipedia.org/wiki/Liste_des_codes_HTTP

Récupération des données à partir du site TVA MAZE : 
-> API -> recherche unique ("Show single search") : https://www.tvmaze.com/api

Date : 16-12-23
"""

import requests
import json # chargement des fichiers JSON
import pprint # affichage dans le terminal amélioré

# URL API pour une recherche unique du site TV MAZE
url = "https://api.tvmaze.com/singlesearch/shows"

# Paramétrage pour accéder au fichier JSON
show = input("Saisir svp un nom de série (en UK) : ")
params = {"q":show} # terminaison de l'URL : "?q=query"

# Instanciation de la librairie requests : get = obtenir (CRUD)
response = requests.get(url, params)

# Si l'URL d'accès est correct
if response.status_code == 200:
    
    # Affichage du contenu du fichier JSON (instruction 'text')
    # print(response.text) # https://api.tvmaze.com/singlesearch/shows?q=girls

    # Conversion du fichier JSON en dict
    data = json.loads(response.text)
    # pprint.pprint(data)
    
    # Récupération de certaines valeurs du dict'data' à partir des clés
    name = data['name']
    premiered = data['premiered']
    summary = data['summary']
    print(f"{name} premiered on {premiered}.")
    print(summary)
    
else:
    # Sinon affichage du code statut HTTP (instruction '.status_code')
    print(f"Erreur : {response.status_code}")
