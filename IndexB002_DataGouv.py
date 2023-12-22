"""
https://www.data.gouv.fr/fr/datasets/?q=api

Traitement opéré : api-lannuaire-administration

Lien :
https://api-lannuaire.service-public.fr/explore/dataset/api-lannuaire-administration/api/

Les requêtes sont similaires à du SQL

Date : 19-12-23
"""
import requests
import json
import pprint

"1ère requête : récupérer tous les organismes présents"

# Liste de tous les types d'organisme
url = "https://api-lannuaire.service-public.fr/api/explore/v2.1/catalog/datasets/api-lannuaire-administration/records?group_by=type_organisme&order_by=type_organisme"

response = requests.get(url)

data = json.loads(response.content)
dict_organismes = data['results']

# pprint.pprint(dict_organismes)

"2ème requête : afficher les établissements selon l'organisme sélectionné"

# Liste des 20 premiers établissements publics
# url = "https://api-lannuaire.service-public.fr/api/explore/v2.1/catalog/datasets/api-lannuaire-administration/records?select=nom&where=type_organisme%20%3D%20%27%C3%89tablissement%20public%27&order_by=nom&limit=20"

# Liste des X premiers établissements publics
limit = "10"
organisme = " ='Établissement public'"
url = "https://api-lannuaire.service-public.fr/api/explore/v2.1/catalog/datasets/api-lannuaire-administration/records?select=nom&where=type_organisme"+organisme+"&order_by=nom&limit="+limit

response = requests.get(url)

data = json.loads(response.content)
dict_lawyers = data['results']

pprint.pprint(dict_organismes)
