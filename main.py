import requests
from bs4 import BeautifulSoup

def vehicle(num: str):
    try:
        veh_num = num.upper()
        url = f"https://www.carinfo.app/rc-details/{veh_num}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        }

        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        details = {}

        # Number Plate
        number_plate = soup.find("div", class_="input_vehical_layout_numberPlateContainer__Ug78g")
        if number_plate:
            details["Number Plate"] = number_plate.find("p").text.strip()

        # Make & Model
        make_model = soup.find("div", class_="input_vehical_layout_vehicalDetails__MseIO")
        if make_model:
            details["Make & Model"] = make_model.find("p", class_="input_vehical_layout_vehicalModel__1ABTF").text.strip()

        # Owner Name
        owner = soup.find("div", class_="input_vehical_layout_ownerDetails__6IzJb")
        if owner:
            details["Owner Name"] = owner.find("p", class_="input_vehical_layout_ownerName__NHkpi").text.strip()

        # RTO Details
        rto_container = soup.find("div", class_="expand_component_detailListContainer__L1nXb")
        if rto_container:
            for item in rto_container.find_all("div", class_="expand_component_detailItem__V43eh"):
                key_tag = item.find("p", class_="expand_component_itemText__cbigB")
                value_tag = item.find("p", class_="expand_component_itemSubTitle__ElsYf")
                if key_tag and value_tag:
                    details[key_tag.text.strip()] = value_tag.text.strip()

        # Website
        if rto_container:
            website_tag = rto_container.find("a", href=True)
            if website_tag:
                details["Website"] = website_tag['href']

        # Format humanoid output
        output = f"🛵 RC Details for Vehicle: {details.get('Number Plate', 'Unknown')}\n"
        output += "──────────────────────────\n"
        output += f"🚗 Make & Model: {details.get('Make & Model', 'N/A')}\n"
        output += f"👤 Owner Name: {details.get('Owner Name', 'N/A')}\n\n"

        output += "🏢 RTO Information:\n"
        output += f"📌 Number: {details.get('Number', 'N/A')}\n"
        output += f"📌 Registered RTO: {details.get('Registered RTO', 'N/A')}\n"
        output += f"📌 State: {details.get('State', 'N/A')}\n"
        output += f"📞 Phone: {details.get('RTO Phone number', 'N/A')}\n"
        output += f"🌐 Website: {details.get('Website', 'N/A')}\n"
        output += "──────────────────────────\n"
        output += "✅ Data fetched successfully!"

        return output

    except requests.exceptions.RequestException:
        return "❌ Network error or unable to reach the RC details site. Please check your connection or try again later."
    except Exception as e:
        return f"❌ An error occurred while fetching the RC details: {e}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

