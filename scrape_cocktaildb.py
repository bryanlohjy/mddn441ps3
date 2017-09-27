# Create json of cocktail info
import requests
from bs4 import BeautifulSoup, Comment

data = {
    'cocktails': {},
    'source': 'http://www.cocktaildb.com'
}

def return_text(x):
    return x.get_text()

for i in range(4758):
    if (i % 10 == 0): # download every 10th entry to save time
        url = 'http://www.cocktaildb.com/recipe_detail?id={}'.format(i+1)
        raw_html = requests.get(url).text
        soup = BeautifulSoup(raw_html, 'html.parser')
        if (soup):
            cocktail = soup.find(id='wellTitle')
            if (cocktail):
                c_name = cocktail.find('h2').get_text()
                data['cocktails'][c_name] = {
                    'recipe': list(map(return_text, soup.find_all(class_='recipeMeasure'))),
                    'directions': list(map(return_text, soup.find_all(class_='recipeDirection')))
                }
                print(i)

import json
with open('data/cocktails.json', 'w') as outfile:
    json.dump(data, outfile)
    print('File written')