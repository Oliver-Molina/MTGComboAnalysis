# This file is used to analyze a combo_data json and display useful statistics about your deck.
# Useful Informatiom
# Combo count
# How often each card appears in a combo
# Average number of cards in a combo involving a given card
# For potential cards, how many new combos could be added
# and the average number of cards in potential combos

import json
from os import path
from functools import partial

# User Inputted Files
user_directory = path.join("..", "UserInputtedFiles")
antidecklist_filepath = path.join(user_directory, "antidecklist.txt")

# System Input Files
input_directory = path.join("..", "ComboParserArtifacts")
combos_filepath = path.join(input_directory, "combo_data.json")
card_data_filepath = path.join(input_directory, "card_data.json")

# Output files
output_directory = path.join("..", "AnalysisArtifacts")
adjacency_list_filepath = path.join(output_directory, "adjacencylist.json")
combos_by_effect_filepath = path.join(output_directory, "combos_by_effect.txt")
card_summaries_filename = path.join(output_directory, "card_summaries.txt")

class CardEntry:
    def __init__(self, name, is_missing):
        self.name = name
        self.is_missing = is_missing
        self.current_combo_ids = []
        self.combos_missing_another_card_ids = []
        self.combos_missing_this_card_ids = []
        self.current_combo_results = []
        self.combos_missing_another_card_results = []
        self.combos_missing_this_card_results = []
        self.average_cards_per_current_combo = 0
        self.average_cards_per_all_combo = 0

    def add_combo_info(self, identifier, info:dict):
        if len(info["missing_cards"]) > 0:
            if self.name in info["missing_cards"]:
                self.combos_missing_this_card_ids.append(identifier)
                for result in info["results"]:
                    if result not in self.combos_missing_this_card_results:
                        self.combos_missing_this_card_results.append(result) 
            else:
                self.combos_missing_another_card_ids.append(identifier)
                for result in info["results"]:
                    if result not in self.combos_missing_another_card_results:
                        self.combos_missing_another_card_results.append(result) 
        else:
            self.current_combo_ids.append(identifier)
            for result in info["results"]:
                if result not in self.current_combo_results:
                    self.current_combo_results.append(result) 

            current_average = self.average_cards_per_current_combo
            current_count = len(self.current_combo_ids) - 1
            new_average = (current_average * current_count + len(info["required_cards"])) / (current_count + 1)
            self.average_cards_per_current_combo = new_average

        current_average = self.average_cards_per_all_combo
        current_count = len(self.current_combo_ids) + len(self.combos_missing_another_card_ids) + len(self.combos_missing_this_card_ids) - 1
        new_average = (current_average * current_count + len(info["required_cards"]) + len(info["missing_cards"])) / (current_count + 1)
        self.average_cards_per_all_combo = new_average

    def print_statistics(self, print_func=print):
        missing_tag = " - Missing" if self.is_missing else ""
        print_func(f"CardName: {self.name}{missing_tag}")
        if not self.is_missing:
            print_func(f"CurrentCombos: {len(self.current_combo_ids)}")
            print_func(f"AverageCardCountPerCurrentCombo: {self.average_cards_per_current_combo}")
            print_func(f"Results:")
            for result in self.current_combo_results:
                print_func(f" - {result}")
        
        print_func(f"AverageComboCardCountAll: {self.average_cards_per_all_combo}")
        print_func(f"CombosMissingThisCard: {len(self.combos_missing_this_card_ids)}")
        print_func(f"Results:")
        for result in self.combos_missing_this_card_results:
            print_func(f" - {result}")

        print_func(f"CombosMissingAnotherCard: {len(self.combos_missing_another_card_ids)}")
        print_func(f"Results:")
        for result in self.combos_missing_another_card_results:
            print_func(f" - {result}")



def parse_card_data(combos, card_data:dict[str, CardEntry] = None):
    if card_data is None:
        card_data = dict[str, CardEntry]()

    for i, combo in enumerate(combos):
        for card in combo["required_cards"]:
            if card not in card_data.keys():
                card_data[card] = CardEntry(card, False)
            card_data[card].add_combo_info(i, combo)
        for card in combo["missing_cards"]:
            if card not in card_data.keys():
                card_data[card] = CardEntry(card, True)
            card_data[card].add_combo_info(i, combo)

    return card_data

