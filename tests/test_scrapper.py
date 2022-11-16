
from scrapper import description, descriptionlien,comment
import requests
from bs4 import BeautifulSoup
import re  

import json as json  



def test_description():
     # saisir l'URL
    url="https://www.youtube.com/watch?v=IzRGy4dvJpA"

    # importer le code de la page
    response=requests.get(url)
    soup=BeautifulSoup(response.text,"html.parser")
    #Json de la page url 
    data = re.search(r"var ytInitialData = ({.*?});", soup.prettify()).group(1)  
    data_json = json.loads(data)
    assert description(data_json)=="A little bit of nostalgia...\nI am sorry but you won't find this particular version anywhere but here. This a version I made myself."


def test_descriptionlien():
     # saisir l'URL
    url="https://www.youtube.com/watch?v=IzRGy4dvJpA"

    # importer le code de la page
    response=requests.get(url)
    soup=BeautifulSoup(response.text,"html.parser")
    #Json de la page url 
    data = re.search(r"var ytInitialData = ({.*?});", soup.prettify()).group(1)  
    data_json = json.loads(data)
    assert descriptionlien(data_json)==""

def test_comment():
     url="https://www.youtube.com/watch?v=IzRGy4dvJpA"
     assert comment(url)==["Season 1 : Should I Stay or Should I Go (Will and Jonathan)\r\nSeason 2 : Every Breath You Take (El and Mike)\r\nSeason 3 : Never Ending Story (Dustin and Suzie)\r\nSeason 4 : Running Up That Hill (Max and Billy)",
                "What really great about the Duffer Brothers is their ability to affect the audience with the music used in \"Stranger Things\". They don't only give young people an opportunity to feel the heartbeat of the 80s but also provide older generation a feeling of nostalgia of the time the showrunners were living in.",
                "I thought I'm the only one who cried with Max's story  :(",
                "I lost my big brother and grandma in a car accident 3 weeks ago. This song has helped me and now has new meaning to me.",
                "Honestly, this version does the one thing I wish from the original- bringing the vocals up to the front of the recording, rather than back in the mix."
            ]