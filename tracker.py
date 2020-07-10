import requests
from bs4 import BeautifulSoup
import smtplib
import csv
import datetime
import os

PERCENTAGE_FACTOR = 100
DEFAULT_FALLEN_PRICE_FACTOR = 0.95
DEFAULT_RISEN_PRICE_FACTOR = 1.05
DEFAULT_RANGE_PERCENT = 5.0
SMTP_PORT = 587

STOCKS_CLIPBOARD_PATH      = r'Insert your stocks clipboard file path here'
STOCKS_CLIPBOARD_TEMP_PATH = r'Insert your stocks clipboard temporary file path here'
EMAILS_INFO_FILE_PATH      = r'Insert your notifying email accounts file path here'

stocks_readable_file = open(STOCKS_CLIPBOARD_PATH, 'r')
stocks_reader = csv.DictReader(stocks_readable_file)

stocks_writable_file = open(STOCKS_CLIPBOARD_TEMP_PATH, 'w', newline='')
fieldnames = ['Stock', 'Range (%)', 'Buying', 'Current', '% Change', 'Timestamp']
stocks_writer = csv.DictWriter(stocks_writable_file, fieldnames)
stocks_writer.writeheader()

emails_file = open(EMAILS_INFO_FILE_PATH, 'r')
emails_reader = csv.DictReader(emails_file)

receiving_emails = []
for row in emails_reader:
    if row['Sending'] != '':
        sending_email = row['Sending']
    if row['Password'] != '':
        password = row['Password']
    if row['Receiving'] != '':
        receiving_emails.append(row['Receiving'])
    else:
        break
emails_file.close()


# Returns the URL of a stock on Yahoo! Finance based on the specified symbol
def get_stock_url(stock):
    stock_url = 'https://finance.yahoo.com/quote/' + stock + '?p=' + stock + '&.tsrc=fin-srch'
    return stock_url


# Returns the price of a stock from Yahoo! Finance based on the specified stock URL
def get_stock_current_price(stock_url):
    page = requests.get(stock_url)
    page.raise_for_status()
    soup = BeautifulSoup(page.content, 'html.parser')

    stock_current_price_tag = soup.find('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span')
    stock_current_price = stock_current_price_tag.text.replace(',', '')
    return stock_current_price


# Sends an email to a user-defined email address if any stock on the clipboard fell or rose over a certain range
def send_email_notification(stock, stock_url, stock_buy_price, stock_current_price, stock_percent_change, email_type):
    smtp = smtplib.SMTP('smtp.gmail.com', SMTP_PORT)
    smtp.ehlo()
    smtp.starttls()

    smtp.login(sending_email, password)

    if email_type == 'fallen':
        subject = 'Stock Price Fall: ' + stock
        body = stock + ' fell ' + str(stock_percent_change) + '%' + ' below your buying price.' + '\n\n' + \
            '-------------------------------------' + '\n' + \
            'Buying price: ' + ' $' + str(stock_buy_price) + '\n' + \
            'Current price: ' + '$' + str(stock_current_price) + '\n' + \
            '-------------------------------------' + '\n\n' + \
            'View the stock: ' + '\n' + stock_url

        message = f'Subject: {subject}\n{body}'

        smtp.sendmail(sending_email, receiving_emails, message)
        smtp.quit()
    elif email_type == 'risen':
        subject = 'Stock Price Rise: ' + stock
        body = stock + ' rose ' + str(stock_percent_change) + '%' + ' above your buying price.' + '\n\n' + \
            '-------------------------------------' + '\n' + \
            'Buying price: ' + ' $' + str(stock_buy_price) + '\n' + \
            'Current price: ' + '$' + str(stock_current_price) + '\n' + \
            '-------------------------------------' + '\n\n' + \
            'View the stock: ' + '\n' + stock_url

        message = f'Subject: {subject}\n{body}'

        smtp.sendmail(sending_email, receiving_emails, message)
        smtp.quit()


