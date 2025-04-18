# This file is used to analyze a combo_data json and display useful statistics about your deck.
# Useful Informatiom
# Combo count
# How often each card appears in a combo
# Average number of cards in a combo involving a given card
# For potential cards, how many new combos could be added
# and the average number of cards in potential combos

import json

combos_filename = "combo_data.json"
card_data_filename = "card_data.json"

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
        new_average = (current_average * current_count + len(info["required_cards"])) / (current_count + 1)
        self.average_cards_per_all_combo = new_average

    def print_statistics(self):

        missing_tag = " - Missing" if self.is_missing else ""
        print(f"CardName: {self.name}{missing_tag}")
        if not self.is_missing:
            print(f"CurrentCombos: {len(self.current_combo_ids)}")
            print(f"AverageCardCountPerCurrentCombo: {self.average_cards_per_current_combo}")
            print(f"Results:")
            for result in self.current_combo_results:
                print(f" - {result}")
        
        print(f"AverageComboCardCountAll: {self.average_cards_per_all_combo}")
        print(f"CombosMissingThisCard: {len(self.combos_missing_this_card_ids)}")
        print(f"Results:")
        for result in self.combos_missing_this_card_results:
            print(f" - {result}")

        print(f"CombosMissingAnotherCard: {len(self.combos_missing_another_card_ids)}")
        print(f"Results:")
        for result in self.combos_missing_another_card_results:
            print(f" - {result}")



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

def print_statistics(card_data: list[CardEntry]):
    for card in card_data:
        card.print_statistics()


def print_card_combo(combo):
    summary = ", ".join(combo["required_cards"] + combo["missing_cards"]).strip()
    print(f"{summary}:")
    print("prerequisites")
    for prerequisite in combo["prerequisites"]:
        print(f" - {prerequisite}")

    print("steps:")
    for step in combo["steps"]:
        print(f" - {step}")

    print("results:")
    for result in combo["results"]:
        print(f" - {result}")

def print_card_combos(card:CardEntry, current_combos, potential_combos):
    print(f"{card.name}:")
    print("Current Combos:")
    for combo_id in card.current_combo_ids:
        combo = current_combos[combo_id]
        print_card_combo(combo)

    print("Combos missing this card:")
    for combo_id in card.combos_missing_this_card_ids:
        combo = potential_combos[combo_id]
        print_card_combo(combo)

    print("Combos missing another card:")
    for combo_id in card.combos_missing_another_card_ids:
        combo = potential_combos[combo_id]
        print_card_combo(combo)

def main():
    # Load combos
    with open(combos_filename, "r") as f:
            combos_text = f.read()

    combos = json.loads(combos_text)

    # Select desired combos
    current_combos = [combo for combo in combos["current"] if combo["colors"] == "c"]
    potential_combos = [combo for combo in combos["potential"] if combo["colors"] == "c"]

    # Analyze combos for statistics
    combo_data = parse_card_data(current_combos)
    combo_data = parse_card_data(potential_combos, combo_data)

    # Apply desired sorting conditions
    cards = list(combo_data.values())
    cards = sorted(cards, key=lambda card: len(card.combos_missing_another_card_ids), reverse=False)
    cards = sorted(cards, key=lambda card: len(card.current_combo_ids), reverse=False)
    cards = sorted(cards, key=lambda card: len(card.combos_missing_this_card_ids), reverse=True)
    # cards = sorted(cards, key=lambda card: card.is_missing, reverse=False)
    cards = [card for card in cards if card.is_missing == True]
    #cards = [card for card in cards if len(card.current_combo_ids) == 1]

    # Display Results
    print_statistics(cards)
    # for card in cards:
    #     print_card_combos(card, current_combos, potential_combos)
    #     print("")



if __name__ == "__main__":
    main()
