import json
import ast
wine_descriptions = json.loads(open("./data/wine_descriptions.json").read())['wine_descriptions']
beer_categories = json.loads(open("./data/beer_categories.json").read())['beer_categories']
beer_styles = json.loads(open("./data/beer_styles.json").read())['beer_styles']

condiments = json.loads(open("./data/condiments.json").read())['condiments']
breads = json.loads(open("./data/breads_and_pastries.json").read())['breads']
pastries = json.loads(open("./data/breads_and_pastries.json").read())['pastries']
menuItems = json.loads(open("./data/menuItems.json").read())['menuItems']

import tracery
from tracery.modifiers import base_english

template = {
    "title": "",
    "description": "",
    "brewed_date": "",
    "style": "",
    "alcohol_content": "",
    "notes": "",
    "pairing": "",
    "serving_suggestion": ""
}

data = []

import random
import copy
import os

def random_pick(arr):
  return arr[random.randrange(0, len(arr) -1)]

for i in range(20):
    base_description = random_pick(wine_descriptions)
    base_style = random_pick(beer_styles)
    base_category = random_pick(beer_categories)
    
    title_rules = {
        "title": "#description.capitalize# #style#",
        "description": base_description,
        "style": base_style
    }
    description_rules = {
        "description": "#adj.a.capitalize# #relation# to the#beer_style#. As refreshing as #temperature.a# #pastry# dipped in #condiment.a#",
        "adj": ["long-lost", "estranged", "blood-bonded"],
        "relation": ["half-brother", "step-cousin", "half-removed god-daughter"],
        "beer_style": beer_styles,
        "temperature": ["freezingly cold", "swelteringly hot", "pretentiously lukewarm"],
        "pastry": pastries,
        "condiment": condiments
    }
    notes_rules = {
        "notes": ["#condiment.capitalize#, #noun#, #pastry#, and #adj# #food#"],
        "adj": ["aged", "worn", "rotten", "fresh", "youthful"],
        "food": menuItems,
        "condiment": condiments,
        "noun": ["bark", "citrus", "door", "window"],
        "pastry": pastries
    }
    pairing_rules = {
        "pairing": ["Goes well with #bread.a# dipped in #adj.a# #condiment#"],
        "adj": ["aged", "worn", "rotten", "fresh", "youthful"],
        "condiment": condiments,
        "bread": breads
    }
    serving_rules = {
        "serving": ["#verb.capitalize# #temperature#, on #adj.a# #noun#"],
        "verb": ["enjoy", "sip", "indulge"],
        "temperature": ["freezingly cold", "swelteringly hot", "pretentiously lukewarm"],
        "adj": ["aged", "worn", "rotten", "fresh", "youthful"],
        "noun": ["yacht", "electric bicycle", "solar powered segway"]
    }
    
    title = tracery.Grammar(title_rules)
    title.add_modifiers(base_english)

    description = tracery.Grammar(description_rules)
    description.add_modifiers(base_english)
    
    notes = tracery.Grammar(notes_rules)
    notes.add_modifiers(base_english)
    
    pairing = tracery.Grammar(pairing_rules)
    pairing.add_modifiers(base_english)
    
    serving = tracery.Grammar(serving_rules)
    serving.add_modifiers(base_english)
    
    tempData = copy.copy(template)
    tempData["title"] = title.flatten("#title#")
    tempData["description"] = description.flatten("#description#")
    tempData["brewed_date"] = random.randrange(1980, 2017)
    tempData["style"] = "A {} {}".format(base_description, base_category)
    tempData["alcohol_content"] = "{}%".format(round(random.random() * 20, 1))
    tempData["notes"] = notes.flatten("#notes#")
    tempData["pairing"] = pairing.flatten("#pairing#")
    tempData["serving_suggestion"] = serving.flatten("#serving#")
    tempData["image"] = random_pick(os.listdir('./data/cans'))
    data.append(tempData)

out_data = { 'content': data }

# writing out a json file of contents
with open('content.json', 'w') as outfile:
    json.dump(out_data, outfile)
