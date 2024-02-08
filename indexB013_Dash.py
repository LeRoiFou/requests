import polars as pl
from dash import Dash, html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import dash_ag_grid as dag

# BACK END ------------------------------------------------------

# Récupération du fichier .csv converti en DF polars
job_df = pl.scan_csv('data/emploi.csv', separator=";")

# Champs à conserver
job_s1 = job_df.select(
    "annee", "trimestre", "region", "zone_d_emploi",
    "effectifs_salaries_cvs", "masse_salariale_cvs").sort(
        by=['annee', 'trimestre', 'zone_d_emploi'])

# Filtre sur le champ 'annee'
job_f1 = job_s1.filter(pl.col('annee') > 2013)

# DF sur les régions uniquement
region_df = job_f1.select('region').unique()

# Conversion de la DF ci-avant en liste
region_list = region_df.collect().sort(by='region').to_numpy().tolist()

# Compréhension de liste de la DF polars traitée ci-avant
region_data = [region for i in region_list for region in i]

# CONFIGURATION DES COMPOSANTS ----------------------------------

# Carte sur les menus déroulants
card_dropdown = dbc.Card([   
    # Menu déroulant sur les régions
    dcc.Dropdown(
        id='drop-region-id', # pour le callback
        options=[  # valeurs du menu déroulant
            {'label': i, 'value': i} for i in region_data],
        placeholder="Région 😎", # valeur affichée par défaut au menu
        clearable=False, # donnée affichée non supprimables
        style={'color': '#000000'}, # Couleur du composant
        className='dropdown-css', # config suppl en fichier .css
        ),
    
    # Zone vide pour le menu déroulant sur les zones d'emploi
    html.Div(
        id="drop-area-id", # pour le callback
        children=[], # données vides
        ),
    ], className='card-css')

# Carte sur la table
card_table = dbc.Card([
    # Bouton d'export
    html.Button(
        "Export Excel", # Texte
        id="button-export-id", # pour le callback
        className='button-css', # config suppl en fichier .css
                ),

    # Zone vide pour la datatable
    html.Div(
        id="table-data-id", # pour le callback
        children=[], # données vides
        ),
    ], className='card-css')

# Carte pour le graphique linéaire (effectifs)
card_line = dbc.Card([
    
    # Zone vide pour le graphique linéaire
    html.Div(
        id="line-staff-id", # pour le callback
        children=[], # données vides
    ),
    ], className='card-css')

# Carte pour le diagramme en barre (salaires)
card_bar = dbc.Card([
    
    # Zone vide pour le diagramme en barre
    html.Div(
        id="bar-wages-id", # pour le callback
        children=[], # données vides
    ),
    ], className='card-css')

# FRONT END ----------------------------------------------------

# Instanciation de la librairie Dash et mise en page @
app = Dash(external_stylesheets=[dbc.themes.SUPERHERO])

# Configuration de la page @
app.layout = html.Div([
    
    # Titre principal
    dbc.Row([
        
        # Titre
        html.H3("Effectifs et masse salariale par zone d'emploi", # texte
                style={'textAlign': 'Center',}, # Alignement du texte à la page @
                className='title-css', # config suppl en fichier .css
                ),
        
        ]),
    
    # Composants à afficher
    dbc.Row([
        
        # Menus déroulants et table
        dbc.Col([
            
            # Carte sur les menus déroulants
            card_dropdown,
            
            # Table : zone vide
            card_table,
            
            ], width=4 # largeur de la colonne
                ),
        
        # Graphiques
        dbc.Col([
            
            # Graphique sur les effectifs : zone vide
            card_line,
            
            # Graphique sur les salaires : zone vide
            card_bar,
            
            ], width=8 # largeur de la colonne
                ),
        
    ]),
    
])

# INTERACTION DES COMPOSANTS -----------------------------------

@callback(Output( # Sortie : menu déroulant sur les zones d'emploi
    component_id='drop-area-id', # id
    component_property='children', # fonctionnalité
    ),
         Input( # Entrée : menu déroulant sur les régions
    component_id='drop-region-id', # id
    component_property='value', # fonctionnalité
    ))
def update_dropdown(region_value):
    
    # Filtre de la DF selon la valeur sélectionné au menu déroulant 'région'
    job_f2 = job_f1.filter(pl.col('region').str.contains(region_value))
    
    # DF sur les zones d'emploi uniquement
    area_df = job_f2.select('zone_d_emploi').unique()

    # Conversion de la DF ci-avant en liste
    area_list = area_df.collect().sort(by='zone_d_emploi').to_numpy().tolist()

    # Compréhension de liste de la DF polars traitée ci-avant
    area_data = [area for i in area_list for area in i]
    
    # Configuration du menu déroulant sur les zones d'emploi
    drop_area = dcc.Dropdown(
        options=[ # valeurs du menu déroulant
                 {'label': i, 'value': i} for i in area_data], 
        placeholder="Zone d'emploi 😛", # valeur affichée par défaut au menu
        clearable=False, # donnée affichée non supprimable
        style={'color': '#000000'}, # Couleur du composant
        className='dropdown-css', # config suppl en fichier .css
        ),
    
    # MAJ du menu déroulant
    return drop_area
    

if __name__ == "__main__":
    app.run_server(debug=True)
