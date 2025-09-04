# MTG Combo Analysis

MTG Combo Analysis is a project made to support EDH deckbuidling.


## Description

This project takes results from [EDH Decklist Combo Finder](https://combo-finder.com/) and analyzes the output to display useful summaries and statistics.

### Visualization 
Combo results are visualized using a barnes hut network diagram with parameters listed below.
* __Node Mass:__ Cards with higher combo potential are found more central within the network.
*  __Edge Colour:__ Current combos will are displayed with blue connections and potential combos with grey.

## Getting Started

### Dependencies

* Python >= 3.10
* beautifulsoup4 >= 4.13.0
* selenium >= 4.31.0
* pyvis >= 0.3.2

### Executing program
#### Quick Instructions
* Navigate to the [UserInputtedFiles](UserInputtedFiles) directory and copy your decklist from any website such as [Moxfield](https://moxfield.com/) to [decklist.txt](UserInputtedFiles/decklist.txt)
* You can also add the names of any cards you wish to ignore to file [antidecklist.txt](UserInputtedFiles/antidecklist.txt)
* If you wish to display combos of only a certain colour combination add those colours to file [desiredColours.txt](UserInputtedFiles/desiredColours.txt)
* Navigate to the [Scripts](Scripts) directory
* Run [run.py](Scripts/run.py)
```
python run.py
```
#### Detailed Instructions
* If you wish to apply custom sorting conditions or just skip the early stages of the pipeline each script can be run independently assuming the previous stages have been run at least once.
* [WebScraper](Scripts/webscraper.py)
```
python webscraper.py
```
* [WebParser](Scripts/htmlparser.py)
```
python htmlparser.py
```
* [Analysis](Scripts/analysis.py)
```
python analysis.py
```
* [Visualization](Scripts/visualization.py)
```
python visualization.py
```

## Authors
[Oliver-Molina](https://github.com/Oliver-Molina)

## Acknowledgments
* Shout out [EDH Decklist Combo Finder](https://combo-finder.com/)