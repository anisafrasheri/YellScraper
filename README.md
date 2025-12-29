# Quick Guide: How to Avoid Yell Detecting You as a Bot

Follow these steps every time before you run the scraper.

---

## 1. Close all Chrome windows
Make sure Chrome is completely shut down — every tab, every window.

---

## 2. Start Chrome using the special command
This starts Chrome in a way that Selenium can use without looking like a bot.

**Windows**
```bash
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenium_profile"
```

**Mac**
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/tmp/selenium_profile"
```
**Linux**
```bash
google-chrome --remote-debugging-port=9222 --user-data-dir="/tmp/selenium_profile"
```
This will open a new Chrome window — keep it open.

## 3. Use Yell normally for 20–30 seconds
In this Chrome window:

Go to yell.com

Search for anything (e.g., “Private Dentistry”)

Scroll down slowly

Press “Show number” on 1 or 2 businesses

This makes Yell see you as a real person.

## 4. Make sure there’s no captcha
If Yell shows a captcha, solve it.

If everything loads normally, you’re good.

## 5. Do NOT close this Chrome window
Leave it open. Selenium will use this exact window when scraping.

## 6. Now run your Python script
Everything should run smoothly.

Keep in mind: the Selenium script is fragile because of Yell’s bot detection. If it doesn’t work properly, simply run it again.

# THANK YOU!
