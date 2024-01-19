"""
https://data.economie.gouv.fr/pages/accueil/

Traitement opéré : API sur les procédures collectives, France entière

Lien : https://open.urssaf.fr/explore/dataset/procedures-collectives-france-entiere/api/?sort=-dernier_jour_du_trimestre

Lancement sur streamlit : 
streamlit run indexB009_Faillites.py

Date : 10-01-24
"""

import requests
import json
import streamlit as st
import pandas as pd


# Présentation des données issues de l'API
class FrontEnd():
    
    def __init__(self) -> None:
        
        # Instanciation des variables
        
        # Secteur concerné
        self.procedure=[
            'Liquidation judiciaire', 'Redressement judiciaire', 'Sauvegarde']
        
        # Appel de la méthode ci-après
        self.gui()
        
    def gui(self):
        
        # Pleine page
        st.set_page_config(
            page_title="API URSSAF - Procédures collectives", layout="wide") 
        
        # Titre principal de la page @
        st.markdown(
            "<h3 style='text-align: center; color: yellow;'>Procédures collectives de 2013 à 2023 (avec correction des valeurs saisonnières)</h3>",
            unsafe_allow_html=True)
        
        # Configuration de la largeur des colonnes
        col1, col2 = st.columns([3, 9])
        
        # Données à afficher dans la colonne n° 1
        with col1:
           
            # Menu déroulant sur le type de procédure
            select_procedure = st.selectbox("Procédure", self.procedure, index=1)
            st.text('\n')
        
            # Accès à l'URL avec le requêtage appliqué :
            url = f"https://open.urssaf.fr/api/explore/v2.1/catalog/datasets/procedures-collectives-france-entiere/records?select=annee%2C%20trimestre%2C%20nombre_de_procedures_cvs&where=nature_de_procedure%20LIKE%20%27{select_procedure}%27%20AND%20annee%20%3E%20date%272012%27&order_by=annee%20ASC%2C%20trimestre%20ASC&limit=100"
            
            # Requête url
            response = requests.get(url)
            
            # Si le code postal a été retrouvé (code http : 200)
            if response.status_code == 200:

                # Récupération du contenu au format json
                data = json.loads(response.content)
                
                # Récupération du contenu au format json
                data = json.loads(response.content)

                # Données converties en DF pandas
                df = pd.DataFrame(data['results'])
                
                # Renommage des champs
                df = df.rename({"annee": "Année", 
                                "trimestre": "Trimestre",
                                "nombre_de_procedures_cvs": "Nombre de procédures"})
                
                # DF à afficher :
                st.dataframe(
                        df,
                        hide_index=True, # index masqué
                    )
                
            # À défaut (code http : 404) 
            else:
                st.warning(f'Données non récupérées', icon="⚠️")
        
        with col2:
            
            # Message d'information
            st.info("Source : URSSAF - Les procédures collectives sont dénombrées par entreprise", icon="ℹ️")
            
            # Concaténation des champs Année et Trimestre
            df['Periode'] = df['annee'].map(str) + ' - ' +  df['trimestre'].map(str)
            
            # Graphique du nombre de sociétés concernées selon la procédure
            st.bar_chart(df, 
                          x='Periode', 
                          y='nombre_de_procedures_cvs', 
                          color='#1e40d8', 
                          height=400)
            
if __name__ == '__main__':
    
    application = FrontEnd()
