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

Prochain travail : présentation des données sous streamlit

Date : 25-12-23
"""

import requests
import json
import streamlit as st
import polars as pl

"Variables à saisir"
code_postal = input("Code postal : ")
limit = int(input("Nombre max d'affichage : "))

# Accès à l'URL avec le requêtage appliqué : 
url = f"https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/controle_techn/records?where=code_postal%3D%27{code_postal}%27&group_by=cct_denomination%20AS%20nom%2C%20cct_adresse%20AS%20adresse%2C%20code_postal%2C%20cct_code_commune%20AS%20commune%2C%20prix_visite%2C%20prix_contre_visite_min%2C%20prix_contre_visite_max&order_by=prix_visite&limit={limit}"

# Requête url
response = requests.get(url)

# Code statut html
response.status_code

# Récupération du contenu au format json
data = json.loads(response.content)

# Affichage des données
df = pl.DataFrame(data['results'])
print(df)
