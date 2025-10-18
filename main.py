from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import pandas as pd

currency = input("Currency: ")
start_date = input("Start Date (YYYY-MM-DD): ")
end_date = input("End Date (YYYY-MM-DD): ")

start = datetime.strptime(start_date, "%Y-%m-%d")
end = datetime.strptime(end_date, "%Y-%m-%d")

data = []
all_currency = set()

current = start
while current <= end:
    str_date = current.strftime("%Y-%m-%d")

    url = f"https://www.x-rates.com/historical/?from={currency}&amount=1&date={str_date}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")


    table = soup.find(name= "table", class_ = "tablesorter ratesTable")
    if table:
        day_data = {"Date": str_date}
        rows = table.find_all("tr")
        for row in rows:
            if row.name != "tr":
                continue
            col = [td.get_text(strip=True) for td in row.find_all("td")]
            if len(col) == 3:
                day_data[col[0] + f" 1.00 {currency}"] = float(col[1])
                day_data[col[0] + f" inv. 1.00 {currency}"] = float(col[2])
                all_currency.add(col[0] + f" 1.00 {currency}")
                all_currency.add(col[0] + f" inv. 1.00 {currency}")
        data.append(day_data)
    else:
        print("No table found.")
    
    current+= timedelta(days=1)

# pandas
data_frame = pd.DataFrame(data)
filename = f"xrates_{currency}_{start_date}_to_{end_date}.csv"
data_frame.to_csv(filename, index=False)

print(f"Data saved in {filename}.")