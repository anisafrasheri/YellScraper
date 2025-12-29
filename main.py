import time
import csv
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Load Actor input from Apify environment variable
# In Apify, the input is available as JSON in ACTOR_INPUT
try:
    import os
    input_data = json.loads(os.environ.get("ACTOR_INPUT", "{}"))
except Exception:
    input_data = {}

# Default values if input not provided
SEARCHES = [(kw, input_data.get("location", "United Kingdom")) for kw in input_data.get("keywords", ["Plumbers", "Electricians"])]
LIMIT = input_data.get("limit", 100)

def scrape_search(driver, keyword, location, remaining_limit, seen_names, results):
    page = 1
    while len(results) < remaining_limit:
        url = (
            f"https://www.yell.com/ucs/UcsSearchAction.do?"
            f"keywords={keyword.replace(' ', '+')}&"
            f"location={location.replace(' ', '+')}&"
            f"pageNum={page}"
        )

        print(f"\n🔎 Loading page {page}: {keyword} in {location}")
        driver.get(url)
        time.sleep(2)

        # Get results on page
        cards = driver.find_elements(By.XPATH, '//article[contains(@class,"businessCapsule")]')
        if not cards:
            print("⚠ No more results for this category.")
            break

        print(f"📌 Found {len(cards)} business cards")

        for card in cards:
            if len(results) >= remaining_limit:
                break
            try:
                name = card.find_element(By.XPATH, ".//h2").text.strip()
            except:
                continue

            if name.lower() in seen_names:
                print(f"⏭ Skipping duplicate: {name}")
                continue

            try:
                website = card.find_element(By.XPATH, './/a[@data-test="localBusiness--website"]').get_attribute("href")
            except:
                website = ""

            phone = ""
            try:
                btn = card.find_element(By.XPATH, './/button[contains(@data-test,"localBusiness--phoneCollapsed")]')
                driver.execute_script("arguments[0].click();", btn)
                time.sleep(0.4)
                phone_elem = card.find_element(By.XPATH, './/span[contains(@class,"business--telephoneNumber")]')
                phone = phone_elem.text.strip()
            except:
                phone = ""

            results.append([name, phone, website])
            seen_names.add(name.lower())
            print(f"[{len(results)}/{remaining_limit}] ✔ {name} | {phone} | {website}")

        page += 1

def scrape_yell(limit):
    options = Options()
    options.debugger_address = "127.0.0.1:9222"
    driver = webdriver.Chrome(options=options)
    print("Connected to verified Chrome browser…")

    seen_names = set()
    results = []

    for keyword, location in SEARCHES:
        if len(results) >= limit:
            break
        print(f"\n===============================\n🔍 Starting category: {keyword}\n===============================")
        remaining = limit - len(results)
        scrape_search(driver, keyword, location, limit, seen_names, results)
        print(f"➡ Finished '{keyword}', total so far: {len(results)}")

    driver.quit()

    # Save results
    with open("yell_scraped.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Name", "Phone", "Website"])
        w.writerows(results)

    print(f"\n✅ DONE — Saved {len(results)} unique entries to yell_scraped.csv")

if __name__ == "__main__":
    scrape_yell(LIMIT)
