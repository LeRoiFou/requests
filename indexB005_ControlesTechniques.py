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

Date : 25-12-23
"""

import requests
import json
import streamlit as st
import pandas as pd
import pprint


# Présentation des données issues de l'API des CT via streamlit
class FrontEnd():
    
    def __init__(self) -> None:
        
        # Instanciation des variables
        self.code_postal = ''
        self.limit = '' # Nombre de CT à afficher (100 : valeur max)
        
        # Appel de la méthode ci-après
        self.gui()
        
    def gui(self):
        
        # Pleine page
        st.set_page_config(page_title="API contrôles techniques", layout="wide") 
        
        # Titre principal de la page @
        st.markdown(
            "<h1 style='text-align: center; color: blue;'>Liste des contrôles techniques</h1>",
            unsafe_allow_html=True)
        st.text('\n')
        
        # Configuration de la largeur des colonnes
        col1, col2 = st.columns([1, 9])
        
        # Données à afficher dans la colonne n° 1
        with col1:
           
            # Zone de saisie pour le code postal
            self.code_postal = st.text_input("Code postal : ", max_chars=5)
            st.text('\n')
        
            # Zone de saisie pour le nombre de CT à afficher
            self.limit = st.text_input(
                "Nbre de CT à afficher (100 max) : ", value=100)
            self.limit = int(self.limit) # conversion str en int
            st.text('\n')
            
            # Bouton d'exécution pour valider les données saisies saisi ci-avant
            clicked = st.button('Valider', type='secondary')
        
        # Si le bouton 'Valider' a été appuyé et que 5 caractères ont été saisis
        # dans la zone de texte 'Code postal' et qu'une valeur est présente dans
        # le nombre de CT à afficher...
        if clicked and len(self.code_postal) == 5 and self.limit > 0:       

            # Accès à l'URL avec le requêtage appliqué :
            url = f"https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/controle_techn/records?where=code_postal%3D%27{self.code_postal}%27&group_by=cct_denomination%20AS%20nom%2C%20cct_adresse%20AS%20adresse%2C%20code_postal%2C%20cct_code_commune%20AS%20commune%2C%20prix_visite%2C%20prix_contre_visite_min%2C%20prix_contre_visite_max&order_by=prix_visite&limit={self.limit}"

            # Requête url
            response = requests.get(url)
            
            # Si le code postal a été retrouvé (code http : 200)
            if response.status_code == 200:

                # Récupération du contenu au format json
                data = json.loads(response.content)
                
                # Récupération du contenu au format json
                data = json.loads(response.content)

                # Données converties en DF pandas
                df = pd.DataFrame(data['results'])
                
                # Données à afficher dans la colonne n° 2
                with col2:
            
                    # DF à afficher
                    st.dataframe(
                        df,
                        column_config={
                            "nom": st.column_config.Column("Nom",),
                            "adresse": st.column_config.Column("Adresse"),
                            "code_postal": st.column_config.Column("CP"),
                            "commune": st.column_config.Column("Commune"),
                            "prix_visite": st.column_config.Column("Prix visite"),
                            "prix_contre_visite_min": st.column_config.Column(
                                "Prix min contre visite"),
                            "prix_contre_visite_max": st.column_config.Column(
                                "Prix max contre visite"),         
                        },
                        hide_index=True, # index masqué
                    )
                
            # À défaut (code http : 404) 
            else:
                
                st.warning(
                    f'Données non récupérées pour le code postal : {self.code_postal}',
                    icon="⚠️")
            
                    
if __name__ == '__main__':
    
    application = FrontEnd()
