from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def vehicle(num: str):
    try:
        veh_num = num.upper()
        url = f"https://www.carinfo.app/rc-details/{veh_num}"

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=60000)
            page.wait_for_timeout(5000)
            html = page.content()
            browser.close()

        soup = BeautifulSoup(html, "html.parser")
        details = {}

        def grab(css):
            tag = soup.select_one(css)
            return tag.text.strip() if tag else "N/A"

        details["Number Plate"] = grab("div[class*='numberPlateContainer'] p")
        details["Make & Model"] = grab("p[class*='vehicalModel']")
        details["Owner Name"] = grab("p[class*='ownerName']")

        for item in soup.select("div[class*='detailItem']"):
            key = item.select_one("p[class*='itemText']")
            val = item.select_one("p[class*='itemSubTitle']")
            if key and val:
                details[key.text.strip()] = val.text.strip()

        output = f"""🛵 RC Details for Vehicle: {details['Number Plate']}
──────────────────────────
🚗 Make & Model: {details['Make & Model']}
👤 Owner Name: {details['Owner Name']}

🏢 RTO Information:
📌 Number: {details.get('Number','N/A')}
📌 Registered RTO: {details.get('Registered RTO','N/A')}
📌 State: {details.get('State','N/A')}
📞 Phone: {details.get('RTO Phone number','N/A')}
──────────────────────────
✅ Data fetched successfully!
"""
        return output

    except Exception as e:
        return f"❌ Error: {e}"