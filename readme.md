# MTG Combo Analysis

MTG Combo Analysis is a project made to support EDH deckbuidling.


## Description

This project takes results from [EDH Decklist Combo Finder](https://combo-finder.com/) and analyzes the output to display useful summaries and statistics.

## Getting Started

### Dependencies

* Python >= 3.10
* beautifulsoup4 >= 4.13.0
* selenium >= 4.31.0

### Executing program

* Copy your decklist from any website such as [Moxfield](https://moxfield.com/) and save it to decklist.txt
* Run webscraper.py
```
python webscraper.py
```
* Parse the webpage response using htmlparser.py
```
python htmlparser.py
```
* Edit analysis.py if you wish to apply custom sorting conditions
* Analyze the results using analysis.py saving results if you please.
```
python analysis.py > summary.txt
```

## Authors
[Oliver-Molina](https://github.com/Oliver-Molina)

## Acknowledgments
* Shout out [EDH Decklist Combo Finder](https://combo-finder.com/)