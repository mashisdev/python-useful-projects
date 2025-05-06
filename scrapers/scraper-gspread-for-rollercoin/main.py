import gspread
from google.oauth2.service_account import Credentials
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()
SHEET_ID = os.getenv("SHEET_ID")
WORKSHEET = os.getenv("WORKSHEET")


def convert_power(power_str):
    """Converts power from Gh/s, Th/s, or Ph/s to a numerical value."""

    power_str = power_str.replace(",", "")  # Remove commas for large numbers
    if "Gh/s" in power_str:
        value = float(power_str.replace(" Gh/s", ""))
        return value
    elif "Th/s" in power_str:
        value = float(power_str.replace(" Th/s", "")) * 1000
        return value
    elif "Ph/s" in power_str:
        value = float(power_str.replace(" Ph/s", "")) * 1000000
        return value
    else:
        return 0  # Return 0 if no unit is found


def extract_html_data(html_content):
    # Extracts specific data from all marketplace-buy-item-card elements.

    soup = BeautifulSoup(html_content, "html.parser")
    item_cards = soup.find_all("a", class_="marketplace-buy-item-card")
    results = []

    for card in item_cards:
        try:
            price_str = card.find("p", class_="item-price").text.strip()
            item_price = price_str.replace(" RLT", "")  # Remove RLT from price
            power_str = card.find("span", class_="item-addition-power").text.strip()
            item_addition_power = convert_power(power_str)
            item_addition_bonus = card.find(
                "span", class_="item-addition-bonus"
            ).text.strip()
            item_title_str = card.find("p", class_="item-title")
            rarity = (
                item_title_str.find("span").text.strip()
                if item_title_str.find("span")
                else ""
            )
            item_title = item_title_str.text.replace(rarity, "").strip()

            results.append(
                {
                    "item_title": item_title,
                    "rarity": rarity,
                    "item_addition_power": item_addition_power,
                    "item_addition_bonus": item_addition_bonus,
                    "item_price": item_price,
                }
            )
        except AttributeError:
            print("Elements not found within an item-card.")
            continue
        except Exception as e:
            print(f"Error within an item-card: {e}")
            continue

    return results


def update_google_sheet(data):
    # Updates or adds data to a Google Sheets spreadsheet.
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    client = gspread.authorize(creds)

    # Connect to Spreadsheet & Worksheet
    try:
        sheet = client.open_by_key(SHEET_ID)
        worksheet = sheet.worksheet(WORKSHEET)
    except gspread.SpreadsheetNotFound:
        print("Spreadsheet not found. Verify the name.")
        return
    except gspread.WorksheetNotFound:
        print("Worksheet not found within the spreadsheet.")
        return

    # Get existing data
    sheet_data = worksheet.get_all_values()
    existing_items = []
    for i, row in enumerate(sheet_data[1:]):  # Use enumerate to get index
        existing_items.append(
            {
                "item_title": row[0].strip(),
                "item_addition_power": (
                    float(row[2]) if row[2] else 0
                ),  # Convert to number
                "row_index": i + 2,  # Adjust index for header and 0-based indexing
            }
        )

    # Add header row if it doesn't exist
    if not sheet_data or not sheet_data[0]:
        worksheet.append_row(["Miner", "Rarity", "Power", "% Bonus", "Price"])

    for item in data:
        item_title = item["item_title"].strip()  # Remove spaces
        item_power = item["item_addition_power"]

        found = False
        for existing_item in existing_items:
            if (
                item_title == existing_item["item_title"]
                and item_power == existing_item["item_addition_power"]
            ):
                # Update existing price
                worksheet.update_cell(
                    existing_item["row_index"], 5, item["item_price"]
                )  # Use the row_index directly
                print(
                    f"Price updated for {item_title} ({item_power}): {item['item_price']}"
                )
                found = True
                break

        if not found:
            # Add new entry
            new_row = [
                item["item_title"],
                item["rarity"],
                item["item_addition_power"],
                item["item_addition_bonus"],
                item["item_price"],
            ]
            worksheet.append_row(new_row)
            print(f"New entry added: {item_title} ({item_power})")


if __name__ == "__main__":
    print("Please enter the HTML content (from marketplace-buy-items-list):")
    html_content = input()

    try:
        data = extract_html_data(html_content)
        update_google_sheet(data)
        print("\nOperation completed.")
    except Exception as e:
        print(f"General error: {e}")
