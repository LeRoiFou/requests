"""
Configuration de la page @ : recours à la librairie Dash
    
Date : 13-01-24
Éditeur : Laurent Reynaud
"""

from dash import Dash, html, dcc, callback, Input, State, Output, exceptions
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

# Titre, menus déroulants et message d'information
dropdown_card = dbc.Card([
    
    # Titre principal de la page @
    html.H4("Travailleurs indépendants depuis 2013", # Texte affiché
            className='main-title', # Voir fichier .css
            ),
    
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
    
    # Bouton d'information
    dbc.Button("Information", # Titre
                id="info-popover", # callback
                className='button-info', # Fichier .css
                ),
    
    # Texte d'information
    dbc.Popover(
        [
        # En-tête du commentaire
        dbc.PopoverHeader("Urssaf, données arrêtées en mai 2023"),
        
        # Corps principal du commentaire
        dbc.PopoverBody(
            "Ces données n’intègrent pas les exploitants agricoles. Pour l’exercice professionnel de son activité économique, le travailleur indépendant (TI) peut opter pour le statut dit « classique » ou celui d’auto-entrepreneur (AE)."),
        
        # Corps principal du commentaire (suite)
        dbc.PopoverBody(
            "Le revenu des AE est calculé à partir du chiffre d'affaires déclaré."),
        
        # Corps principal du commentaire (suite)
        dbc.PopoverBody(
            "Le nombre de travailleurs indépendants comptabilise des comptes de cotisants et non des individus et ayant dégagé un revenu."),
        ],
        id="popover", # pour le callback
        target="info-popover",  # pour le callback avec le bouton d'information
        placement="bottom", # commentaire placé de préférence en dessous du bouton
        is_open=False, # si True : commentaire toujours affiché
    ),
    
], className='dropdowns-card') # Config fichier .css

# Diagrammes
graph_card = dbc.Card([
    
    # Zone vide pour le nombre d'indépendants (diagramme en barres)
    html.Div(id='graph-numbers', # pour le callback
             children=[] # Zone vide
             ), 
    
    html.Br(),
    
    # Zone vide pour les revenus des indépendants (diagramme linéaire)
    html.Div(id='graph-revenues', # pour le callback
             children=[] # Zone vide
             ), 
    
], className='graphs-card') # Config fichier .css

# FRONT END ----------------------------------------------------------

# Instanciation de la librairie Dash avec thème appliqué sur la page @
# https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/explorer/
app = Dash(external_stylesheets=[dbc.themes.DARKLY])

# Configuration de la page @
app.layout = html.Div(children=[
    
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
        component_property='children' # Fonctionnalité : valeur de la zone vide
        ),
     Output(
         component_id='graph-revenues', # Sortie : diagramme linéaire (rev indép.)
         component_property='children' # Fonctionnalité : valeur de la zone vide
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
            data_frame=df_ti, # Récupération de la DF
            title="Nombre d'indépendants",
            x='annee', # Axe des abscisses
            y="nombre_de_ti", # Axe des ordonnées
            height=350, # Hauteur
            text_auto='.3s', # Montants à 3 chiffres mentionnés sur les barres
            color_discrete_sequence=['#4292c6'], # Couleur des barres
        ).update_traces(
            textfont_size=12, # Taille des caractères à l'intérieur du graph
            textposition="inside", # Texte en dehors / intérieur des barres
        ).update_layout(
            xaxis_title='', # Modification du nom de l'axe x
            yaxis_title='', # Modification du nom de l'axe y
        )
          
        # Configuration du diagramme linéaire (revenus des indépendants)
        graph_revenues = px.line(
            data_frame=df_revenues, # Récupération de la DF
            title="Revenus totaux",
            x='annee', # Axe des abscisses
            y="revenu", # Axe des ordonnées
            height=350, # Hauteur
            color_discrete_sequence=['#4292c6'], # Couleur de la ligne
        ).update_traces(
            textfont_size=12, # Taille des caractères à l'intérieur du graph
            mode="markers+lines", # marqueur sur la ligne
        ).update_layout(
            xaxis_title='', # Modification du nom de l'axe x
            yaxis_title='', # Modification du nom de l'axe y
        )
        
        # MAJ des graphiques
        return dcc.Graph(figure=graph_numbers), dcc.Graph(figure=graph_revenues)
    
    # Si dans l'un des menus déroulants, aucune valeur n'est affichée   
    else:
        
        # Exception : pas de MAJ des graphiques
        raise exceptions.PreventUpdate
    
# Affichage d'un commentaire en cliquant sur le bouton "Information"
@callback(
    Output("popover", "is_open"), # Sortie : commentaire
    [Input("info-popover", "n_clicks")], # Entrée : Bouton d'information
    [State("popover", "is_open")], # State : commentaire
)
def toggle_popover(n, is_open):
    
    # Evite l'affichage automatique du commentaire dès ouverture de la page @
    if n:
        return not is_open
    
    return is_open

if __name__ == '__main__':
    app.run_server(debug=True)
