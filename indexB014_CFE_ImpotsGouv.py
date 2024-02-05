"""
Accès à la déclaration CFE du site impôts.gouv à partir de l'identifiant et du
code d'accès au site, en listant les n° de SIREN et les dénominations de sociétés
pour lesquels l'usager dispose des habilitations

Lien : https://www.linkedin.com/feed/update/urn:li:activity:7159872812692742144/
Github : https://github.com/Fabrice-Heuvrard/RPA_CFE-Cotisation-Fonciere-Entreprise/tree/main

Date : 05-02-24
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os

# Assignation de variables
url = "https://cfspro-idp.impots.gouv.fr/oauth2/authorize?[...]"
credentials_file = "data/identifiants.txt" # récup identifiant
file_path = "data/SIREN2.TXT" # récup SIREN et dénominations des sociétés

def initialize_driver():
    """
    Return : connexion par google chrome
    """
    
    # Assignation en str du chemin rattaché à ce fichier : 
    # (Résultat : C:\Users\LRCOM\pythonProjects\requests)
    current_directory = os.getcwd()
    
    # Assignation en str de la connexion à google chrome
    chrome_options = Options()
    
    # Connexion au google chrome
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": current_directory,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    })
    
    return webdriver.Chrome(options=chrome_options)

def connect_to_website_with_credentials(driver, url, credentials_file):
    driver.get(url)

    # Vérification si déjà connecté
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "identifiant_après_connexion")))
        print("Déjà connecté.")
        return driver
    except:
        print("Pas encore connecté. Procédure de connexion en cours.")

    with open(credentials_file, "r") as file:
        lines = file.readlines()
        username = lines[0].strip()
        password = lines[1].strip()

    username_input = driver.find_element(By.ID, "ident")
    password_input = driver.find_element(By.NAME, "password")

    username_input.send_keys(username)
    password_input.send_keys(password)

    login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Connexion')]")
    login_button.click()
    sleep(1)

    return driver

# TODO
def rename_downloaded_pdf(siren_number, company_name, download_directory):
    original_file = os.path.join(download_directory, "doc.pdf")
    new_file_name = f"{siren_number}_{company_name.replace(' ', '_')}.pdf"  
    new_file = os.path.join(download_directory, new_file_name)

    if os.path.exists(original_file):
        os.rename(original_file, new_file)
        print(f"Le fichier PDF a été renommé en : {new_file}")
    else:
        print("Le fichier 'doc.pdf' n'a pas été trouvé.")
        
        
def read_siren_data(file_path):
    """
    Argument : récupération du fichier 'data/SIREN2.txt'
    Return : une liste de tous les dénominations figurant dans le fichier .txt
    """
    
    # Assignation d'une liste
    siren_data = []
    
    # Récupération des données du fichier .txt
    with open(file_path, "r") as file:
        
        # Pour chaque ligne du fichier .txt...
        for line in file:
            
            # Insertion dans une liste pour chaque ligne du fichier .txt
            parts = line.strip().split(",", 1)
            
            # Si pour chaque liste il y a deux composants (n° SIREN et dénomination)
            if len(parts) == 2:
                
                # Récupération des données du 2ème composant : dénomination
                company_name = parts[1].strip()
                
                # Ajout des dénominations des sociétés dans une liste
                siren_data.append(company_name)

    return siren_data

def extract_valid_siren_numbers(file_path):
    """
    Argument : récupération du fichier 'data/SIREN2.txt'
    Return : une liste de tous les n° SIREN figurant dans le fichier .txt
    """
    
    # Assignation d'une liste
    siren_numbers = []

    # Récupération des données du fichier .txt
    with open(file_path, "r") as file:
        
        # Pour chaque ligne du fichier .txt...
        for line in file:
            
            # Insertion dans une liste pour chaque ligne du fichier .txt
            parts = line.strip().split(",", 1)
            
            # Si pour chaque liste il y a deux composants (n° SIREN et dénomination)
            if len(parts) == 2:
                
                # Récupération des données du 1er composant : n° SIREN
                siren_number = parts[0].strip()

                # Vérifier que siren_number contient exactement 9 chiffres
                if len(siren_number) == 9 and siren_number.isdigit():
                    
                    # Ajout des n° de SIREN dans une liste
                    siren_numbers.append(siren_number)
                   
    return siren_numbers

def main():

    # Récupération des n° SIREN du fichier 'data/SIREN2.txt' dans une liste
    siren_numbers = extract_valid_siren_numbers(file_path)

    # Récupération des dénominations du fichier 'data/SIREN2.txt' dans une liste
    name_company_list = read_siren_data(file_path)

    # Assignation d'un compteur
    compteur  = 0
    
    # Pour chacun des SIREN de la liste...
    for siren in siren_numbers:
        
        # Assignation du n° SIREN récupéré
        siren = siren
        
        # Assignation de la dénomination de la société au composant n° 'compteur'
        name = name_company_list[compteur]
        
        # Connexion par google chrome
        driver = initialize_driver()

        # Connexion au site impôts.gouv avec identifiant et mdp
        driver = connect_to_website_with_credentials(driver, url, credentials_file)

        print("Connexion à la page d'accueil")
        driver.get("https://cfspro.impots.gouv.fr/mire/accueil.do")
   
        print("Je clique sur Avis CFE")
        avis_cfe_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Avis CFE')]")
        avis_cfe_link.click()
 
        for i in range(9):
            siren_input = driver.find_element(By.ID, f"siren{i}")
            siren_input.send_keys(siren[i])

        consulter_button = driver.find_element(By.NAME, "button.submitValider")
        consulter_button.click()

        #sleep(2)

        window_handles = driver.window_handles
        driver.switch_to.window(window_handles[-1])

        #sleep(2)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Accès aux avis de CFE')]")))

        acces_cfe_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Accès aux avis de CFE')]")
        acces_cfe_button.click()

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, "Avis d'imposition")))

        avis_imposition_link = driver.find_element(By.LINK_TEXT, "Avis d'imposition")
        avis_imposition_link.click()

        demandes_impression_image = driver.find_element(By.XPATH, '//img[@alt="Demandes d\'impression"]')
        demandes_impression_image.click()

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, "Tout le document")))
        tout_document_link = driver.find_element(By.LINK_TEXT, "Tout le document")
        tout_document_link.click()

        driver.switch_to.window(driver.window_handles[-1])

        wait = WebDriverWait(driver, 20)
        print_image = wait.until(EC.presence_of_element_located((By.XPATH, "//img[@alt='Imprimer - PDF 33 Ko']")))

        # Si l'image est présente, vous pouvez cliquer dessus ou effectuer d'autres actions
        print_image.click()      
        wait = WebDriverWait(driver, 90)
        tout_effacer_link = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Tout effacer')]")))

        # Si le lien "Tout effacer" est présent, cliquez dessus
        tout_effacer_link.click()
        print("Le lien 'Tout effacer' a été cliqué avec succès.")

        rename_downloaded_pdf(siren,  name, os.getcwd())

        # Fermez le navigateur à la fin
        driver.quit()

        compteur = compteur +1

    print("Script terminé !")


if __name__ == "__main__":
    main()
