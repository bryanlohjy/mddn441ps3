#  Read + filter lyrics ==============
from __future__ import unicode_literals
import csv
import random
import os
import spacy
import tracery
from tracery.modifiers import base_english
import json
import numpy as np
from numpy import dot
from numpy.linalg import norm

lyrics_raw = csv.DictReader(open('data/lyrics.csv',  encoding='ISO-8859-1'))
lyrics = []
for row in lyrics_raw:
    # Keys: Rank, Song, Artist, Year, Lyrics, Source
    not_obscure = (int(row['Year']) >= 2010 and int(row['Rank']) < 50) or (int(row['Rank']) <= 5 and int(row['Year']) >= 1994)
    if (not_obscure) :
        lyrics.append({
            'rank': row['Rank'],
            'song': row['Song'],  
            'artist': row['Artist'],
            'year': row['Year'],
            'lyrics': row['Lyrics'],
            'source': row['Source']
        });

# NLP vector helpers ========================
nlp = spacy.load('en')
def vec(s):
    return nlp.vocab[s].vector

# cosine similarity
def cosine(v1, v2):
    if norm(v1) > 0 and norm(v2) > 0:
        return dot(v1, v2) / (norm(v1) * norm(v2))
    else:
        return 0.0
    
def spacy_closest(token_list, vec_to_check, n=30):
    return sorted(token_list,
                  key=lambda x: cosine(vec_to_check, vec(x)),
                  reverse=True)[:n]


def word_count(token_list):
    count = {} 
    for token in token_list:
        text = str(token.text).strip()
        if (len(text) > 0):
            if (text not in count.keys()):
                count[text] = 0

            count[text] += 1
    return count

def addv(coord1, coord2):
    return [c1 + c2 for c1, c2 in zip(coord1, coord2)]

# Create cocktail content =========================
# Misc Helpers ======================
def get_flavour_nouns(drink):
    drink_recipe_doc = nlp(' '.join(drink['recipe']))
    drink_recipe_tokens = list(set([w.text for w in drink_recipe_doc if w.is_alpha]))
    flavours = []
    # extract list of flavours from recipe
    for w in drink_recipe_doc:
        if (w.pos_ in ['NOUN', 'PROPN'] and w.text.lower() not in flavours and w.text.lower() not in ['sec', 'cl', 'gills', 'tsp', 'oz', 'splash', 'dashes', 'teaspoon', 'dash']):
            if(w.text.lower() == 'vermouth'):
                flavours.append('{} vermouth'.format('dry'))
            else:
                flavours.append(w.text)            
    return flavours

def get_vocab(s, d): # create a vocabulary from the lyrics based loosely on the recipe of the drink
    lyric_doc = nlp(s['lyrics'])
    lyric_tokens = list(set([w.text for w in lyric_doc if w.is_alpha]))
    spacy_closest(lyric_tokens, vec('flavour'))
    flavours = get_flavour_nouns(d);
    # for each flavour identified, find closest words in lyrics and collect by part of speech 
    flav_words = {}
    for flav in flavours:
        neighbours = spacy_closest(lyric_tokens, vec(flav))
        if (len(neighbours) > 0):
            neighbour_doc = nlp(' '.join(neighbours))
            for i in neighbour_doc:
                noun_blacklist = ['what', 'bought', 'm', 'tres', 'gon']
                adj_blacklist = ['nt', 'whatever', 'youyou', 'half', 'tell', 'ya', 'm', 'its', 'my', 'betweenchorus', 'i', 'you', 'me', 'homeand', 'most', 'least', 'second', 'tryna', 'their', 'her', 'want', 'moment', 'enough', 'much', 'sharpen', 'that', 'better', 'your', 'what', 'his', 'yours', 'wanna', 'last', 'my', 'give', 'got']
                if (i.pos_ == 'ADJ' and (i.text.lower().strip() not in adj_blacklist)):
                    if (i.pos_ not in flav_words.keys()):
                        flav_words[i.pos_] = []  
                    flav_words[i.pos_].append(i.text)
                elif (i.pos_ == 'NOUN' and (i.text.lower().strip() not in noun_blacklist)):
                    if (i.pos_ not in flav_words.keys()):
                        flav_words[i.pos_] = []  
                    flav_words[i.pos_].append(i.text)                    
                elif (i.pos_ != 'ADJ' and i.pos_ != 'NOUN'):
                    if (i.pos_ not in flav_words.keys()):
                        flav_words[i.pos_] = []  
                    flav_words[i.pos_].append(i.text)
    return flav_words

