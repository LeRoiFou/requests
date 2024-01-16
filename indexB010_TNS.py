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

from dash import Dash, html, dcc, callback, Input, Output, exceptions
import dash_bootstrap_components as dbc
import requests
import json
import polars as pl
import plotly.express as px

# BACK END --------------------------------------------------------------

# Récupération du fichier .csv des départements converti en DF polars
departments_list = pl.read_csv('data/departments.csv').to_numpy().tolist()

# Compréhension de liste de la DF polars traitée ci-avant
departments = [department for department_list in departments_list
             for department in department_list]

# CONFIGURATION DES COMPOSANTS -----------------------------------------

# Menus déroulants
dropdown_card = dbc.Card([
    
    # Menu déroulant pour le type d'indépendant
    dcc.Dropdown(
        id='type', # pour le callback
        options=[ # valeur affichée / valeurs pour le callback
            {'label':'Auto-entrepreneurs', 'value':'Autoentrepreneur'},
            {'label':'Travailleurs indépendants', 'value':'TI classique'},],
        placeholder="Type d'indépendant",
        clearable=False, # Données non supprimables
        className='dropdown-independent', # Config fichier .css
    ),
    
    # Menu déroulant pour le département
    dcc.Dropdown(
        id='departments', # pour le callback
        options=[ # valeur affichée / valeurs pour le callback
            {'label': i, 'value': i} for i in departments],
        placeholder="Sélectionner un département",
        clearable=False, # Données non supprimables
        className='dropdown-independent', # Config fichier .css
    ),
    
], className='dropdowns-card') # Config fichier .css

# Diagrammes
graph_card = dbc.Card([
    
    # Graphique vide pour le nombre d'indépendants (diagramme en barres)
    dcc.Graph(id='graph-numbers'), # pour le callback
    
    # Graphique vide pour les revenus des indépendants (diagramme linéaire)
    dcc.Graph(id='graph-revenues'), # pour le callback
    
], className='graphs-card') # Config fichier .css

# FRONT END ----------------------------------------------------------

# Instanciation de la librairie Dash avec thème appliqué sur la page @
# https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/explorer/
app = Dash(external_stylesheets=[dbc.themes.DARKLY])

# Configuration de la page @
app.layout = html.Div(children=[
    
    # Titre principal de la page @
    html.H3("Travailleurs indépendants depuis 2013", # Texte affiché
            className='main-title', # Voir fichier .css
            ),
    
    dbc.Row([
        
        # Colonne sur les menus déroulants
        dbc.Col(dropdown_card, # Configuration ci-avant
                width=3, # Taille de la colonne
                ),
        
        # Colonne sur les graphique
        dbc.Col(graph_card, # Configuration ci-avant
                width=9, # Taille de la colonne
                ),
    ])
])

# INTERACTION DES COMPOSANTS -----------------------------------------

# MAJ des diagrammes en fonction des valeurs sélectionnées dans les menus déroulants
@callback(
    [Output(
        component_id='graph-numbers', # Sortie : diagramme en barres (nbre indép.)
        component_property='figure' # Fonctionnalité : figure du graph
        ),
     Output(
         component_id='graph-revenues', # Sortie : diagramme linéaire (rev indép.)
         component_property='figure' # Fonctionnalité : figure du graph
         )],
   [ Input(
       component_id='type', # Entrée : menu déroulant type d'indépendant
       component_property='value' # Fonctionnalité : valeurs du menu déroulant
       ),
    Input(
        component_id='departments', # Entrée : menu déroulant des départements
        component_property='value' # Fonctionnalité : valeurs du menu déroulant
    )])
def update_graph(type_seleted, departments_selected):
        
    # Si au moins une valeur est affichés aux deux menus déroulants...
    if type_seleted and departments_selected:
        
        # Récupération de l'URL selon les valeurs sélectionnées 
        # dans les menus déroulants
        url = f"https://open.urssaf.fr/api/explore/v2.1/catalog/datasets/les-revenus-des-travailleurs-independants-par-departement/records?select=annee%2C%20nombre_de_ti%2C%20revenu&where=type_de_travailleur_independant%3D%27{type_seleted}%27%20AND%20departement%3D%22{departments_selected}%22%20AND%20annee%20%3E%20date%272012%27&order_by=annee&limit=100"
        
        # Requête url
        response = requests.get(url)
        
        # Récupération du contenu au format json
        data = json.loads(response.content)

        # Récupération des données ci-avant converties en DF polars
        df = pl.DataFrame(data['results'])
        
        # DF sur les années et le nombre d'indépendants
        df_ti = df.select(['annee', 'nombre_de_ti'])
        
        # DF sur les années et les revenus des indépendants
        df_revenues = df.select(['annee', 'revenu'])
        
        # Configuration du diagramme en barres (nombre d'indépendants)
        graph_numbers = px.bar(
            data_frame=df_ti,
            x='annee',
            y="nombre_de_ti",
            height=350,
        )
          
        # Configuration du diagramme linéaire (revenus des indépendants)
        graph_revenues = px.line(
            data_frame=df_revenues,
            x='annee',
            y="revenu",
            height=350,
        )
        
        # MAJ des graphiques
        return graph_numbers, graph_revenues
    
    # Si dans l'un des menus déroulants, aucune valeur n'est affichée   
    else:
        
        # Exception : pas de MAJ des graphiques
        raise exceptions.PreventUpdate

if __name__ == '__main__':
    app.run_server(debug=True)
