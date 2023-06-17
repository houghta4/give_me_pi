# Log to file
import logging
# Beautiful Soup for scraping
from bs4 import BeautifulSoup
import requests
# Twilio to send text message and a call
from twilio.rest import Client
import os
# .env for Twilio credentials
from dotenv import load_dotenv
# Time for delay
import time
# Extract domain name so twilio is happy
import tldextract as tld
# Keep track of last found product time to prevent spam call/text
import datetime
from datetime import timedelta  

logging.basicConfig(filename='give_me_pi.log', encoding='utf-8', level=logging.INFO)


# Loading .env with secrets
load_dotenv()

# Set the interval time
INTERVAL = 30


# Twilio credentials and client set up
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
twilio_number = os.environ['TWILIO_NUMBER']
my_number = os.environ['PERSONAL_NUMBER']

client = Client(account_sid, auth_token)


def log_info(msg):
    t = time.ctime(time.time())
    logging.info(f'[{t}] \t {msg}')

def log_error(msg):
    t = time.ctime(time.time())
    logging.error(f'[{t}] \t {msg}')


# Text personal number from twilio number
def text(avail_msg):
    #Text message to be sent
    return client.messages.create(
        body=f'{avail_msg}',
        from_=twilio_number,
        to=my_number
    )
        

# Call personal number from twilio number
def phone_call(avail_msg):
    return client.calls.create(
        twiml=f"<Response><Say>{avail_msg}</Say></Response>",
        from_=twilio_number,
        to=my_number
    )

# Scraping the product name
def get_name(doc):

    # Finding h1 with product name
    name_div = doc.find("h1", {"class": "products_name"})

    # Extracting text from product name h1
    product_name = name_div.text

    return product_name


# Checking if the item is available
def item_availability(doc):
    # Looking for the "Add to Cart" button, which is unavailable if item is out of stock
    return doc.find(string='Add to cart')


def send_message(doc, url):
    # Getting product name from the get_name function
    product_name = get_name(doc)

    # Checking whether item_availability function confirms that the item is in stock
    if item_availability(doc):
        log_info(f'Product found at {url}')
        domain = tld.extract(url).domain
        avail_msg= f'{product_name} is in Stock on {domain.title()}\'s website!'

        msg = text(avail_msg)
        log_info(f'SMS sent. SID: {msg.sid}')

        # Wait before calling
        time.sleep(5)

        call = phone_call(avail_msg)
        log_info(f'Call sent. SID: {call.sid}')

        # For now, (with one url) end process
        exit()

    else: # out of stock
        log_info(f'Out of stock at {url}\n')

    


# Prompt user for an URL with the target product
# URL = input("Paste the URL of the target product from the Adafruit.com website: ")
URL = 'https://www.adafruit.com/product/4564'


try:
    log_info('-' * 22 + 'Starting process' + '-' * 22)
    log_info(f'Checking availability of items at given urls every {INTERVAL} seconds.\n')

    # Main loop
    while True:

        log_info(f'Checking {URL}')
        # Parse page
        result = requests.get(URL)
        doc = BeautifulSoup(result.text, "html.parser")
        
        if result.status_code == 200:
            log_info(result)
            send_message(doc, URL)
        else:
            log_error(result)
        
        time.sleep(INTERVAL)
except:
    log_info('-' * 23 + 'Ending process' + '-' * 23)