import requests
from bs4 import BeautifulSoup

SPACES = 15
URL = "https://coinmarketcap.com/"
page = requests.get(URL)

parser = BeautifulSoup(page.content, "html.parser")
table_of_content = parser.find("table", class_="h7vnx2-2 czTsgW cmc-table") # ändra till att den hittar alla strängar som innehåller cmc-table

body = table_of_content.find("tbody")
body_tr = body.find_all("tr")

def get_crypto_name(element):
    title = element.find("p", class_="sc-1eb5slv-0 iworPT")
    if(title is not None):
        return title.text.strip()
    return "error"

def get_crypto_price(element):
    price = element.find("div", class_="sc-131di3y-0 cLgOOr")
    if(price is not None):
        price_real = price.find("span")
        return price_real.text.strip()
    return "error"

def add_stuff_to_string(stuff):
    for x in range(len(stuff), SPACES):
        stuff += " "
    return stuff


def get_24h_change(element, iteration):
    positive_change = 1
    change = element.find("span", class_="sc-15yy2pl-0 kAXKAX")
    if(change is None):
        positive_change = 0
        change = element.find("span", class_="sc-15yy2pl-0 hzgCfk")

    if(change is None):
        return add_stuff_to_string("N/A")

    other_change = ""
    if(iteration == 0):
        parent = change.parent
        sibling = parent.find_next_sibling()
        other_change += get_24h_change(sibling, 1)
        #kör funktionen igen

    #format the string before returning
    change = change.text.strip()
    change = add_stuff_to_string(change)

    #color code the output
    if(positive_change):
        change = "\033[0;32m" + change + "\033[0;37m"
    else:
        change = "\033[0;31m" + change + "\033[0;37m"

    if(len(other_change) > 0):
        change += other_change
    
    return change

def get_market_cap(element):
    market_cap = element.find("span", class_="sc-1ow4cwt-0 iosgXe")
    if(market_cap is None):
        return "error"
    return market_cap.text.strip()


def get_formatted_output(crypto_element):
    crypto_string = ""

    # get name
    name = get_crypto_name(crypto_element)
    if(name == "error"):
        return "error"
    crypto_string += add_stuff_to_string(name)
    # get price
    price = get_crypto_price(crypto_element)
    if(price == "error"):
        return "error"
    crypto_string += add_stuff_to_string(price)

    # get price difference 24h
    change = get_24h_change(crypto_element, 0)
    if(change == "error"):
        return "error"
    crypto_string += change
    
    market_cap = get_market_cap(crypto_element)
    if(market_cap == "error"):
        return "error"
    crypto_string += market_cap
    return crypto_string


first_string = add_stuff_to_string("Name")
first_string += add_stuff_to_string("Price")
first_string += add_stuff_to_string("24h")
first_string += add_stuff_to_string("7 days")
first_string += "Market Cap"
print(first_string)
for tr in body_tr:
    #title = tr.find("p", class_="sc-1eb5slv-0 iworPT")
    element = ""
    element = get_formatted_output(tr)
    if(element == "error"):
        break
    print(element)