def get_foods():
    data = {}
    data['condiment'] = json.loads(open("./data/condiments.json").read())['condiments']
    data['bread'] = json.loads(open("./data/breads_and_pastries.json").read())['breads']
    data['pastry'] = json.loads(open("./data/breads_and_pastries.json").read())['pastries']
    data['menu_item'] = json.loads(open("./data/menuItems.json").read())['menuItems']
    data['wine_descriptions'] = json.loads(open("./data/wine_descriptions.json").read())['wine_descriptions']
    data['beer_categories'] = json.loads(open("./data/beer_categories.json").read())['beer_categories']
    data['beer_styles'] = json.loads(open("./data/beer_styles.json").read())['beer_styles']
    return data

def humanise_name(n):
    return n.lower().replace('featuring', '&').replace('and', '&').replace('"', '').strip().title().replace('Jayz', 'Jay-Z').replace('Keha', 'Ke$ha')

# Generate content ======================
def get_drink_title(s, d):
    case = random.randint(0, 4)
    if (len(s['song'].split()) > 1 and case == 0):  # replace alcohol with artist name
        nlp = spacy.load('en')
        song_title_doc = nlp(s['song'])
        drink_doc = nlp(d['name'])
        case2 = random.randint(0, 1)
        name = []
        replaced = False
        for w in song_title_doc:
            if ((w.pos_ == 'NOUN' or w.pos_ == 'ADJ' or w.pos_ == 'PRON') and replaced == False):
                drink_tokens = list(set([z.text for z in drink_doc if z.is_alpha]))
                neighbours = spacy_closest(drink_tokens, vec('liquour'))
                if (len(neighbours) >= 1):
                    alcohol_name = neighbours[0]
                    name.append(alcohol_name)
                    replaced = True
            else:
                name.append(w.text)
        apostrophe = '\'' if (s['artist'][-1].lower() == 's') else '\'s'
        return '{}{} {}'.format(humanise_name(s['artist']), apostrophe, humanise_name(' '.join(name)))
    elif (case == 1): # artist's song name
        apostrophe = '\'' if (s['artist'][-1].lower() == 's') else '\'s'
        return '{}{} {}'.format(humanise_name(s['artist']), apostrophe, humanise_name(s['song']))      
    else: # artist's #DRINK#
        apostrophe = '\'' if (s['artist'][-1].lower() == 's') else '\'s'
        return '{}{} {}'.format(humanise_name(s['artist']), apostrophe, d['name'])

def get_drink_description(s, d):
    description_rules = get_foods()
    description_rules['artist'] = humanise_name(s['artist'])
    description_rules['drink1'] = d['name']
    description_rules['drink2'] = random.choice(list(drink_data['cocktails'].items()))[0]
    description_rules['first_sentence'] = ['#ADJ.a.capitalize# mix between the #drink1# and the #drink2#', '#ADJ.a.capitalize# variant of the #drink1#']
    vocab = get_vocab(s, d)
    if ('ADJ' in vocab.keys()):
        description_rules['ADJ'] = vocab['ADJ']
    else:
        description_rules['ADJ'] = ['aged', 'worn', 'weathered']
        
    if ('NOUN' in vocab.keys()):
        description_rules['NOUN'] = vocab['NOUN']
    else:
        description_rules['NOUN'] = ['flow', 'music', 'crib']
        
    apostrophe = '\'' if (s['artist'][-1].lower() == 's') else '\'s'
        
    description_rules['base'] = "#first_sentence#. As #ADJ# as #artist#{} #NOUN#.".format(apostrophe)  
    description = tracery.Grammar(description_rules)
    description.add_modifiers(base_english)
    return description.flatten('#base#')

