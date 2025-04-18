from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time


decklist_filename = "decklist.txt"
url = "https://combo-finder.com/"
output_filename = "webpage.html"

# Read decklist file
try:
    with open(decklist_filename, "r", encoding="utf-8") as file:
        decklist_text = file.read()
except FileNotFoundError as e:
    print(f"No decklist found, please save your decklist to {decklist_filename}")
    exit(-1)

# Setup Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

try:
    print(f"Navigating to {url}.")
    driver.get(url)

    print("Waiting for page to load")
    time.sleep(2)

    print("Sending decklist")
    textarea = driver.find_element(By.ID, "decklistInput")
    textarea.clear()
    textarea.send_keys(decklist_text)

    print("Waiting for server response.")
    time.sleep(7)

    print(f"Saving webpage response to {output_filename}.")
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html)

finally:
    driver.quit()
