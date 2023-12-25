"""
https://api.gouv.fr/

Traitement opéré : API Carto - module Codes Postaux
Récupération des communes selon le code postal saisi

Lien : https://api.gouv.fr/les-api/api_carto_codes_postaux
Documentation : https://api.gouv.fr/documentation/api_carto_codes_postaux
URL: https://apicarto.ign.fr/api/codes-postaux/communes

Lancement sur streamlit : 
streamlit run indexB004_DataGouv.py

Date : 22-12-23
"""

import requests
import json
import pandas as pd
import streamlit as st
import pprint

class FrontEnd():
    
    def __init__(self) -> None:
        
        # Instanciation de variable : code postal
        self.code_postal = ''
        
        self.gui()
    
    def gui(self):
        
        # Titre principal de la page @
        st.header(":green[Liste des communes selon le code postal saisi]")
        st.text('\n')
        
        # Zone de saisie
        self.code_postal = st.text_input("Code postal : ")
        st.text('\n')

        # Bouton d'exécution pour valider le CP saisi ci-avant
        clicked = st.button('Valider', type='secondary')
        
        # Si le bouton 'Valider' a été appuyé et que 5 caractères ont été saisis
        # dans la zone de texte 'Code postal'...
        if clicked and len(self.code_postal) == 5:       
            self.treatments()
    
    def treatments(self):

        # Accès à l'URL avec le requêtage appliqué : code_postal
        url = 'https://apicarto.ign.fr/api/codes-postaux/communes/'+self.code_postal

        # Requête url
        response = requests.get(url)
        
        # Si le code postal a été retrouvé (code http : 200)
        if response.status_code == 200:

            # Récupération du contenu au format json
            data = json.loads(response.content)
            # pprint.pprint(data)

            # Liste des communes
            city_list = [i['nomCommune'] for i in data]
            
            # Conversion en df pandas
            city_df = pd.DataFrame({"Commune(s)": city_list})
            
            # Titre à afficher
            st.write(f"Communes avec le code postal suivant : {self.code_postal}")
            
            # DF à afficher
            st.data_editor(
                city_df,
                column_config={
                    "widgets": st.column_config.Column(
                        "Commune(s)",
                        width="medium",
                        required=True,
                    )
                },
                hide_index=True, # index masqué
                num_rows="dynamic",
            )
        
        # À défaut (code http : 404) 
        else:
            
            st.warning(
                f'Communes non retrouvée pour le code postal : {self.code_postal}',
                icon="⚠️")

if __name__ == '__main__':
    
    application = FrontEnd()