# Updates a specific row from the stocks clipboard
def update_row(stock, range_percent, stock_buy_price, stock_current_price, stock_percent_change, sent_email, is_buy_price_empty):
    if sent_email:
        stocks_writer.writerow({'Stock': stock, 'Range (%)': str(range_percent) + '%', 'Buying': '$' + str(stock_buy_price),
            'Current': '$' + str(stock_current_price), '% Change': str(stock_percent_change) + '%',
            'Timestamp': str(datetime.datetime.now())[5:10].replace('0', '').replace('-', '|') + str(datetime.datetime.now())[10:16]})
    elif sent_email is False and is_buy_price_empty is False:
        stocks_writer.writerow({'Stock': stock, 'Range (%)': str(range_percent) + '%', 'Buying': '$' + str(stock_buy_price),
             'Current': '$' + str(stock_current_price), '% Change': str(stock_percent_change) + '%'})
    else:
        stocks_writer.writerow({'Stock': stock, 'Range (%)': str(range_percent) + '%', 'Buying': str(stock_buy_price),
             'Current': '$' + str(stock_current_price), '% Change': stock_percent_change})


# Tracks stocks from a CSV file defined by the user and sends emails if a stock on the clipboard fell or rose over a certain range
def track_stocks():
    for row in stocks_reader:
        stock = str(row['Stock']).upper()

        if row['Range (%)'] == '' or row['Range (%)'] == 'N/A':
            range_percent = DEFAULT_RANGE_PERCENT
            fallen_price_factor = DEFAULT_FALLEN_PRICE_FACTOR
            risen_price_factor  = DEFAULT_RISEN_PRICE_FACTOR
        else:
            range_percent = float(str(row['Range (%)']).rstrip('%'))
            fallen_price_factor = 1 - (range_percent / PERCENTAGE_FACTOR)
            risen_price_factor  = 1 + (range_percent / PERCENTAGE_FACTOR)

        if row['Buying'] == '' or row['Buying'] == 'N/A':
            is_buy_price_empty = True
            stock_buy_price = 'N/A'
        else:
            is_buy_price_empty = False
            stock_buy_price = float(str(row['Buying'].replace(',', '')).lstrip('$'))
            if stock_buy_price >= 1000:
                before, sep, after = str(stock_buy_price).partition('.')
                stock_buy_price = int(before)

        stock_url = get_stock_url(stock)

        stock_current_price = float(str(get_stock_current_price(stock_url)).replace(',', ''))
        if stock_current_price >= 1000:
            before, sep, after = str(stock_current_price).partition('.')
            stock_current_price = int(before)

        if is_buy_price_empty:
            stock_percent_change = 'N/A'
        else:
            stock_percent_change = PERCENTAGE_FACTOR * ((stock_current_price - stock_buy_price) / stock_buy_price)
            if stock_percent_change >= 0:
                stock_percent_change = float(str(stock_percent_change)[:4])
            else:
                stock_percent_change = float(str(stock_percent_change)[:5])

        if is_buy_price_empty is False and stock_current_price < (fallen_price_factor * stock_buy_price):
            send_email_notification(stock, stock_url, stock_buy_price, stock_current_price, stock_percent_change, 'fallen')
            sent_email = True
            print('Email sent: ' + stock + ' fell below ' + str(range_percent) + '% of your buying price.')
        elif is_buy_price_empty is False and stock_current_price > (risen_price_factor * stock_buy_price):
            send_email_notification(stock, stock_url, stock_buy_price, stock_current_price, stock_percent_change, 'risen')
            sent_email = True
            print('Email sent: ' + stock + ' rose above ' + str(range_percent) + '% of your buying price.')
        else:
            sent_email = False

        update_row(stock, range_percent, stock_buy_price, stock_current_price, stock_percent_change, sent_email, is_buy_price_empty)

    stocks_readable_file.close()
    stocks_writable_file.close()

    os.replace(STOCKS_CLIPBOARD_TEMP_PATH, STOCKS_CLIPBOARD_PATH)
