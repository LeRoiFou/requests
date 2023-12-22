"""
https://api.gouv.fr/

Traitement opéré : API Carto - module Codes Postaux
Récupération des communes selon le code postal saisi

Lien : https://api.gouv.fr/les-api/api_carto_codes_postaux
Documentation : https://api.gouv.fr/documentation/api_carto_codes_postaux
URL: https://apicarto.ign.fr/api/codes-postaux/communes

Date : 22-12-23
"""

import requests
import json
import pprint

code_postal = "68290"

# Accès à l'URL avec le requêtage appliqué : code_postal
url = 'https://apicarto.ign.fr/api/codes-postaux/communes/'+code_postal

# Requête url
response = requests.get(url)

# Récupération du contenu au format json
data = json.loads(response.content)
# pprint.pprint(data)

# Liste des communes
city_list = [i['nomCommune'] for i in data]
print(city_list)