def print_statistics(card_data: list[CardEntry], print_func=print):
    for card in card_data:
        card.print_statistics(print_func=print_func)


def print_card_combo(combo, print_func=print):
    summary = ", ".join(combo["required_cards"] + combo["missing_cards"]).strip()
    print_func(f"{summary}:")
    print_func("prerequisites")
    for prerequisite in combo["prerequisites"]:
        print_func(f" - {prerequisite}")

    print_func("steps:")
    for step in combo["steps"]:
        print_func(f" - {step}")

    print_func("results:")
    for result in combo["results"]:
        print_func(f" - {result}")

def print_card_combos(card:CardEntry, combos, print_func=print):
    current_combos = [combo for combo in combos if not any(combo["missing_cards"])]
    potential_combos = [combo for combo in combos if any(combo["missing_cards"])]

    print_func(f"{card.name}:")
    print_func("Current Combos:")
    for combo_id in card.current_combo_ids:
        combo = current_combos[combo_id]
        print_card_combo(combo, print_func=print_func)

    print_func("Combos missing this card:")
    for combo_id in card.combos_missing_this_card_ids:
        combo = potential_combos[combo_id]
        print_card_combo(combo, print_func=print_func)

    print_func("Combos missing another card:")
    for combo_id in card.combos_missing_another_card_ids:
        combo = potential_combos[combo_id]
        print_card_combo(combo, print_func=print_func)

def combo_is_desired(combo, antidecklist, desired_colours):
    if combo["colors"] != desired_colours:
        return False
    if any(card in combo["required_cards"] for card in antidecklist):
        return False
    if any(card in combo["missing_cards"] for card in antidecklist):
        return False
    
    return True

def remove_undesired_combos(combos, desired_colours, antidecklist):
    return [combo for combo in combos if combo_is_desired(combo, antidecklist, desired_colours)]


def print_combos_by_effect(combos, print_func=print):
    combos_by_result = dict()

    for combo in combos:
        summary = ", ".join(combo["required_cards"] + combo["missing_cards"]).strip()
        for result in combo["results"]:    
            if combos_by_result.get(result) is None:
                combos_by_result[result] = []
            
            result_combos:list = combos_by_result[result]

            if result_combos.count(result) == 0:
                result_combos.append(summary)

    for result in combos_by_result.keys():
        print_func(f"{result}:")
        for combo in combos_by_result[result]:
            print_func(combo)

def generate_adjacency_list(combos):
    adjacency_list = dict()
    for combo in combos:
        required_cards = combo["required_cards"]
        for required_card in required_cards:
            if adjacency_list.get(required_card) is None:
                adjacency_list[required_card] = []
            missing_cards = [card for card in required_cards if card not in adjacency_list[required_card] and card != required_card]
            adjacency_list[required_card] = adjacency_list[required_card] + missing_cards

    return adjacency_list

def main():
    # Load combos
    with open(combos_filepath, "r") as f:
        combos_text = f.read()

    combos = json.loads(combos_text)

    # Select desired combos
    antidecklist = []
    try:
        with open(antidecklist_filepath, "r") as f:
            antidecklist = f.read().splitlines()
    except FileNotFoundError as e:
        pass

    desired_colours = "c"
    combos = remove_undesired_combos(combos, desired_colours, antidecklist)

    # Analyze combos for statistics
    combo_data = parse_card_data(combos)

    # Apply desired sorting conditions
    cards = list(combo_data.values())
    cards = sorted(cards, key=lambda card: len(card.combos_missing_another_card_ids), reverse=True)
    cards = sorted(cards, key=lambda card: len(card.combos_missing_this_card_ids), reverse=True)
    cards = sorted(cards, key=lambda card: len(card.current_combo_ids), reverse=True)

    # Save Results
    current_combos = [combo for combo in combos if len(combo["missing_cards"]) == 0]

    with open(card_summaries_filename, 'w') as f:
        print_func = partial(print, file=f)
        print_statistics(cards, print_func=print_func)

    with open(combos_by_effect_filepath, 'w') as f:
        print_func = partial(print, file=f)
        print_combos_by_effect(current_combos, print_func=print_func)

    adj = generate_adjacency_list(current_combos)

    with open(adjacency_list_filepath, 'w') as f:
        f.write(json.dumps(adj, indent=2))




if __name__ == "__main__":
    main()
