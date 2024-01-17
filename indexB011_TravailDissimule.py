"""
Configuration de la page @ : recours à la librairie Dash
    
Date : 17-01-24
Éditeur : Laurent Reynaud
"""

from dash import Dash, html, dcc, callback, Input, State, Output, exceptions
import dash_bootstrap_components as dbc
import requests
import json
import polars as pl
import plotly.express as px

# BACK END --------------------------------------------------------------

# Récupération du fichier .csv des régions converti en DF polars
district_df = pl.read_csv('data/regions.csv')

# Conversion de la df polars ci-avant en liste
district_list = district_df.to_numpy().tolist()

# Compréhension de liste de la DF polars traitée ci-avant
districts = [district for i in district_list for district in i]

# CONFIGURATION DES COMPOSANTS -----------------------------------------

# Titre, menus déroulants et message d'information
dropdown_card = dbc.Card([
    
    # Titre principal de la page @
    html.H4(
        "Luttre contre le travail dissimulé par les URSSAF", # Texte affiché
        className='main-title', # Voir fichier .css
        ),
    
    # Menu déroulant pour les régions
    dcc.Dropdown(
        id='districts', # pour le callback
        options=[ # valeur affichée / valeurs pour le callback
            {'label': i, 'value': i} for i in districts],
        placeholder="Sélectionner un département",
        clearable=False, # Données non supprimables
        className='dropdown-district', # Config fichier .css
        ),
    
    # Bouton d'information
    dbc.Button(
        "Information", # Titre
        id="info-popover", # pour le callback
        ),
    
    # Texte d'information
    dbc.Popover(
        [
        # En-tête du commentaire
        dbc.PopoverHeader("Lutte contre le travail illégal"),
        
        # Corps principal du commentaire
        dbc.PopoverBody(
            "NB : la colonne ancienne région correspondant à l'organisation des Urssaf comporte une particularité à partir de la mise à jour 2022."),
        
         # Corps principal du commentaire (complément d'information)
        dbc.PopoverBody(
            "Les Urssaf Haute et Basse-Normandie ont fusionné et sont regroupées sous le terme Normandie."),
        
        ],
        id="popover", # pour le callback
        target="info-popover",  # pour le callback avec le bouton d'information
        placement="bottom", # commentaire placé de préférence en dessous du bouton
        is_open=False, # si True : commentaire toujours affiché
    ),
    
], className='dropdowns-card') # Config fichier .css

# Diagrammes
graph_card = dbc.Card([
    
    # Zone vide pour le nombre de redressements
    html.Div(id='graph-numbers', # pour le callback
             children=[] # Zone vide
             ), 
    
    html.Br(),
    
    # Zone vide pour le montant des redressements
    html.Div(id='graph-revenues', # pour le callback
             children=[] # Zone vide
             ), 
    
], className='graphs-card') # Config fichier .css

# FRONT END ----------------------------------------------------------

# Instanciation de la librairie Dash avec thème appliqué sur la page @
# https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/explorer/
app = Dash(external_stylesheets=[dbc.themes.SUPERHERO])

# Configuration de la page @
app.layout = html.Div(children=[
    
    dbc.Row([
        
        # Colonne sur le menu déroulant, bouton d'information
        dbc.Col(dropdown_card, # Configuration ci-avant
                width=3, # Taille de la colonne
                ),
        
        # Colonne sur les graphiques
        dbc.Col(graph_card, # Configuration ci-avant
                width=9, # Taille de la colonne
                ),
    ])
])

# INTERACTION DES COMPOSANTS -----------------------------------------

# MAJ des diagrammes en fonction de la valeur sélectionnée dans le menus déroulant
@callback(
    [Output(
        'graph-numbers', # Sortie : diagramme en barres (nbre de redressements)
        'children' # Fonctionnalité : valeur de la zone vide
        ),
     Output(
         'graph-revenues', # Sortie : diagramme linéaire (montant des redressements)
         'children' # Fonctionnalité : valeur de la zone vide
         )],
    Input(
        'districts', # Entrée : menu déroulant des départements
        'value' # Fonctionnalité : valeurs du menu déroulant
        )
    )
def update_graph(district_selected):
        
    # Si au moins une valeur est affichée...
    if district_selected:
        
        # Récupération de l'URL selon les valeurs sélectionnées 
        # dans les menus déroulants
        url = f"https://open.urssaf.fr/api/explore/v2.1/catalog/datasets/resultats-de-la-lutte-contre-le-travail-illegal/records?select=annee%2C%20ancienne_region%2C%20nombre_redressements%2C%20montant_redressements&where=nombre_redressements%20%3E%200%20AND%20ancienne_region%20LIKE%20%27{district_selected}%27&order_by=annee&limit=100"
        
        # Requête url
        response = requests.get(url)
        
        # Récupération du contenu au format json
        data = json.loads(response.content)

        # Récupération des données ci-avant converties en DF polars
        df = pl.DataFrame(data['results'])
        
        # DF sur les années et le nombre de redressements
        df_numbers = df.select(['annee', 'nombre_redressements'])
        
        # DF sur les années et le montant des redressements
        df_revenues = df.select(['annee', 'montant_redressements'])
        
        # Configuration du diagramme en barres (nombre de redressements)
        graph_numbers = px.bar(
            data_frame=df_numbers, # Récupération de la DF
            title="Nombre de redressements",
            x='annee', # Axe des abscisses
            y="nombre_redressements", # Axe des ordonnées
            height=350, # Hauteur
            text_auto='.3s', # Montants à 3 chiffres mentionnés sur les barres
            color_discrete_sequence=['#0f2537'], # Couleur des barres
        ).update_traces(
            textfont_size=12, # Taille des caractères à l'intérieur du graph
            textposition="inside", # Texte en dehors / intérieur des barres
        ).update_layout(
            xaxis_title='', # Modification du nom de l'axe x
            yaxis_title='', # Modification du nom de l'axe y
        )
          
        # Configuration du diagramme linéaire (montant des redressements)
        graph_revenues = px.line(
            data_frame=df_revenues, # Récupération de la DF
            title="Montant des redressements",
            x='annee', # Axe des abscisses
            y="montant_redressements", # Axe des ordonnées
            height=350, # Hauteur
            color_discrete_sequence=['#0f2537'], # Couleur de la ligne
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
