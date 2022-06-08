#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import time
import sys

#--------- Constants -------------------#
SPACES = 15
URL = "https://coinmarketcap.com/"
GREEN = "\033[0;32m"
RED = "\033[0;31m"
WHITE = "\033[0;37m"
UP_ARROW = u'\u2191'
DOWN_ARROW = u'\u2193'
CLEAR_TERMINAL = "\033[H\033[J"
#---------------------------------------#

#---------- Functions --------------------#
def get_crypto_name(element):
    title = element.find("p", class_="sc-1eb5slv-0 iworPT")
    if(title is not None):
        return title.text.strip()
    return "N/A"

def get_crypto_price(element):
    price = element.find("div", class_="sc-131di3y-0 cLgOOr")
    if(price is not None):
        price_real = price.find("span")
        return price_real.text.strip()
    return "N/A"

def add_stuff_to_string(stuff):
    for x in range(len(stuff), SPACES):
        stuff += " "
    return stuff


def get_change(element, iteration):
    positive_change = 1

    # Search for positive change
    change = element.find("span", class_="sc-15yy2pl-0 kAXKAX")
    if(change is None):
        positive_change = 0
        # Search for negative change
        change = element.find("span", class_="sc-15yy2pl-0 hzgCfk")

    if(change is None):
        return add_stuff_to_string("N/A")

    seven_day_change = ""
    if(iteration == 0):
        parent = change.parent
        sibling = parent.find_next_sibling()
        seven_day_change += get_change(sibling, 1)

    #format the string before returning
    change = change.text.strip()
    change = change + UP_ARROW if positive_change else change + DOWN_ARROW
    change = add_stuff_to_string(change)

    #color code the output
    change = GREEN + change + WHITE if positive_change else RED + change + WHITE

    change += seven_day_change
    
    return change

def get_market_cap(element):
    market_cap = element.find("span", class_="sc-1ow4cwt-0 iosgXe")
    if(market_cap is None):
        return "N/A"
    return market_cap.text.strip()


def get_formatted_output(crypto_element):
    crypto_string = ""

    name = get_crypto_name(crypto_element)
    if(name == "N/A"):
        return "No element found"
    crypto_string += add_stuff_to_string(name)

    price = get_crypto_price(crypto_element)
    crypto_string += add_stuff_to_string(price)

    crypto_string += get_change(crypto_element, 0)
    
    crypto_string += get_market_cap(crypto_element)
    return crypto_string

def print_first_string():
    first_string = add_stuff_to_string("Name")
    first_string += add_stuff_to_string("Price")
    first_string += add_stuff_to_string("24h")
    first_string += add_stuff_to_string("7 days")
    first_string += "Market Cap"
    print(first_string)

def main():
    while(1):
        page = requests.get(URL)
        parser = BeautifulSoup(page.content, "html.parser")

        table_of_content = parser.find("table", class_="h7vnx2-2 czTsgW cmc-table") 
        body = table_of_content.find("tbody")
        body_tr = body.find_all("tr")

        # clear terminal before beginning
        print(CLEAR_TERMINAL)
        print_first_string()

        for tr in body_tr:
            element = get_formatted_output(tr)
            if(element == "No element found"):
                break
            print(element)
        
        print()
        print("Prices are updated every minute, press CTRL + C to quit program ")
        time.sleep(60)

#-----------------------------------------#

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(CLEAR_TERMINAL)
        quit()