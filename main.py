import spacy
import requests
import pycld2 as cld2
from bs4 import BeautifulSoup
import random as rand


# r = requests.get("https://en.wikipedia.org/wiki/Will_Smith")
# # soup = BeautifulSoup(r.content, "html.parser")

empty = []
people = []
links = []
limit = 50
graph = {}

def search(links, destination):
    for element in links:
        if element[1] == destination:
            return True 
    return False

def get_links(data,graph,destination,limite,path=[]):
    limit = 75
    people = []
    links = []
    empty = []

    if limite == 10:
        return False, path

    r = requests.get("https://en.wikipedia.org" + data[0])
    soup = BeautifulSoup(r.content, "html.parser")
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(soup.get_text())
    i = 0
    
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            people.append(str(ent))
            i+=1
        if i == limit:
            break

    people_set = set(people)

    for link in soup.find_all(empty):
        x = (link.get('href'),link.get('title'))
        if x == (None,None) or x[1] == None or x[0] == None or str(x[1]) not in people_set or x in links:
            continue
        links.append(x)
    
    graph[data[1]] = links
    path.append(data[1])

    if search(links,destination):
        path.append(destination)
        return True, path
    else:
        limite+=1 
        if links[0][1] in path:
            return get_links(links[rand.randint(1,len(links))], graph, destination,limite,path)  
        return get_links(links[0], graph, destination,limite,path)


p1 = get_links(("/wiki/Tite_Kubo", "Tite Kubo"),graph,"Ichigo Kurosaki",0)
print(p1)
