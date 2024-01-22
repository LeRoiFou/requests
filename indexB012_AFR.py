"""
Zone d'Aide à Finalité Régionale (ZAFR) : période 2022 - 2027

Données récupérées à partir fichier .csv deu site data.gouv :
https://www.data.gouv.fr/fr/datasets/zones-daide-a-finalite-regionale-afr/

Lancement sur streamlit : 
streamlit run indexB012_AFR.py

Date : 22-01-24
"""

import pandas as pd
import streamlit as st
# Mise en forme : filtre, trie, déplacement des colonnes
from st_aggrid import AgGrid
# Options complémentaires
from st_aggrid.grid_options_builder import GridOptionsBuilder

# Présentation des données issues de l'API des loyers encadrés via streamlit
class FrontEnd():
    
    def __init__(self) -> None:
        
        # Instanciation des variables
        
        # Récupération des fichiers .csv convertis en DF pandas
        city_df = pd.read_csv(
            'data/afr_2022.csv', sep=";", encoding='latin-1')
        district_df = pd.read_csv(
            'data/departement_afr.csv', encoding='unicode_escape', sep=";")
        
        # Fusion des deux fichiers ci-avant
        afr_df = city_df.merge(district_df, on='N°')
        
        # Renommage de champs
        afr_df.rename(columns={
            'lib_com':'Commune', 'classement_afr':'AFR',
            'N°':'N° de département'}, inplace=True)
        
        # Sélection des champs à afficher
        self.afr_df = afr_df[[
            'Commune', 'N° de département', 'Département', 'Région', 'AFR', ]]
        
        # Appel de la méthode ci-après
        self.gui()
        
    def gui(self):
        
        # Pleine page
        st.set_page_config(
            page_title="DATA GOUV - Zones AFR", layout="wide",) 
        
        # Titre principal de la page @
        st.markdown(
            "<h3 style='text-align: center; color: yellow;'>Zone d'Aide à Finalité Régionale : période 2022 - 2027</h3>",
            unsafe_allow_html=True,)
        
        # Configuration de la largeur des colonnes
        col1, col2, col3 = st.columns([2, 8, 2])
        
        with col2:
        
            # Zone de saisie de la commune
            city_input = st.text_input("Nom de la commune 👇",)
            
            # Si le nom de la commune a été saisie...
            if city_input:
                
                # Récupération de la DF : filtre sur le nom saisi
                afr_df = self.afr_df[self.afr_df['Commune'].str.contains(
                    f'^{city_input}', case=False)].sort_values(by='Commune')
                
                # Affichage de la table en insérant la DF filtrée ci-avant
                AgGrid(afr_df)
            
                    
if __name__ == '__main__':
    
    application = FrontEnd()
