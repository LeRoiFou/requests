"""
Test : récupération de la dénonimation de la société à partir du site INSEE
Librairie utilisée : api_insee

Pour récupérer la clé et le mdp sur le site INSEE :
https://api.insee.fr/catalogue/site/themes/wso2/subthemes/insee/pages/help.jag#commencer

Date : 16-12-2023
"""

from api_insee import ApiInsee
import configparser
import pprint

# Récupération des codes du fichier .ini
access_data = configparser.ConfigParser()
access_data.read('data_insee.ini')

# Obtention de la clé et du code secret
key_ini = access_data.get('INSEE', 'cle')
secret_ini = access_data.get('INSEE', 'secret')

# Instanciation de la librairie ApiInsee avec clé et code secret récupérés
api = ApiInsee(
    key = key_ini,
    secret = secret_ini
)

# Obtention des données selon le SIREN choisi
number_company = '005520135'
data = api.siren(number_company).get()
pprint.pprint(data)

# Récupération du nom de la société
company_name = data['uniteLegale']['periodesUniteLegale'][0]['denominationUniteLegale']
print(f"Nom de la société : {company_name}")
