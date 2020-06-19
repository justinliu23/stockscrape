import requests
from bs4 import BeautifulSoup

NAME = "name"
BUY_PRICE = "buy price"
# - Personal stocks clipboard in which you can edit
# - Any changes will be reflected accordingly in the program
stocks_clipboard = \
    {
        1: {NAME: 'AAPL', BUY_PRICE: 331.76},
        2: {NAME: 'AMZN', BUY_PRICE: 2600.98},
        3: {NAME: 'BA'  , BUY_PRICE: 190.54},
        4: {NAME: 'FB'  , BUY_PRICE: 232.53},
        5: {NAME: 'GOOG', BUY_PRICE: 1435.96},
        6: {NAME: 'INTC', BUY_PRICE: 60.49},
        7: {NAME: 'MSFT', BUY_PRICE: 194.24},
        8: {NAME: 'NVDA', BUY_PRICE: 369.44},
        9: {NAME: 'TSLA', BUY_PRICE: 970.00},
        10: {NAME: 'AMD', BUY_PRICE: 55.00},
        11: {NAME: 'UAL', BUY_PRICE: 40.00},
        12: {NAME: 'NUGT', BUY_PRICE: 65.38},
        13: {NAME: 'XOM', BUY_PRICE: 40.00},
        14: {NAME: 'PLUG', BUY_PRICE: 5.00},
    }


# Returns the URL of a stock on Yahoo! Finance based on any stock symbol
def get_stock_url(stock_symbol):
    stock = stock_symbol.upper()
    stock_url = 'https://finance.yahoo.com/quote/' + stock + '?p=' + stock + '&.tsrc=fin-srch'

    return stock_url


# Returns the price of a stock based on any stock URL for Yahoo! Finance
def get_current_stock_price(stock_url):
    page = requests.get(stock_url)
    page.raise_for_status()
    soup = BeautifulSoup(page.content, 'html.parser')

    current_stock_price = soup.find('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text

    return current_stock_price


# Prints the price of a stock based on any stock URL for Yahoo! Finance
def display_stock_price(stock_url):
    before, sep, after = stock_url.partition('?')
    oldBefore = before
    before, sep, after = oldBefore.partition('quote/')
    stock = after

    current_stock_price = get_current_stock_price(stock_url)
    print('Current Price of ' + stock + ': ' + '$' + current_stock_price)


# Allows the user to pick any stock from the clipboard to view the price of
def pick_stocks():
    print('--------')
    for i in range(len(stocks_clipboard)):
        stock = stocks_clipboard[i + 1].get(NAME)
        spaces = ' ' * (5 - len(stock))
        print(stock + spaces + '[' + str((i + 1)) + ']')
        print('--------')

    choice = input()

    if (int(choice) <= len(stocks_clipboard) and int(choice) > 0):
        for i in range(len(stocks_clipboard)):
            if int(choice) == i + 1:
                stock = stocks_clipboard[i + 1].get(NAME)
                stock_url = get_stock_url(stock)
                display_stock_price(stock_url)
    else:
        print('Invalid input.')



# Prints the price of any stock based on the stock symbol
def enter_stock():
    print('Stock Name:')
    stock = input().upper()
    stock_url = get_stock_url(stock)

    display_stock_price(stock_url)


# - Allows the user to pick any stock from the clipboard to view the price of
# - Prints the price of any stock based on the stock symbol
def view_stocks():
    print('\n****************************')
    print('| Pick Stocks          [1] |')
    print('| ------------------------ |')
    print('| Enter a Stock Symbol [2] |')
    print('****************************')

    choice = input()

    if int(choice) == 1:
        pick_stocks()
    elif int(choice) == 2:
        enter_stock()
    else:
        print('Invalid input.')


# Calls view_stocks() in a loop controlled by the user
def main():
    continue_viewing = 'y';
    while continue_viewing.casefold() == 'y':
        view_stocks()
        print('\nView another stock? [Y/N]')
        continue_viewing = input()


if __name__ == "__main__":
    main()
