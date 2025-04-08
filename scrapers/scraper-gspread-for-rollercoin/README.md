# Rollercoin Marketplace Scraper

<div align=center>
  <img src="https://github.com/user-attachments/assets/4affda23-38a1-4e9e-802f-f2fc4da74319" alt="Rollercoin logo" width="100">
  <p>This Python project is designed to scrape data from the Rollercoin marketplace, a free-to-play cryptocurrency mining simulation game. Rollercoin allows users to purchase virtual miners and earn passive cryptocurrency income. The game's marketplace features a vast selection of miners with varying stats and prices.</p>
</div>

### Problem
The sheer volume of available miners (more than 150,000) and their fluctuating market prices make it challenging to identify and track optimal investment opportunities.

### Solution
This project scrapes miner data from the Rollercoin marketplace by parsing the HTML content of the `marketplace-buy-items-list` element. The script then organizes and stores this data in a Google Sheet for further analysis. To ensure data integrity, the script checks for duplicate miners using the unique combination of their names and power statistics.

### Considerations
- **Authentication:** Due to the complexity of automating site authentication (which involves email verification codes), this project does not handle login procedures. Users are expected to manually log in and provide the marketplace HTML.
- **Data Storage**: The scraped data is stored in a Google Sheet, enabling users to perform custom analyses.

### Functionality

1. Google Sheets API: requires a credentials.json file for Google Sheets API access. Refer to this tutorial for setup:
   [![Automate Google Sheets With Python - Google Sheets API Tutorial](https://markdown-videos-api.jorgenkh.no/url?url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DzCEJurLGFRk)](https://www.youtube.com/watch?v=zCEJurLGFRk)
   <br>
2. Environment Variables: set SHEET_ID (https://docs.google.com/spreadsheets/d/SHEET_ID/edit) and WORKSHEET environment variables to specify the target Google Sheet and worksheet.
3. Dependencies: install required Python packages (gspread, beautifulsoup4, google-auth-httplib2, google-api-python-client, google-auth-oauthlib & python-dotenv) using
`pip install -r "requirements.txt"` and run with `py main.py`
4. HTML input: the script prompts for an HTML formatted text in the console. The user must log in to the site, navigate to the marketplace URL ([rollercoin.com/marketplace](http://rollercoin.com/marketplace)), inspect the site and search for the `marketplace-buy-items-list` element, copy and paste the HTML into the console and press enter.
5. Data Output: the script creates a structured table in the Google Sheet with essential miner data, facilitating informed trading decisions. The program also prints to the console the modifications it makes to the spreadsheet (e.g., `New entry added: ...`)

### Future Enhancements

- Implement real-time market data updates.
- Develop a user-friendly interface for data visualization.
- Explore strategies for automated trading based on market analysis.
