"""
https://data.economie.gouv.fr/pages/accueil/

Traitement opéré : API sur l'encadrement des loyers à Paris
Affichez entre autres, le prix appliqué, prix min et prix max

Données limitées à 100 sorties

Lien API : https://opendata.paris.fr/explore/dataset/logement-encadrement-des-loyers/api/?disjunctive.annee&disjunctive.id_zone&disjunctive.nom_quartier&disjunctive.piece&disjunctive.epoque&disjunctive.meuble_txt

Lancement sur streamlit : 
streamlit run indexB006_Loyers.py

Date : 05-01-24
"""

import requests
import json
import streamlit as st
import pandas as pd
import polars as pl


# Présentation des données issues de l'API des loyers encadrés via streamlit
class FrontEnd():
    
    def __init__(self) -> None:
        
        # Instanciation des variables
        
        # Année
        self.year = ['2019', '2020', '2021', '2022', '2023']
        
        # Récup du fichier .csv converti en df polars sur les noms des quartiers
        df_districts = pl.read_csv('data/districts.csv')
        
        # Conversion de la df polars ci-avant en liste
        list_districts = df_districts.to_numpy().tolist()
        
        # Compréhension de liste ci-avant
        self.districts = [district for list_district in list_districts
                     for district in list_district]
        
        # Nombre de pièces
        self.rooms = ['1', '2', '3', '4']
        
        # Époque de construction
        self.period = ["Avant 1946", "1946-1970", "1971-1990", "Apres 1990"]
        
        # Meublé ou non
        self.furnished = ["meublé", "non meublé"]
        
        # Appel de la méthode ci-après
        self.gui()
        
    def gui(self):
        
        # Pleine page
        st.set_page_config(
            page_title="API - Encadrement des loyers à Paris", layout="wide") 
        
        # Titre principal de la page @
        st.markdown(
            "<h1 style='text-align: center; color: yellow;'>Encadrement des loyers à Paris</h1>",
            unsafe_allow_html=True)
        
        # Configuration de la largeur des colonnes
        col1, col2, col3 = st.columns([2, 1, 7])
        
        # Données à afficher dans la colonne n° 1
        with col1:
           
            # Menu déroulant sur l'année
            year = st.selectbox("Année", self.year)
            st.text('\n')
            
            # Menu déroulant sur le quartier
            districts = st.selectbox("Quartier", self.districts)
            st.text('\n')
            
            # Menu déroulant sur le nombre de pièces
            rooms = st.selectbox("Nombre de pièces", self.rooms)
            st.text('\n')
            
            # Menu déroulant sur l'époque de construction'
            period = st.selectbox("Époque de construction", self.period)
            st.text('\n')
            
            # Menu déroulant sur le meublé
            furnished = st.selectbox("Meublé ou non meublé", self.furnished)
            st.text('\n')
        
            # Bouton d'exécution pour valider les données saisies saisi ci-avant
            clicked = st.button('Valider', type='secondary')
        
        # Si le bouton 'Valider' a été appuyé...
        if clicked:       

            # Accès à l'URL avec le requêtage appliqué :
            url = f"https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/logement-encadrement-des-loyers/records?select=annee%2C%20nom_quartier%2C%20piece%2C%20epoque%2C%20meuble_txt%2C%20ref%2C%20min%2C%20max&where=annee%3D{year}%20and%20nom_quartier%3D%22{districts}%22%20and%20piece%3D{rooms}%20and%20epoque%3D%22{period}%22%20and%20meuble_txt%3D%22{furnished}%22&order_by=ref&limit=100"

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
                with col3:
            
                    # DF à afficher
                    st.dataframe(
                        df,
                        column_config={
                            "annee": st.column_config.Column("Année",),
                            "nom_quartier": st.column_config.Column("Quartier"),
                            "piece": st.column_config.Column("Pièce(s)"),
                            "epoque": st.column_config.Column("Époque"),
                            "meuble_txt": st.column_config.Column("Ameublement"),
                            "ref": st.column_config.Column("Loyer au m²"), 
                            "min": st.column_config.Column("Minimum"),
                            "max": st.column_config.Column("Maximum"),  
                        },
                        hide_index=True, # index masqué
                    )
                
            # À défaut (code http : 404) 
            else:
                
                st.warning(
                    f'Données non récupérées', icon="⚠️")
            
                    
if __name__ == '__main__':
    
    application = FrontEnd()
