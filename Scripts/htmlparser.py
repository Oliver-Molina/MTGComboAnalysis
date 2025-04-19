from bs4 import BeautifulSoup
import re
import json
from os import path 


# System Input Files
input_directory = path.join("..", "WebScraperArtifacts")
html_filepath = path.join(input_directory, "webpage.html")

# Output Files
output_directory = path.join("..", "ComboParserArtifacts")
combo_data_filepath = path.join(output_directory, "combo_data.json")
card_data_filepath = path.join(output_directory, "card_data.json")

def clean_li(li_tag):
    text = li_tag.get_text(separator=' ', strip=True)
    cleaned = re.sub(r"\s+([’'.,!?;:])", r"\1", text) # Remove spaces before punctuation
    cleaned = re.sub(r'\s+', ' ', cleaned).strip() # Compress whitespace
    return cleaned

# Step 1: Load the HTML file
html_content = ""
with open(html_filepath, 'r', encoding='utf-8') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')

# Step 2: Find the main container
app_div = soup.find('div', {'id': 'app'})

# Step 3: Extract combo-details sections
combo_details = []
card_data = dict()

for combo in app_div.find_all('details'):
    # Extract colors
    colors = combo.get("colors", "")
    
    # Check for potential-combo-entry class
    category = "potential" if "potential-combo-entry" in combo.get("class", []) else "current"
    
    # Extract combo card names and image links
    card_images = combo.find("summary").find("div", class_='card-images').find_all("img")
    required_cards = []
    missing_cards = []
    for image in card_images:
        title = image.get('title', '')
        missing = "missing" in image.get('class', [])

        if missing:
            missing_cards.append(title)
        else:
            required_cards.append(title)

        if card_data.get(title) is None:
            card_details = dict()
            card_details["src"] = image.get('src', '')
            card_details["missing"] = missing
            card_data[title] = card_details

    combo_block = combo.find('div', class_='combo-details')
    if combo_block:
        ul_tags = combo_block.find_all('ul')

        # Clean each li properly
        results = [clean_li(li) for li in ul_tags[0].find_all('li')]
        prerequisites = [clean_li(li) for li in ul_tags[1].find_all('li')]
        steps = [clean_li(li) for li in ul_tags[2].find_all('li')]

        combo_details.append({
            'colors': colors,
            'required_cards': required_cards,
            'missing_cards': missing_cards,
            'prerequisites': prerequisites,
            'steps': steps,
            'results': results,
        })

# Step 4: Output or save the data
with open(combo_data_filepath, 'w', encoding="utf-8") as f:
    f.write(json.dumps(combo_details, indent=2))

with open(card_data_filepath, 'w', encoding="utf-8") as f:
    f.write(json.dumps(card_data, indent=2))
