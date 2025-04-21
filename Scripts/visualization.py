from pyvis.network import Network
from os import path
import json
import math

# System Input files
analysis_directory = path.join("..", "AnalysisArtifacts")
adjacency_list_filepath = path.join(analysis_directory, "adjacencylist.json")
combos_by_effect_filepath = path.join(analysis_directory, "combos_by_effect.json")
card_summaries_filepath = path.join(analysis_directory, "card_summaries.json")

combo_directory = path.join("..", "ComboParserArtifacts")
card_data_filepath = path.join(combo_directory, "card_data.json")
combo_data_filepath = path.join(combo_directory, "combo_data.json")

# Output files
output_directory = path.join("..", "VisualizationArtifacts")
combo_vis_filepath = path.join(output_directory, "combovis.html")

def load_data(filepath):
    with open(filepath, 'r') as f:
            return json.loads(f.read())
    
def prepare_title(card):
     title = "Name: " + str(card["name"])
     title += "\nis_missing: " + str(card["is_missing"])
     title += "\ncurrent_combos: " + str(len(card["current_combo_ids"]))
     title += "\ncombos_missing_this_card: " + str(len(card["combos_missing_this_card_ids"]))
     title += "\ncombos_missing_another_card: " + str(len(card["combos_missing_another_card_ids"]))
     title += "\naverage_cards_per_current_combo: " + "{:.2f}".format(card["average_cards_per_current_combo"])
     title += "\naverage_cards_per_all_combo: " + "{:.2f}".format(card["average_cards_per_all_combo"])
     return title
     
def prepeare_mass(card, max_combos):
    combo_count = len(card["current_combo_ids"])
    ratio = max_combos / combo_count if combo_count > 0 else max_combos
    mass = 1 + math.log2(ratio)
    return mass

def main():
    combo_net = Network(height="100vh", width="100%")
    combo_net.barnes_hut()

    try:
        adjaceny_list:dict = load_data(adjacency_list_filepath)
        combos_by_effect:dict = load_data(combo_data_filepath)
        card_summaries:dict = load_data(card_summaries_filepath)
        card_data:dict = load_data(card_data_filepath)
        combo_data:list = load_data(combo_data_filepath)
    except FileNotFoundError as e:
        return -1

    cardnames = list(adjaceny_list.keys())
    max_combos = max([len(card["current_combo_ids"]) for card in card_summaries.values()])
    print(max_combos)
    for i, cardname in enumerate(cardnames):
        card = card_summaries[cardname]
        title = prepare_title(card)
        label=card["name"]
        image=card_data[label]["src"]
        mass = prepeare_mass(card, max_combos)
        combo_net.add_node(n_id=i, title=title, shape="image", image=image, size=100, mass=mass)

    for i, card in enumerate(cardnames):
        for adjacency in  adjaceny_list[card]:
            adj_i = cardnames.index(adjacency)
            
            color = "#02baf7"
            if card_data[card]["missing"] == True or card_data[adjacency]["missing"] == True:
                color = "grey"
            
            if adj_i != -1:
                combo_net.add_edge(i, adj_i, color=color) 

    combo_net.show(combo_vis_filepath, notebook=False)

    return 0
         

if __name__ == "__main__":
    rtn = main()
    exit(rtn)