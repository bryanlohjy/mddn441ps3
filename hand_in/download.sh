# Create necessary directories
mkdir temp_data
mkdir idml_files

# Load wine descriptions
wget https://raw.githubusercontent.com/dariusk/corpora/master/data/foods/wine_descriptions.json --directory-prefix=data
# Load beer categories
wget https://raw.githubusercontent.com/dariusk/corpora/master/data/foods/beer_categories.json --directory-prefix=data
# Load beer styles
wget https://raw.githubusercontent.com/dariusk/corpora/master/data/foods/beer_styles.json --directory-prefix=data
# Load condiments
wget https://raw.githubusercontent.com/dariusk/corpora/master/data/foods/condiments.json --directory-prefix=data
# Load breads_and_pastries
wget https://raw.githubusercontent.com/dariusk/corpora/master/data/foods/breads_and_pastries.json --directory-prefix=data
# Load menuItems
wget https://raw.githubusercontent.com/dariusk/corpora/master/data/foods/menuItems.json --directory-prefix=data
# Downloading images of beer cans from craftcans.com
wget --adjust-extension \
     --random-wait \
     --limit-rate=100k \
     --span-hosts \
     --convert-links \
     --backup-converted \
     --no-directories \
     --timestamping \
     --page-requisites \
     --directory-prefix=data/cans \
     --execute robots=off \
     -A "*.jpg" \
     http://www.craftcans.com/db.php?cat=cans

# Downloading images of beer cans from ebay - craftcans.com seems to be temperamental
wget --adjust-extension \
     --random-wait \
     --limit-rate=100k \
     --span-hosts \
     --convert-links \
     --backup-converted \
     --no-directories \
     --timestamping \
     --page-requisites \
     --directory-prefix=data/cans \
     --execute robots=off \
     -A "*.jpg" \
     http://www.ebay.com/bhp/old-beer-cans

# Data for cocktail generator
# song lyrics
wget -O data/lyrics.csv \
https://raw.githubusercontent.com/walkerkq/musiclyrics/master/billboard_lyrics_1964-2015.csv
# cocktail images
wget --adjust-extension \
     --random-wait \
     --span-hosts \
     --convert-links \
     --backup-converted \
     --no-directories \
     --timestamping \
     --page-requisites \
     --directory-prefix=data/images \
     --execute robots=off \
     -A "*.jpg" \
     'http://www.thecocktaildb.com/index.php'

# Scrap cocktail db database with BeautifulSoup
python scrape_cocktaildb.py