"""
Effectifs salariés et masse salariale trimestriels du secteur privé, 
par zone d'emploi
Lien :  https://www.data.gouv.fr/fr/datasets/effectifs-salaries-et-masse-salariale-trimestriels-du-secteur-prive-par-zone-demploi/

Séries trimestrielles des effectifs salariés et de la masse salariale 
du secteur privé, par zone d'emploi.

Objet : présentation des données sous Streamlit / Dash / Power BI

Lancement sur streamlit : 
streamlit run indexB013_Streamlit.py

Dashboard :
https://docs.google.com/drawings/d/1OKiRsCjmbV6p6VJojp3Ivz3Hvs2_cKFvSBSMGZ-Qxq0/edit

Prochain travail : Insérer la table

Date : 24-01-24
"""

import streamlit as st
import pandas as pd

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
       
        # Récupération du fichier .csv converti en DF polars
        job_df = pd.read_csv('data/emploi.csv', sep=";")
        
        # Champs à conserver
        job_s1 = job_df[[
            "annee", "trimestre", "region", "zone_d_emploi",
            "effectifs_salaries_cvs", "masse_salariale_cvs"]].sort_values(
                by=['annee', 'trimestre', 'zone_d_emploi'])
            
        # Filtre sur le champ 'annee'
        job_f1 = job_s1[job_s1['annee'] > 2013]
        
        # Insertion de la DF traitée ci-après dans le 1er menu déroulant
        region_st = st.selectbox(
            "Région",
            job_f1['region'].sort_values().unique(),
            )
        
        # DF filtrée selon la région sélectionnée dans le menu déroulant ci-avant
        job_f2 = job_f1[job_f1['region'] == region_st]
        
        # Espace entre les 2 menus déroulants
        st.text('')
        
        # Insertion de la DF traitée ci-après dans le 2ème menu déroulant
        area_st = st.selectbox(
            "Zone d'emploi",
            job_f2['zone_d_emploi'].sort_values().unique(),
            )
        
if __name__ == '__main__':
    
    app()
