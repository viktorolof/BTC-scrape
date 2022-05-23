import requests
from bs4 import BeautifulSoup

URL = "https://coinmarketcap.com/"
page = requests.get(URL)

parser = BeautifulSoup(page.content, "html.parser")
table_of_content = parser.find("table", class_="h7vnx2-2 czTsgW cmc-table") # ändra till att den hittar alla strängar som innehåller cmc-table

#print(table_of_content)
body = table_of_content.find("tbody")
body_tr = body.find_all("tr")
#cryptos = body_tr.find_all("a", class_="cmc_link")

def get_formatted_output(crypto_element):
    return crypto_element


# print(name     price      change     etc)
for tr in body_tr:
    title = tr.find("p", class_="sc-1eb5slv-0 iworPT")
    price = tr.find("div", class_="sc-131di3y-0 cLgOOr")
    price_real = price.find("span")
    #introduce error checking in the loop (function)
    print(price_real.text.strip())


