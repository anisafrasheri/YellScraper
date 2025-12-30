# 🟡 Yell Business Scraper (Apify Actor)

Scrape business listings from **Yell.com** using custom keywords and location.  
The Actor collects **business name, phone number, and website** and stores the results in an Apify dataset.

This scraper uses **Selenium with a real Chrome session** to reduce bot detection.

---

## 🚀 What this Actor does

- 🔍 Searches Yell.com by **keyword(s)** and **location**
- 🏢 Extracts:
  - Business name
  - Phone number
  - Website (if available)
- 🧹 Removes duplicate businesses automatically
- 📦 Saves results to the **default Apify dataset**
- 📄 Exportable to CSV, JSON, Excel

---

## 📥 Actor Input

The Actor accepts the following input parameters:

```json
{
  "keywords": ["Plumbers", "Electricians"],
  "location": "United Kingdom",
  "limit": 100
}
