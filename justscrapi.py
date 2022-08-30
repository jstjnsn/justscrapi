from json import dumps

import requests
from bs4 import BeautifulSoup

user_ticker = str(
    input("Which ticker details do you want to get? (choose from IWDA, EMIM, VUSA): ")
)

URLS = {
    "iwda": "https://www.justetf.com/en/etf-profile.html?query=IE00B4L5Y983&groupField=index&from=search&isin=IE00B4L5Y983",
    "emim": "https://www.justetf.com/en/etf-profile.html?query=IE00BKM4GZ66&groupField=index&from=search&isin=IE00BKM4GZ66#overview",
    "vusa": "https://www.justetf.com/en/etf-profile.html?query=IE00B3XXRP09&groupField=index&from=search&isin=IE00B3XXRP09#overview",
}

page = requests.get(URLS.get(user_ticker.lower()))

soup = BeautifulSoup(page.content, "html.parser")

top_10_row = (
    soup.find("div", class_="constituents-top")
    .find_next_sibling("table")
    .find_all("tr")
)

holdings = []

for holding_row in top_10_row:
    holding_parts = holding_row.find_all("td")

    holdings.append(
        {
            "name": holding_parts[0].get_text(),
            "value": holding_parts[1].find("span").get_text(),
        }.copy()
    )

f = open("holdings-{}.json".format(user_ticker), "w")
f.write(dumps(holdings))
f.close()

print("Ticker details saved to {}!".format(f.name))
