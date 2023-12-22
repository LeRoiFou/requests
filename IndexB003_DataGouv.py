"""
https://api.gouv.fr/

Traitement opéré : API Recherche d’entreprises

Lien : https://recherche-entreprises.api.gouv.fr/docs/
URL: https://recherche-entreprises.api.gouv.fr/

Date : 22-12-23
"""

# https://recherche-entreprises.api.gouv.fr/search

import requests
import json
import pprint

# Accès à l'url avec les requêtes suivantes :
# Code commune INSEE = 68201
# Et n'est pas un service public
url = "https://recherche-entreprises.api.gouv.fr/search?code_commune=68201&est_service_public=False"

# Requête url
response = requests.get(url)

# Récupération du contenu au format json
data = json.loads(response.content)
pprint.pprint(data)

