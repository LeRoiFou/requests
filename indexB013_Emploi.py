"""
Effectifs salariés et masse salariale trimestriels du secteur privé, 
par zone d'emploi
Lien :  https://www.data.gouv.fr/fr/datasets/effectifs-salaries-et-masse-salariale-trimestriels-du-secteur-prive-par-zone-demploi/

Séries trimestrielles des effectifs salariés et de la masse salariale 
du secteur privé, par zone d'emploi.

Lancement sur streamlit : 
streamlit run indexB013_Emploi.py

Dashboard :
https://docs.google.com/drawings/d/1OKiRsCjmbV6p6VJojp3Ivz3Hvs2_cKFvSBSMGZ-Qxq0/edit

Date : 24-01-24
"""

import streamlit as st
import polars as pl

def app():
        
    # Pleine page
    st.set_page_config(
        page_title="Emploi secteur privé", layout="wide") 
    
    # Titre principal de la page @
    st.markdown(
        "<h1 style='text-align: center; color: yellow;'>Effectifs et masse salariale par zone d'emploi</h1>",
        unsafe_allow_html=True)
    
    # Configuration de la largeur des colonnes
    col1, col2 = st.columns([4, 8])
    
    # Données à afficher dans la colonne n° 1
    with col1:
       pass
                    
if __name__ == '__main__':
    
    app()
