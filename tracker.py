import requests
from bs4 import BeautifulSoup
import smtplib

NAME = "name"
BUY_PRICE = "buy price"
# - Personal clipboard in which you can edit.
# - Any changes will be reflected accordingly in the program
# - Email notifications will be sent for the newly added stock
stocks_clipboard = \
    {
        1: {NAME: 'AAPL', BUY_PRICE: 351.76},
        2: {NAME: 'AMZN', BUY_PRICE: 2653.98},
        3: {NAME: 'BA'  , BUY_PRICE: 160.54},
        4: {NAME: 'FB'  , BUY_PRICE: 235.53},
        5: {NAME: 'GOOG', BUY_PRICE: 1435.96},
        6: {NAME: 'INTC', BUY_PRICE: 60.49},
        7: {NAME: 'MSFT', BUY_PRICE: 194.24},
        8: {NAME: 'NVDA', BUY_PRICE: 369.44},
        9: {NAME: 'TSLA', BUY_PRICE: 1000.00},
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


# Checks if any stock on the clipboard fell below 5% of the buying price
def check_price_fall():
    fallen_price_factor = 0.95

    for i in range(len(stocks_clipboard)):
        stock = stocks_clipboard[i + 1].get(NAME)
        stock_url = get_stock_url(stock)
        stock_buy_price = float(str(stocks_clipboard[i + 1].get(BUY_PRICE)).replace(',', ''))
        current_stock_price = float(get_current_stock_price(stock_url).replace(',', ''))

        if current_stock_price < (fallen_price_factor * stock_buy_price):
            print('Email sent: ' + stock + ' fell below 5% of your buying price.')
            send_fallen_price_email(stock, stock_buy_price)


# Checks if any stock on the clipboard rose above 5% of the buying price
def check_price_rise():
    risen_price_factor = 1.05

    for i in range(len(stocks_clipboard)):
        stock = stocks_clipboard[i + 1].get(NAME)
        stock_url = get_stock_url(stock)
        stock_buy_price = float(str(stocks_clipboard[i + 1].get(BUY_PRICE)).replace(',', ''))
        current_stock_price = float(get_current_stock_price(stock_url).replace(',', ''))

        if current_stock_price > (risen_price_factor * stock_buy_price):
            print('Email sent: ' + stock + ' rose above 5% of your buying price.')
            send_risen_price_email(stock, stock_buy_price)


# Sends an email to a specified email address if any stock on the clipboard fell below 5% of the buying price
# --------------------------------------------------------------------------
# - Requires Google 2-Step Verification to be enabled
# - The password is a generated Google App Password for one's Gmail account
# --------------------------------------------------------------------------
def send_fallen_price_email(stock, stock_buy_price):
    stock_url = get_stock_url(stock)
    stock_current_price = float(get_current_stock_price(stock_url))

    percentage_factor = 100

    stock_fallen_amount = percentage_factor * ((stock_buy_price - stock_current_price) / stock_buy_price)
    sliced_stock_fallen_amount = str(stock_fallen_amount)[:4]
    stock_price_fallen_percentage = -float(sliced_stock_fallen_amount)

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()

    sending_email = 'someone@example.com'
    receiving_emails = ['someoneelse1@example.com', 'someoneelse2@example.com', 'someoneelse3@example.com']
    password = 'Insert your password here'
    smtp.login(sending_email, password)

    subject = 'Stock Price Fall: ' + stock
    body = stock + ' fell ' + str(stock_price_fallen_percentage) + '%' + ' below your buying price.' + '\n\n' + \
           '-------------------------------------' + '\n' + \
           'Buying price: ' + ' $' + str(stock_buy_price) + '\n' + \
           'Current price: ' + '$' + str(stock_current_price) + '\n' + \
           '-------------------------------------' + '\n\n' + \
           'View the stock: ' + '\n' + stock_url

    message = f'Subject: {subject}\n{body}'

    smtp.sendmail(sending_email, receiving_emails, message)
    smtp.quit()


# Sends an email to specified email addresses if any stock on the clipboard rose above 5% of the buying price
# --------------------------------------------------------------------------
# - Requires Google 2-Step Verification to be enabled
# - The password is a generated Google App Password for one's Gmail account
# --------------------------------------------------------------------------
def send_risen_price_email(stock, stock_buy_price):
    stock_url = get_stock_url(stock)
    stock_current_price = float(get_current_stock_price(stock_url))

    percentage_factor = 100

    stock_risen_amount = percentage_factor * ((stock_current_price - stock_buy_price) / stock_buy_price)
    stock_sliced_risen_amount = str(stock_risen_amount)[:4]
    stock_price_rise_percentage = float(stock_sliced_risen_amount)

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()

    sending_email = 'someone@example.com'
    receiving_emails = ['someoneelse1@example.com', 'someoneelse2@example.com', 'someoneelse3@example.com']
    password = 'Insert your password here'
    smtp.login(sending_email, password)

    subject = 'Stock Price Rise: ' + stock
    body = stock + ' rose ' + str(stock_price_rise_percentage) + '%' + ' above your buying price.' + '\n\n' + \
           '-------------------------------------' + '\n' + \
           'Buying price: ' + ' $' + str(stock_buy_price) + '\n' + \
           'Current price: ' + '$' + str(stock_current_price) + '\n' + \
           '-------------------------------------' + '\n\n' + \
           'View the stock: ' + '\n' + stock_url

    message = f'Subject: {subject}\n{body}'

    smtp.sendmail(sending_email, receiving_emails, message)
    smtp.quit()


# - Tracks all stocks on the clipboard
# - Sends email notifications if the current price changed by 5% or more from the buying price.
def track_stocks():
    check_price_fall()
    check_price_rise()
