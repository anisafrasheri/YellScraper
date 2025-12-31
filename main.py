import time
from apify_client import ApifyClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

LIMIT = 500  # total unique results needed

SEARCHES = [
    ("Private Dentists", "UK"),
    ("Cosmetic Dentistry", "United Kingdom"),
    ("Dental Implants", "United Kingdom")  # NEW FALLBACK CATEGORY
]

# Initialize Apify client
client = ApifyClient()
# dataset_id = client.dataset("default").id  # default dataset


def scrape_search(driver, keyword, location, remaining_limit, seen_names):
    page = 1
    results = []

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

        cards = driver.find_elements(By.XPATH, '//article[contains(@class,"businessCapsule")]')

        if not cards:
            print("⚠ No more results for this category.")
            break

        for card in cards:
            if len(results) >= remaining_limit:
                break

            try:
                name = card.find_element(By.XPATH, ".//h2").text.strip()
            except:
                continue

            if name.lower() in seen_names:
                continue

            try:
                website = card.find_element(
                    By.XPATH, './/a[@data-test="localBusiness--website"]'
                ).get_attribute("href")
            except:
                website = ""

            phone = ""
            try:
                btn = card.find_element(
                    By.XPATH,
                    './/button[contains(@data-test,"localBusiness--phoneCollapsed")]'
                )
                driver.execute_script("arguments[0].click();", btn)
                time.sleep(0.4)
                phone_elem = card.find_element(
                    By.XPATH,
                    './/span[contains(@class,"business--telephoneNumber")]'
                )
                phone = phone_elem.text.strip()
            except:
                phone = ""

            # -------------------------
            # Push to Apify dataset
            # -------------------------
            record = {"name": name, "phone": phone, "website": website}
           # client.dataset(dataset_id).push_items([record])

            results.append(record)
            seen_names.add(name.lower())
            print(f"[{len(results)}/{remaining_limit}] ✔ {name} | {phone} | {website}")

        page += 1

    return results


def scrape_yell(limit):
    options = Options()
    options.debugger_address = "127.0.0.1:9222"
    driver = webdriver.Chrome(options=options)
    print("Connected to verified Chrome browser…")

    seen_names = set()
    total_results = []

    for keyword, location in SEARCHES:
        if len(total_results) >= limit:
            break
        print(f"\n===============================")
        print(f"🔍 Starting category: {keyword}")
        print(f"===============================")

        remaining = limit - len(total_results)
        results = scrape_search(driver, keyword, location, remaining, seen_names)
        total_results.extend(results)
        print(f"➡ Finished '{keyword}', total so far: {len(total_results)}")

    driver.quit()
    print(f"\n✅ DONE — Scraped {len(total_results)} unique entries")


if __name__ == "__main__":
    scrape_yell(LIMIT)
