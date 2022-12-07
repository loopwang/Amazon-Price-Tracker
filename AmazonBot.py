# 1) Check price of item
# 2) Get notified via Email when price changes

from unicodedata import name
import requests
from lxml import html
import smtplib
import ssl
import getpass




def fetch_price():
    url = 'https://www.amazon.ca/Google-Whole-Wi-Fi-System-Version/dp/B01MDJ0HVG/ref=sr_1_1?crid=DU4JRCQEYL1&keywords=google%2Bhome%2Bmesh&qid=1670392003&sprefix=google%2Bhome%2Bmesh%2Caps%2C165&sr=8-1&th=1'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Accept-Encoding': None
    }

    r = requests.get(url, headers=headers)
    tree = html.fromstring(r.content)
    price = tree.xpath('//span[@class="a-price-whole"]/text()')[0]
    print('Current Price: $' +  price)
    return price

def fetch_name():
    url = 'https://www.amazon.ca/Google-Whole-Wi-Fi-System-Version/dp/B01MDJ0HVG/ref=sr_1_1?crid=DU4JRCQEYL1&keywords=google%2Bhome%2Bmesh&qid=1670392003&sprefix=google%2Bhome%2Bmesh%2Caps%2C165&sr=8-1&th=1'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Accept-Encoding': None
    }

    r = requests.get(url, headers=headers)
    tree = html.fromstring(r.content)
    name = tree.xpath('//span[@id="productTitle"]/text()')[0]
    return name

def send_email(price):
    smtp_server = "smtp-mail.outlook.com"
    port = 587 # For starttls
    sender_email = "pricetracker661@outlook.com"
    password = getpass.getpass()

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() 
        server.starttls(context=context)
        server.ehlo() 
        server.login(sender_email, password)

        subject = 'Price decreased'
        body = f'{name} is now {price} dollars'
        link = 'https://www.amazon.ca/Google-Wi-Fi-System-single-point/dp/B073ZMDMKH/ref=sr_1_2?crid=33MT8Z3XUR89Z&keywords=google+home+router&qid=1665002130&qu=eyJxc2MiOiIyLjg0IiwicXNhIjoiMi4wNSIsInFzcCI6IjEuNTAifQ%3D%3D&sprefix=google+home+roue%2Caps%2C136&sr=8-2'
        msg = f"Subject: {subject} \n\n {body} \n\n {link}"
        server.sendmail(sender_email, sender_email, msg)
    # TODO: Send email here
    except Exception as e:
    # Print any error messages to stdout
        print(e)
    finally:
        server.quit()


if __name__ == "__main__":
    price = fetch_price()
    name = fetch_name()
    if float(price) < 150:
        send_email(price)
    else:
        print("Still expensive!") 