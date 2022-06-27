import requests
from fake_headers import Headers

from bs4 import BeautifulSoup
from pprint import pprint

header = Headers().generate()

cars = {} # Dict med alla hitboxes som keys och bilar i en lista som values

req = requests.Session()
response = req.get("https://support.rocketleague.com/hc/en-us/articles/360029832054-Rocket-League-Car-Hitboxes", headers=header)

if response.status_code == 403:
    raise Exception(f"{response.status_code} rejected. \nResponse headers: {response.headers}\nResponse Text: {response.text}")

soupContent = BeautifulSoup(response.content, 'html.parser')

def getCars(cars_list, currentElement):
    # Lägg till bil till car_list
    if currentElement.string != None and currentElement.name != "h4": # Lägg it till NoneTypes i listan av bilar
        cars_list.append(currentElement.string)
    
    if not currentElement.next_sibling:
        return cars_list

    print("\nCurrent tag", currentElement)
    nextTitle = currentElement.find_next_sibling('h4') 
    print("next title:", nextTitle)
    
    # Om det inte finns någon nästa h4 så ska den lägga till p eller a tills div är slut
    # if currentElement.nextSibling.next:
    print("\nnext sibling:", currentElement.next_sibling.next.name)

    # Kolla ifall nästa element är nextTitle eller ifall nextTitle inte är None
    if (currentElement.next_sibling.next == nextTitle) or not nextTitle:      
        # # Om nästa nästa sibling är p eller a så ska den returnera carlist
        if not nextTitle and currentElement.next_sibling.next.name == "p":
            return getCars(cars_list, currentElement.next_sibling.next)
        else:
            return cars_list
    else:
        # Gå vidare till nästa bil 
        return getCars(cars_list, currentElement.next_sibling.next)

def getHitboxes():
    hitboxes = {}

    article = soupContent.find("div", class_="article-body")
    
    # Undvik att skiten crashar ifall den inte hittar articlen
    if not article:
        print("The article is a NoneType exiting:", article)
        return None

    for hitbox_type in article.find_all('h4'):
        print(hitbox_type)
        if hitbox_type.text == '\xa0':
            continue

        hitbox = hitbox_type.string
        hitbox_fixed = hitbox_type.string.replace(" Hitbox", "")
        
        hitboxes[hitbox_fixed] = getCars([], currentElement=article.find("h4", string=hitbox))
            
    return hitboxes

cars = getHitboxes()

pprint(cars)

