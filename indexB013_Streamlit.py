"""
Effectifs salariés et masse salariale trimestriels du secteur privé, 
par zone d'emploi
Lien :  https://www.data.gouv.fr/fr/datasets/effectifs-salaries-et-masse-salariale-trimestriels-du-secteur-prive-par-zone-demploi/

Séries trimestrielles des effectifs salariés et de la masse salariale 
du secteur privé, par zone d'emploi.

Objet : présentation des données sous Streamlit / Dash / Power BI

Lancement sur streamlit : 
streamlit run indexB013_Streamlit.py

Pour l'insertion des séparateurs de milliers et la devise € :
https://discuss.streamlit.io/t/formatting-numbers-with-commas-as-thousand-separators-in-st-aggrids-configure-columns-method/25386

Dashboard :
https://docs.google.com/drawings/d/1OKiRsCjmbV6p6VJojp3Ivz3Hvs2_cKFvSBSMGZ-Qxq0/edit

Prochain travail : Même résultat que streamlit mais cette fois-ci avec Dash 🦹‍♂️

Date : 24-01-24
"""

import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd

def app():
        
    # Récupération du fichier .csv converti en DF polars
    job_df = pd.read_csv('data/emploi.csv', sep=";")
    
    # Champs à conserver
    job_s1 = job_df[[
        "annee", "trimestre", "region", "zone_d_emploi",
        "effectifs_salaries_cvs", "masse_salariale_cvs"]].sort_values(
            by=['annee', 'trimestre', 'zone_d_emploi'])
        
    # Filtre sur le champ 'annee'
    job_f1 = job_s1[job_s1['annee'] > 2013]    
    
    # Pleine page
    st.set_page_config(
        page_title="Emploi secteur privé", layout="wide") 
    
    # Titre principal de la page @
    st.markdown(
        "<h5 style='text-align: center; color: yellow;'>Effectifs et masse salariale par zone d'emploi</h5>",
        unsafe_allow_html=True)
    
    # Configuration de la largeur des colonnes
    col1, col2 = st.columns([4, 8])
    
    # Données à afficher dans la colonne n° 1 : menus déroulants et table
    with col1:  
        
        # Insertion de la DF traitée ci-après dans le 1er menu déroulant
        region_st = st.selectbox(
            "Région", # Titre rattaché au menu déroulant
            job_f1['region'].sort_values().unique(), # valeurs à insérer
            )
        
        # DF filtrée selon la région sélectionnée dans le menu déroulant ci-avant
        job_f2 = job_f1[job_f1['region'] == region_st]
        
        # Espace entre les 2 menus déroulants
        st.text('')
        
        # Insertion de la DF traitée ci-après dans le 2ème menu déroulant
        area_st = st.selectbox(
            "Zone d'emploi", # Titre rattaché au menu déroulant
            job_f2['zone_d_emploi'].sort_values().unique(), # valeurs à insérer
            )
        
        # Traitement opérée sur la DF en fonction des valeurs sélectionnés dans les
        # 2 menus déroulants
        my_df = job_f1[(job_f1['region'] == region_st) &
                        (job_f1['zone_d_emploi'] == area_st)]
        
        # Champs à afficher
        my_df = my_df[['annee', 'trimestre', 'effectifs_salaries_cvs',
                       'masse_salariale_cvs']]
        
        # Instanciation de la sous-librairie GridOptionsBuilder
        gb = GridOptionsBuilder.from_dataframe(my_df)

        # Configuration des colonnes        
        gb.configure_column(
            field="annee", # Nom du champ de la DF
            header_name="Année", # Nom à afficher sur streamlit
            )
        gb.configure_column(
            field="trimestre", # Nom du champ de la DF
            header_name="Trimestre", # Nom à afficher sur streamlit
            )  
        gb.configure_column(
            field="effectifs_salaries_cvs", # Nom du champ de la DF
            header_name="Effectifs", # Nom à afficher sur streamlit 
            type=["numericColumn","numberColumnFilter","customNumericFormat"], 
            valueFormatter="data.effectifs_salaries_cvs.toLocaleString('fr-FR')",
            ) # type et valueFormatter : séparateur de milliers
        gb.configure_column(
            field="masse_salariale_cvs", # Nom du champ de la DF
            header_name="Salaires", # Nom à afficher sur streamlit
            type=["numericColumn","numberColumnFilter","customNumericFormat"], 
            valueFormatter="data.masse_salariale_cvs.toLocaleString('fr-FR', {style: 'currency', currency: 'EUR', maximumFractionDigits:0})",
            ) # type et valueFormatter : séparateur de milliers et devise €
        
        # Mise en place des configurations de la table ci-avant
        go = gb.build()
        
        # Affichage de la table
        AgGrid(my_df, 
               gridOptions=go, # configuration des colonnes ci-avant
               fit_columns_on_grid_load=True, # ajustement automatique des colonnes
               height=350, # hauteur de la table
               )
    
    # Données à afficher dans la colonne n° 2 : graphiques
    with col2:
        
        # Concaténation des champs Année et Trimestre
        my_df['Periode'] = (
            my_df['annee'].map(str) + ' - ' +  my_df['trimestre'].map(str))
        
        # Renommage des champs
        my_df = my_df.rename(columns={'effectifs_salaries_cvs':'Effectifs',
                                      'masse_salariale_cvs':'Salaires'})

        # Graphique sur les effectifs
        st.line_chart(my_df, 
                      x='Periode', 
                      y='Effectifs', 
                      color='#1e1ece', 
                      height=280)
        
        # Graphique sur les salaires
        st.bar_chart(my_df, 
                      x='Periode', 
                      y='Salaires', 
                      color='#f22409', 
                      height=280)

# Lancement de l'application        
app()