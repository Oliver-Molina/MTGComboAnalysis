from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from os import path

# External URLs
url = "https://combo-finder.com/"

# User Inputted Files
user_directory = path.join("..", "UserInputtedFiles")
decklist_filename = path.join(user_directory, "decklist.txt")

# Output Files
output_directory = path.join("..", "WebScraperArtifacts")
webpage_copy_filepath = path.join(output_directory, "webpage.html")


def main():
    # Read decklist file
    try:
        with open(decklist_filename, "r", encoding="utf-8") as file:
            decklist_text = file.read()
    except FileNotFoundError as e:
        print(f"No decklist found, please save your decklist to {decklist_filename}")
        return -1

    # Setup Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    try:
        print(f"Navigating to {url}.")
        driver.get(url)

        print("Waiting for page to load.")
        time.sleep(2)

        print("Sending decklist.")
        textarea = driver.find_element(By.ID, "decklistInput")
        textarea.clear()
        textarea.send_keys(decklist_text)

        
        wait_duration = 7
        while wait_duration > 0:
            wait_duration -= 1
            print(f"Waiting for server response. {wait_duration}", end="\n" if wait_duration==0 else "\r")
            time.sleep(1)


        print(f"Saving webpage response to {webpage_copy_filepath}.")
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        with open(webpage_copy_filepath, "w", encoding="utf-8") as f:
            f.write(html)

    finally:
        driver.quit()

    return 0

if __name__ == "__main__":
    rtn = main()
    exit(rtn)
