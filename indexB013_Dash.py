import polars as pl
from dash import Dash, html, dcc, callback, Input, Output, exceptions, clientside_callback
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import plotly.express as px

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
    dcc.Dropdown(
        id="drop-area-id", # pour le callback
        options=[], # données vides
        value=[], # pas de valeurs affichées par défaut
        placeholder="Zone d'emploi 😛", # valeur affichée par défaut au menu
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

# MAJ du menu déroulant sur les zones d'emploi en fonction de la région sélectionnée
# dans le premier menu déroulant
@callback([Output( # Sortie : menu déroulant sur les zones d'emploi
    component_id='drop-area-id', # id
    component_property='options', # fonctionnalité : valeurs du menu déroulant
    ),
           Output( # Sortie : menu déroulant sur les zones d'emploi
    component_id='drop-area-id', # id
    component_property='value', # fonctionnalité : valeurs affichées par défaut
    )
           ],
         Input( # Entrée : menu déroulant sur les régions
    component_id='drop-region-id', # id
    component_property='value', # fonctionnalité
    ))
def update_dropdown(region_value):
    
    # Filtre de la DF selon la valeur sélectionné au menu déroulant 'région'
    job_f2 = job_f1.filter(pl.col('region').str.contains(region_value))
    
    # DF sur les zones d'emploi uniquement
    area_df = job_f2.select('zone_d_emploi').collect().unique().to_series().to_list()
    
    # Alimentation des données du menu déroulant de la zone d'emploi selon 
    # la valeur sélectionnée dans le menu déroulant des régions
    area_options = [{'label': data, 'value': data}
                    for data in sorted(area_df)]
    
    # Affichage de la zone d'emploi selon la valeur sélectionné dans le menu 
    # déroulant des régions
    area_value = [data['value'] for data in area_options]
    
    # Si au moins une région a été sélectionnée
    if len(area_value) > 0:
        
        # La valeur à afficher dans le menu déroulant est la 1ère zone d'emploi
        area_value = area_value[0]
    
    # MAJ de la valeur affichée et des valeurs alimentées
    return area_options, area_value

# MAJ de la table en fonction de la zone d'emploi sélectionnée dans le deuxième
# menu déroulant
@callback(Output(
    component_id='table-data-id', # id
    component_property='children', # fonctionnalités
    ),
          Input(
    component_id='drop-area-id', # id
    component_property='value', # fonctionnalités
    ))
def update_table(area_value):

    # Si une valeur est sélectionnée dans le menu déroulant de la zone d'emploi
    if len(area_value) > 0:
    
        # Filtre de la DF selon la valeur sélectionnée au menu déroulant 
        # 'zone d'emploi'
        job_f2 = job_f1.filter(pl.col('zone_d_emploi').str.contains(area_value))
        
        # Champs à afficher
        table_df = job_f2.select(['annee', 'trimestre', 'effectifs_salaries_cvs',
                                  'masse_salariale_cvs',]).collect().to_pandas()
                
        # Configuration des montants numériques avec séparateur de milliers
        locale_fr_FR = """d3.formatLocale({
                        "decimal": ",",
                        "thousands": "\u00a0",
                        "grouping": [3],
                        "nan": ""
                        })"""
        
        # Configuration des montants numériques en devise € 
        # avec séparateur de milliers
        currency_fr_FR = """d3.formatLocale({
                        "decimal": ",",
                        "thousands": "\u00a0",
                        "grouping": [3],
                        "currency": ["", "\u00a0€"],
                        "nan": ""
                        })"""
                        
        # Configuration des en-têtes de la table 
        columnDefs = [
            {
                "headerName": "Annee", # Nom de la colonne
                "field": "annee", # ID de la colonne
                "cellStyle": {'textAlign': 'center'}, # Alignement des cellules
            },
            {
                "headerName": "Trimestre", # Nom de la colonne
                "field": "trimestre", # ID de la colonne
                "cellStyle": {'textAlign': 'center'}, # Alignement des cellules
            },
            {
                "headerName": "Effectifs", # Nom de la colonne
                "field": "effectifs_salaries_cvs", # ID de la colonne
                "cellStyle": {'textAlign': 'center'}, # Alignement des cellules
                "valueFormatter": { # Format séparateur de milliers locale_fr_FR
                "function": f"{locale_fr_FR}.format('$,.0f')(params.value)"},
            },
            {
                "headerName": "Salaires", # Nom de la colonne
                "field": "masse_salariale_cvs", # ID de la colonne
                "cellStyle": {'textAlign': 'center'}, # Alignement des cellules
                "valueFormatter": { # Format monétaire
                "function": f"{currency_fr_FR}.format('$,.0f')(params.value)"},
            },]
        
        # Configuration de la table
        defaultColDef = {
            "sortable": True, # Trie
            "resizable": True, # Taille ajustable
            "minWidth": 100, # Taille mini
        }
        
        # Style attribué pour le fichier Excel an niveau des en-têtes UNIQUEMENT
        # Lien : https://ag-grid.com/javascript-data-grid/excel-export-styles/
        excelStyles = [
            {
                "id": "header",
                "alignment": {
                    "horizontal": "Center",
                },
                "font": {
                    "bold": "true",
                },
                "interior": {
                    "pattern": "Solid",
                    "color": "#1c87d3",
                },
            },
        ]
        
        # MAJ de la table AgGrid
        table = dag.AgGrid(
                id='table-aggrid-id',
                rowData=table_df.to_dict('records'), # Récup données de la DF en dict
                columnDefs=columnDefs, # config des en-têtes effectuée ci-avant
                defaultColDef=defaultColDef, # configuration de la table ci-avant
                columnSize="sizeToFit", # Colonnes ajustées à leurs largeurs
                style={"height": 480}, # Hauteur du tableau
                dashGridOptions={ # Configuration export Excel
                    "rowSelection": "multiple", # Multiple sélection
                    "excelStyles": excelStyles, # style pour l'export Excel
                    "defaultExcelExportParams": # Hauteur des colonnes en-têtes Excel
                        {"headerRowHeight": 30},
                },
                enableEnterpriseModules=True, # indispensable pour l'export Excel
                className="ag-table-css", # config suppl en fichier .css
                ),
        
        return table
    
    # Si aucune valeur n'est affichée au menu déroulant de la zone d'emploi
    elif len(area_value) == 0:
        
        # Pas de MAJ de la table
        raise exceptions.PreventUpdate

# # MAJ du graphique linéaire selon les données de la table
# @callback(Output( # Sortie : graphique linéaire
#     component_id='line-staff-id', # id
#     component_property='children', # fonctionnalités
#     ),
#          [Input( # Entrée : table
#     component_id='table-aggrid-id', # id
#     component_property='virtualRowData', # fonctionnalités : filtre
#     ),  Input( # Entrée : table
#     component_id='table-aggrid-id', # id
#     component_property='selectedRows', # fonctionnalités : sélection
#     )])
def update_line_graph(rows, selected):
    
    # Si les données de la table sont récupérées
    if rows:
        # DF récupérée dont filtre, trie... de la table AgGrid
        dff = pl.DataFrame(rows)
        
        # Sélection par le champ 'Date' de la DF
        selected = [s["Date"] for s in selected] if selected else []
        
        # MAJ du graphique
        fig = px.bar(
            dff, # DF filtrée ci-avant
            x="Date", # Données sur l'axe des abscisses
            y='Montant journalier', # Données sur l'axe des ordonnées
            height=560, # Hauteur
            text_auto='.3s', # Montants à 3 chiffres mentionnés sur les barres
            color_discrete_sequence=['#1b846d'], # Couleur des barres
            ).update_traces(
                textfont_size=12, # Taille des caractères à l'intérieur du graph
                textposition="inside", # Texte en dehors / intérieur des barres
                ).update_layout(
                    xaxis_tickangle=-45, # Alignement du texte axe des abscisses
                    font=dict(size=12), # Taille du texte au niveau des axes
                    xaxis_title='', # Modification du nom de l'axe x
                    yaxis_title='Montant', # Modification du nom de l'axe y
                    )
        
        return dcc.Graph(figure=fig)

# # MAJ du diagramme en barre selon les données de la table
# @callback(Output( # Sortie : diagramme en barres
#     component_id='bar-wages-id', # id
#     component_property='children', # fonctionnalités 
#     ),
#           [Input( # Entrée : table
#     component_id='table-aggrid-id', # id
#     component_property='virtualRowData', # fonctionnalités : filtre
#     ),  Input( # Entrée : table
#     component_id='table-aggrid-id', # id
#     component_property='selectedRows', # fonctionnalités : sélection
#     )])
def update_bar_graph(rows, selected):
    
    # Si les données de la table sont récupérées
    if rows:
        pass
    
# Configuration export Excel des données de la datatable
clientside_callback(
    """function (n) {
        if (n) {
            dash_ag_grid.getApi("table-aggrid-id").exportDataAsExcel();
        }
        return dash_clientside.no_update
    }""",
    Output("button-export-id", "n_clicks"),
    Input("button-export-id", "n_clicks"),
    prevent_initial_call=True, # évite MAJ des composants dès chargement page @
)   


if __name__ == "__main__":
    app.run_server(debug=True)
