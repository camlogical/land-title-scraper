from flask import Flask, jsonify, request
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

def scrape_land_data_playwright(land_number: str) -> dict:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://miniapp.mlmupc.gov.kh", timeout=15000)
        page.wait_for_selector('input[name="landNum"]', timeout=10000)
        page.fill('input[name="landNum"]', land_number)

        time.sleep(30)  # Manual CAPTCHA solving time

        page.click('button[type="submit"]')
        page.wait_for_timeout(5000)

        html = page.content()
        browser.close()

        soup = BeautifulSoup(html, 'html.parser')

        if "មិនមានព័ត៌មានអំពីក្បាលដីនេះទេ" in html:
            return {"status": "not_found", "message": "មិនមានព័ត៌មានអំពីក្បាលដីនេះទេ."}

        serial_info = soup.select_one('#serail_info')
        location = soup.find('span', string=lambda x: x and 'ភូមិ' in x)
        updated_system = soup.find('p', string=lambda x: x and 'ធ្វើបច្ចុប្បន្នភាព' in x)

        table = soup.find("table", class_="table table-bordered")
        owner_info = {}

        if table:
            for row in table.find_all("tr"):
                cols = row.find_all("td")
                if len(cols) == 2:
                    key = cols[0].get_text(strip=True)
                    value = cols[1].get_text(strip=True)
                    owner_info[key] = value

        return {
            "status": "found",
            "serial_info": serial_info.get_text(strip=True) if serial_info else "",
            "location": location.get_text(strip=True) if location else "",
            "updated_system": updated_system.get_text(strip=True) if updated_system else "",
            "owner_info": owner_info
        }

@app.route('/scrape', methods=['GET'])
def scrape():
    land_number = request.args.get('land_number')
    if not land_number:
        return jsonify({"status": "error", "message": "Land number is required."}), 400

    result = scrape_land_data_playwright(land_number)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
