"""
Test : récupération de la dénonimation de la société à partir du site INSEE
Librairie utilisée : api_insee

Pour récupérer la clé et le mdp sur le site INSEE :
https://api.insee.fr/catalogue/site/themes/wso2/subthemes/insee/pages/help.jag#commencer

Date : 16-12-2023
"""

from api_insee import ApiInsee
import pprint

api = ApiInsee(
    key = 'dvuXoxNNTqdckK4eEpBb77vr2Rca',
    secret = '8ZVP257bzIZB3dNZUnIBjXbIo_8a'
)

data = api.siren('005520135').get()
pprint.pprint(data)

company_name = data['uniteLegale']['periodesUniteLegale'][0]['denominationUniteLegale']
print(f"Nom de la société : {company_name}")