def get_pairing(s, d):
    vocab = get_vocab(s, d)
    pairing_rules = get_foods()
    pairing_rules['artist'] = s['artist']
    if ('ADJ' in vocab.keys()):
        pairing_rules['ADJ'] = vocab['ADJ']
    else:
        pairing_rules['ADJ'] = ['aged', 'worn', 'weathered']
        
    plural_artist = 'has'
    if ('&' in humanise_name(s['artist'])):
        plural_artist = 'have'
    pairing_rules['base'] = "{} it with #ADJ.a# #menu_item# and #pastry#.".format('{} {}'.format(humanise_name(s['artist']), plural_artist))
    
    pairing = tracery.Grammar(pairing_rules)
    pairing.add_modifiers(base_english)
    return pairing.flatten('#base#')
    
def get_drink_style(s, d):
    description_rules = get_vocab(s, d)
    if ('ADJ' not in description_rules.keys()):
        description_rules['ADJ'] = ['passable', 'tender', 'loud']
    
    description_rules['second_adj'] = ['', ' and #ADJ#', ', #ADJ# and #ADJ#']
    description_rules['base'] = ['#ADJ.capitalize##second_adj#.']
    description = tracery.Grammar(description_rules)
    description.add_modifiers(base_english)
    return description.flatten('#base#')

def get_drink_notes(s, d):
    vocab = get_vocab(s, d)
    if ('NOUN' not in vocab.keys()):
        vocab['NOUN'] = ['hair', 'music', 'party']
        
    note_noun = random.choice(vocab['NOUN']).title()
    
    flavours = get_flavour_nouns(d)
    notes_text = []
    if (len(flavours) > 0):
        for i in range(len(flavours)):
            if (i < 2):
                notes_text.append(flavours[i].title())
    return (str(', '.join(notes_text)) + ' and a {} of {}.'.format(random.choice(['hint', 'dash']), note_noun.lower()))
    
def get_drink_serving(s, d):
    vocab = get_vocab(s, d)
    if ('ADJ' not in vocab.keys()):
        vocab['ADJ'] = ['passable', 'tender', 'loud']
        
    if(len(d['directions']) > 0):
        serving = random.choice(d['directions'])
        return '{}. {}.'.format(serving, 'Drink to the {} sounds of {}'.format(random.choice(vocab['ADJ']), s['song'].title()))
    else:
        return random.choice(['Enjoy cold.', 'On the rocks.'])

def get_image(i = 'z'):
    images = os.listdir('./data/images')
    if (i == 'z'):
        return random.choice(images)
    else:
        return images[i % len(images)]

def get_drink(s, d, i):
    content = {
        'title': get_drink_title(s, d),
        'description': get_drink_description(s, d),
        'brewed_date': s['year'],
        'style': get_drink_style(s, d),
        'alcohol_content': "{}%".format(round(random.random() + float(s['rank']), 1)),
        'notes': get_drink_notes(s, d),
        'pairing': get_pairing(s, d),
        'serving_suggestion': get_drink_serving(s, d),
        'image': get_image(i)
    }
    return content

data_array = []
for i in range(20):
    # Selecting random data ======================
    drink_data = {};
    with open('data/cocktails.json') as d:
        data = json.load(d)
        d.close()
        drink_data = data

    song = random.choice(lyrics)
    song['song'].replace('suit  tie', 'suit and tie')

    d = random.choice(list(drink_data['cocktails'].items()))
    drink = {
        'name': d[0],
        'directions': d[1]['directions'],
        'recipe': d[1]['recipe']   
    }
    # Generate content
    data_array.append(get_drink(song, drink, i))

out_data = { 'content': data_array }
for i in range(len(out_data['content'])):
    item = out_data['content'][i]
    with open('temp_data/cocktail-{:02d}.csv'.format(i),'w') as file:
        for key in item.keys():
            file.write('{}\t{}'.format(key, item[key]))
            file.write('\n')
