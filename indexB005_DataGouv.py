"""
https://data.economie.gouv.fr/pages/accueil/

Traitement opéré : API Prix des contrôles techniques
Affichez les tarifs des contrôles et des contre-visites des centres techniques 
des véhicules légers

Données limitées à 100 sorties

Lien API : https://data.economie.gouv.fr/explore/dataset/controle_techn/api/?disjunctive.cct_code_dept&disjunctive.cat_vehicule_libelle&disjunctive.cat_energie_libelle
URL: https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/controle_techn/records

Lancement sur streamlit : 
streamlit run indexB005_DataGouv.py

Prochain travail : récupérer les départements de la liste de dictionnaires
avec le fichier jupyter labo

Date : 25-12-23
"""

import requests
import json
import streamlit as st
import pprint

"Liste des départements"

# URL pour la liste des départements
url = 'https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/controle_techn/records?group_by=cct_code_dept'

# Récupération de l'URL pour requêtage
dept_response = requests.get(url)

# Récupération du contenu au format json
dept_data = json.loads(dept_response.content)

# pprint.pprint(dept_data['results'])

print(dept_data['results'])

