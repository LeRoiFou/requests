"""
Configuration de la page @ :

Recours à la librairie Dash

Un titre principal

1 colonne comprenant 2 menus déroulants :
-> un pour le type d'indépendant
-> un pour le ou les départements

1 colonne comprenant 2 graphiques :
-> Graphique sur le nombre d'indépendants (diagramme en barres) :
    . Axe des X : années
    . Axe des y : le nombre d'indépendants par département(s)

-> Graphique sur les revenus des indépendants (diagramme linéaire) :
    . Axe des X : années
    . Axe des y : les revenus des indépendants par département(s)
    
Date : 13-01-24
Éditeur : Laurent Reynaud
"""

from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

# BACK END --------------------------------------------------------------


# CONFIGURATION DES COMPOSANTS -----------------------------------------

# Menus déroulants
dropdown_card = dbc.Card([
    
    # Menu déroulant pour le type d'indépendant
    dcc.Dropdown(
        id='type', # pour le callback
        options=[ # valeur affichée / valeurs pour le callback
            {'label':'Auto-entrepreneurs', 'value':'auto'},
            {'label':'Travailleurs indépendants', 'value':'independent'}
            ],
        className='dropdown-independent'
    )
    
    # Menu déroulant pour le ou les départements
    
])

# Diagrammes


# FRONT END ----------------------------------------------------------

# Instanciation de la librairie Dash avec thème appliqué sur la page @
# https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/explorer/
app = Dash(external_stylesheets=[dbc.themes.DARKLY])

# Configuration de la page @
app.layout = html.Div(children=[
    
    # Titre principal de la page @
    html.H1("Travailleurs indépendants depuis 2013", # Texte affiché
            className='main-title', # Voir fichier .css
            ),
    
    # Colonne sur les menus déroulants
    dbc.Col(dropdown_card, # Configuration ci-avant
            width=2, # Taille de la colonne
            ),
])


# INTERACTION DES COMPOSANTS -----------------------------------------


if __name__ == '__main__':
    app.run_server(debug=True)
