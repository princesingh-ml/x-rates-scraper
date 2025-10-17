from bs4 import BeautifulSoup
import requests

currency = input("Currency: ")
date = input("Date (YYYY-MM-DD): ")
url = f"https://www.x-rates.com/historical/?from={currency}&amount=1&date={date}"
response = requests.get(url)
x_rate_webpage = response.text

soup = BeautifulSoup(x_rate_webpage, "html.parser")

table = soup.find(name= "table", class_ = "tablesorter ratesTable")

if table:
    rows = table.find_all("tr")
    for row in rows:
        col = [td.get_text(strip=True) for td in row.find_all("td")]
        if col:
            print(col)
else:
    print("No table found.")