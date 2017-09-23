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