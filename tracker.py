import requests
from bs4 import BeautifulSoup
import smtplib
import csv

fallen_price_factor = 0.95
risen_price_factor = 1.05
percentage_factor = 100

stocks_clipboard_file = open('INSERT YOUR FILE PATH FOR THE STOCKS CLIPBOARD HERE', 'r')
stocks_clipboard_reader = csv.reader(stocks_clipboard_file)

emails_file = open('INSERT YOUR FILE PATH FOR THE NOTIFYING EMAIL ACCOUNTS HERE', 'r')
emails_reader = csv.reader(emails_file)

receiving_emails = []

next(emails_reader)

for row in emails_reader:
    if row[0] != '':
        sending_email = row[0]
    if row[1] != '':
        password = row[1]
    if row[2] != '':
        receiving_emails.append(row[2])
    else:
        break

emails_file.close()


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

    current_stock_price_tag = soup.find('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span')
    current_stock_price = current_stock_price_tag.text.replace(',', '')
    return current_stock_price


# Checks if any stock on Stocks Clipboard.csv fell or rose over 5% of the buying price
def check_price_change():
    next(stocks_clipboard_reader)

    for row in stocks_clipboard_reader:
        stock = row[0]
        stock_url = get_stock_url(stock)
        stock_buy_price = float(str(row[1].replace(',', '')))
        current_stock_price = float(get_current_stock_price(stock_url))

        if current_stock_price < (fallen_price_factor * stock_buy_price):
            send_email_notification(stock, stock_buy_price, 'fallen')
            print('Email sent: ' + stock + ' fell below 5% of your buying price.')

        elif current_stock_price > (risen_price_factor * stock_buy_price):
            send_email_notification(stock, stock_buy_price, 'risen')
            print('Email sent: ' + stock + ' rose above 5% of your buying price.')

    stocks_clipboard_file.close()


# Sends an email to a specified email address if any stock on the clipboard fell below 5% of the buying price
# --------------------------------------------------------------------------
# - Requires Google 2-Step Verification to be enabled
# - The password is a generated Google App Password for one's Gmail account
# --------------------------------------------------------------------------
def send_email_notification(stock, stock_buy_price, email_type):
    stock_url = get_stock_url(stock)
    stock_current_price = float(get_current_stock_price(stock_url))

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()

    smtp.login(sending_email, password)

    if email_type == 'fallen':
        stock_fallen_amount = percentage_factor * ((stock_buy_price - stock_current_price) / stock_buy_price)
        sliced_stock_fallen_amount = str(stock_fallen_amount)[:4]
        stock_price_fallen_percentage = -float(sliced_stock_fallen_amount)

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

    elif email_type == 'risen':
        stock_risen_amount = percentage_factor * ((stock_current_price - stock_buy_price) / stock_buy_price)
        stock_sliced_risen_amount = str(stock_risen_amount)[:4]
        stock_price_rise_percentage = float(stock_sliced_risen_amount)

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


# - Tracks stocks based on a CSV file defined by the user
# - Sends email notifications if a stock's current price changed by 5% or more from the buying price
def track_stocks():
    check_price_change()
