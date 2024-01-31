"""
Effectifs salariés et masse salariale trimestriels du secteur privé, 
par zone d'emploi
Lien :  https://www.data.gouv.fr/fr/datasets/effectifs-salaries-et-masse-salariale-trimestriels-du-secteur-prive-par-zone-demploi/

Séries trimestrielles des effectifs salariés et de la masse salariale 
du secteur privé, par zone d'emploi.

Objet : présentation des données sous Streamlit / Dash / Power BI

Dashboard :
https://docs.google.com/drawings/d/1OKiRsCjmbV6p6VJojp3Ivz3Hvs2_cKFvSBSMGZ-Qxq0/edit

Prochain travail : Même résultat que streamlit mais cette fois-ci avec Dash 🦹‍♂️

Date : 31-01-24
"""

from dash import Dash, html, dcc, callback, Input, State, Output, exceptions
import dash_bootstrap_components as dbc
import requests
import json
import pandas as pd
import plotly.express as px

# BACK END -----------------------------------------------------------

# Récupération du fichier .csv converti en DF polars
job_df = pd.read_csv('data/emploi.csv', sep=";")

# Champs à conserver
job_s1 = job_df[[
    "annee", "trimestre", "region", "zone_d_emploi",
    "effectifs_salaries_cvs", "masse_salariale_cvs"]].sort_values(
        by=['annee', 'trimestre', 'zone_d_emploi'])
    
# Filtre sur le champ 'annee'
my_df = job_s1[job_s1['annee'] > 2013]

# DF sur les régions
region_df = my_df['region'].sort_values().unique()

# CONFIGURATION DES COMPOSANTS ----------------------------------------------

# Carte sur les menus déroulants et la table
dropdown_card = dbc.Card([
    
    # Titre rattaché au menu déroulant pour les régions
    html.Label("Région", # Titre
               className='label-css', # Config dans le fichier .css
               ),
    
    # Menu déroulant pour les régions
    dcc.Dropdown(
        id='id-region', # pour le callback
        value='Grand Est', # Valeur affichée par défaut
        options=region_df, # Valeurs insérées dans le menu déroulant
        clearable=False, # Données non supprimables
        style={'color':'black'}, # Couleur du texte
        className='drop-css', # Config dans le fichier .css
        ),
    
    html.Br(),
    
    # Titre rattaché au menu déroulant pour les zones d'emploi
    html.Label("Zone d'emploi", # Titre
               className='label-css', # Config dans le fichier .css
               ),
    
    # Zone vide pour le menu déroulant pour les zones d'emploi
    html.Div(id='id-area', # pour le callback
             children='', # Données vides
             )
    
], class_name='dropdown-card-css')

# FRONT END --------------------------------------------------------

# Instanciation de la librairie Dash avec thème appliqué sur la page @
# https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/explorer/
app = Dash(external_stylesheets=[dbc.themes.SUPERHERO])

# Configuration de la page @
app.layout = html.Div(children=[
    
    # Titre principal de la page @
    html.H3("Effectifs et masse salariale par zone d'emploi",
            className='main-title'),
    
    # Insertion des composants configurés ci-avant
    dbc.Row([
        
        # Colonne sur les menus déroulants
        dbc.Col(
            
            # Composants compris dans cette colonne
            dbc.Row([
                
                # Carte sur les menus déroulants
                dropdown_card,
                
            ]), width=3, # Largeur de la colonne
            )
        ]),
    
])

# INTERACTION DES COMPOSANTS -------------------------------------------------

# MAJ du menu déroulant sur les zones d'emploi en fonction de la valeur sélectionnée
# dans le menu déroulant sur les régions
@callback(
    Output( # Sortie : menu déroulant sur les zones d'emploi
        component_id='id-area', # ID 
        component_property='value', # Fonctionnalité
    ),
    Input( # Entrée : menu déroulant sur les régions
          component_id='id-region', # ID
          component_property='value', # Fonctionnalité
    ),
)
def dropdown_func(input_value):
    
    # DF traitée selon la région sélectionnée dans le menu déroulant sur les régions
    area_df = region_df[region_df["region"] == input_value]
    
    print(area_df)
    
    # Données à conserver
    area_df = area_df["zone_d_emploi"].sort_values().unique()
    
    # Menu déroulant pour les régions
    area_dropdown =  dcc.Dropdown(
        id='id-area',
        value=area_df[0], # 1ère valeur affichée par défaut
        options=area_df, # Valeurs insérées dans le menu déroulant
        clearable=False, # Données non supprimables
        style={'color':'black'}, # Couleur du texte
        className='drop-css', # Config dans le fichier .css
        ),
    
    # MAJ du menu déroulant
    return area_dropdown

if __name__ == '__main__':
    app.run_server(debug=True)
