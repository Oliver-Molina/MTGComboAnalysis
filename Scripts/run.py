from os import system


def main():
    commands = ["python webscraper.py",
                "python htmlparser.py",
                "python analysis.py",
                "python visualization.py",]
    
    rtn = system(" && ".join(commands))

if __name__ == "__main__":
    main()