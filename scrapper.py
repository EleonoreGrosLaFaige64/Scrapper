import requests
from bs4 import BeautifulSoup
import re  
import json as json  
import sys
import argparse
import getopt

import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver


#Fonction pour avoir les commentaires d'une vidéo
def comment(url):
    try:
        s=Service(ChromeDriverManager().install())
        options = Options()
        driver = webdriver.Chrome(service=s, chrome_options=options)
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        commentaires = []
        element = driver.find_element(By.XPATH, "//*[@id=\"comments\"]")
        driver.execute_script("arguments[0].scrollIntoView();", element)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        commentsList = soup.find_all("ytd-comment-thread-renderer", {"class": "style-scope ytd-item-section-renderer"}, limit = 5)
        while commentsList == []:
            time.sleep(1)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            commentsList = soup.find_all("ytd-comment-thread-renderer", {"class": "style-scope ytd-item-section-renderer"}, limit = 5)
        for comment in commentsList:
            commentaires.append(comment.find("yt-formatted-string", {"id": "content-text"}).text)
        return commentaires
    except:
        return "pas de commentaires"

#Fonction pour ecrire dans le fichier output    
def ecrireoutput(Video,output):
    filename = output
    #Copier le cotnenu du fichier output
    with open(filename, "r") as file:
        lst = json.load(file)
    #Ecrire le contenu du fichier ouptut
    with open(filename, mode='w') as f:
        json.dump(lst, f, ensure_ascii=False)
    

    #Rajouter Video a la fin du fichier 
    with open(filename, mode='w') as f:
        lst.append(Video)
        json.dump(lst, f, ensure_ascii=False)

#Fonction pour avoir la description d'une video
def description(data_json):
    #try au cas ou si il n'y a pas de description et qu'une erreur est retourné
    try:
    #Avoir la description de la video
        tab = data_json['contents']['twoColumnWatchNextResults']['results']['results']['contents'][1]['videoSecondaryInfoRenderer']['description']['runs']
        description = ""
        for i in range(len(tab)):

            description = description + tab[i]['text']
        return description
    except:
        return "pas de description"

#Fonction pour avoir les liens presents dans la description de la vidéo
def descriptionlien(data_json):
    try:
        tab = data_json['contents']['twoColumnWatchNextResults']['results']['results']['contents'][1]['videoSecondaryInfoRenderer']['description']['runs']

    #Avoir les liens presents dans la description

        tab_lien = data_json['contents']['twoColumnWatchNextResults']['results']['results']['contents'][1]['videoSecondaryInfoRenderer']['description']['runs']
        description_lien = ""
        for i in range(len(tab_lien)):
            if ("https://" in tab[i]['text']) or ("http://" in tab[i]['text']):
                description_lien = description_lien + tab[i]['text'] + '\n'
        return description_lien
    except:
        return "pas de lien"


#Fonction qui recuere les donnees et appele la fonction ecrireoutput
def ecrire(id,output):

    # saisir l'URL
    url="https://www.youtube.com/watch?v="+id

    # importer le code de la page
    response=requests.get(url)
    soup=BeautifulSoup(response.text,"html.parser")
    #Json de la page url 
    data = re.search(r"var ytInitialData = ({.*?});", soup.prettify()).group(1)  
    data_json = json.loads(data)
    filename = "tmp.json"
    # Ecrire le json dans le fichier tmp
    with open(filename, mode='w') as f:
        json.dump(data_json, f)
   
    #Avoir les likes
    try:
        likes=data_json['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0]['videoPrimaryInfoRenderer']['videoActions']['menuRenderer']['topLevelButtons'][0]['segmentedLikeDislikeButtonRenderer']['likeButton']['toggleButtonRenderer']['defaultText']['accessibility']['accessibilityData']['label']
    except:
        likes="100"
    #Tous les infos de la video youtube
    Video={soup.find("meta", itemprop="videoId")["content"] :{
     "nom":soup.find("meta", itemprop="name")["content"],
     "Autheur":soup.find("span", itemprop="author").next.next['content'],
     "Nombre de pouces bleu":likes,
     "Nombres de vues" :soup.find("meta", itemprop="interactionCount")["content"],
     "Description":description(data_json),
     "Description exeptionnels":descriptionlien(data_json),
     "Id de la video":soup.find("meta", itemprop="videoId")["content"],
     "Les n premiers commentaires":comment(url),}}
    ecrireoutput(Video,output)
    
#Permet de lire les arguments dans la console
def lireArguments(argv):
    input = ''
    output = ''
    try:
        options, args = getopt.getopt(argv,"hi:o:",["input=","output="])
    except getopt.GetoptError:
        print ('scrapper.py --input <inputfile> --output <outputfile>')
        sys.exit(2)
    for opt, arg in options:
        if opt == '-h':
            print ('scrapper.py --input <inputfile> --output <outputfile>')
            sys.exit()
        elif opt in ("-i", "--input"):
            input = arg
        elif opt in ("-o", "--output"):
            output = arg
    return input, output

#Fonctions pour recuperer le json
def main():
    
    input, output =  lireArguments(sys.argv[1:])
    f=open(input)
    data=json.load(f)
    for i in data['videos_id']:
        ecrire(i,output)
    f.close()
if __name__ == "__main__":
    main()




