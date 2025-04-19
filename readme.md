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
* Navigate to the [UserInputtedFiles](UserInputtedFiles) directory and copy your decklist from any website such as [Moxfield](https://moxfield.com/) to [decklist.txt](UserInputtedFiles/decklist.txt)
* You can also add the names of any cards you wish to ignore to file [antidecklist.txt](UserInputtedFiles/antidecklist.txt)
* Navigate to the [Scripts](Scripts) directory
* Run [webscraper.py](Scripts/webscraper.py)
```
python webscraper.py
```
* Parse the webpage response using [htmlparser.py](Scripts/htmlparser.py)
```
python htmlparser.py
```
* Edit [analysis.py](Scripts/analysis.py) if you wish to apply custom sorting conditions
* Run [analysis.py](Scripts/analysis.py) and view the results.
```
python analysis.py > summary.txt
```

## Authors
[Oliver-Molina](https://github.com/Oliver-Molina)

## Acknowledgments
* Shout out [EDH Decklist Combo Finder](https://combo-finder.com/)