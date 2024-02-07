from dash import Dash, html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import dash_ag_grid as dag

# BACK END ------------------------------------------------------

# CONFIGURATION DES COMPOSANTS ----------------------------------

# Carte sur les menus déroulants
card_dropdown = dbc.Card([   
    # Menu déroulant sur les régions
    dcc.Dropdown(
        id='drop-region-id', # pour le callback
        options=[], # valeurs du menu déroulant
        placeholder="Grand Est", # valeur affichée par défaut au menu
        clearable=False, # donnée affichée non supprimables
        style={'color': '#000000'}, # Couleur du composant
        className='dropdown-css', # config suppl en fichier .css
        ),
    
    # Menu déroulant sur les zones d'emploi
    dcc.Dropdown(
        id='drop-area-id', # pour le callback
        options=['test'], # valeurs du menu déroulant
        placeholder="Colmar", # valeur affichée par défaut au menu
        clearable=False, # donnée affichée non supprimable
        style={'color': '#000000'}, # Couleur du composant
        className='dropdown-css', # config suppl en fichier .css
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

if __name__ == "__main__":
    app.run_server(debug=True)
