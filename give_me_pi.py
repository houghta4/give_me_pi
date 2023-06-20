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

DEBUG = True
if not DEBUG:
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG, format='[%(asctime)s] \t %(levelname)s \t %(message)s', datefmt='%a %m %d %H:%M:%S %Y')
else:
    logging.basicConfig(filename='give_me_pi.log', encoding='utf-8', level=logging.INFO, format='[%(asctime)s] \t %(levelname)s \t %(message)s', datefmt='%a %m %d %H:%M:%S %Y')


# Loading .env with secrets
load_dotenv()

# Set the interval time
INTERVAL = 60

sent = []

# Twilio credentials and client set up
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
twilio_number = os.environ['TWILIO_NUMBER']
my_number = os.environ['PERSONAL_NUMBER']

client = Client(account_sid, auth_token)


# Text personal number from twilio number
def text(avail_msg):
    #Text message to be sent
    if DEBUG:
        return 
    msg = client.messages.create(
        body=f'{avail_msg}',
        from_=twilio_number,
        to=my_number
    )
    logging.info(f'SMS sent. SID: {msg.sid}')
        

# Call personal number from twilio number
def phone_call(avail_msg):
    if DEBUG:
        return 
    call = client.calls.create(
        twiml=f"<Response><Say>{avail_msg}</Say></Response>",
        from_=twilio_number,
        to=my_number
    )
    logging.info(f'Call sent. SID: {call.sid}')


# Scraping the product name
def get_name(doc):

    # Finding h1 with product name
    name_div = doc.find("h1", attrs={"class": ["products_name", 'productView-title', 'product-detail__title', 'product_name']})
    if not name_div:
        name_div = doc.find("h1", {"id": 'MainContent_ProdName'})

    # Extracting text from product name h1
    product_name = name_div.text if name_div else ''

    return product_name


# Checking if the item is available
def item_availability(doc, domain, kit=None):
    # Looking for the "Add to Cart" button, which is unavailable if item is out of stock
    if domain == 'adafruit' or domain == 'chicagodist':
        return doc.find(string='Add to Cart')
    elif domain == 'pishop':
        return doc.find(string='IN STOCK')
    elif domain == 'vilros':
        return not doc.find(string="Notify Me When Available")
    elif domain == 'canakit':
        if not kit:
            kit = 'Pi 4 8GB Starter Kit - 32GB'
        return not doc.find('b', string=kit).parent.find_next_siblings("td")[1].find(string='Pre-Orders Sold Out')
    else:
        return ''


def send_message(doc, url):
    # Getting product name from the get_name function
    product_name = get_name(doc)
    domain = tld.extract(url).domain

    # Checking whether item_availability function confirms that the item is in stock
    if domain not in sent and item_availability(doc, domain):
        logging.critical(f'Product found at {url}')
        
        avail_msg= f'{product_name} is in Stock on {domain.title()}\'s website!'

        text(avail_msg)
        

        # Wait before calling
        time.sleep(5)

        phone_call(avail_msg)
        
        sent.append(domain)



# links
# https://www.pishop.us/product/raspberry-pi-4-model-b-8gb/
# https://www.adafruit.com/product/4564
# https://vilros.com/products/raspberry-pi-4-model-b-8gb-ram?src=raspberrypi
# https://chicagodist.com/products/raspberry-pi-4-model-b-8gb?src=raspberrypi
# https://www.canakit.com/raspberry-pi-4-starter-kit.html

# URL = 'https://www.adafruit.com/product/4564' # out of stock
# URL = 'https://www.adafruit.com/product/2830' # in stock

# URL = 'https://www.pishop.us/product/raspberry-pi-pico-w-with-pre-soldered-headers/' # in stock
# URL = 'https://www.pishop.us/product/raspberry-pi-4-model-b-8gb/' # out of stock


# URL = 'https://vilros.com/products/raspberry-pi-4-model-b-8gb-ram?src=raspberrypi' # out of stock
# URL = 'https://vilros.com/collections/raspberry-pi-boards/products/raspberry-pi-pico-wireless' # in stock

# URL = 'https://chicagodist.com/products/raspberry-pi-4-model-b-8gb?src=raspberrypi' # out of stock
# URL = 'https://chicagodist.com/products/0-1-36-pin-strip-right-angle-female-socket-header-5-pack' # in stock

# URL = 'https://www.canakit.com/raspberry-pi-4-starter-kit.html'

urls = ['https://www.pishop.us/product/raspberry-pi-4-model-b-8gb/',
        'https://www.adafruit.com/product/4564',
        'https://vilros.com/products/raspberry-pi-4-model-b-8gb-ram?src=raspberrypi',
        'https://chicagodist.com/products/raspberry-pi-4-model-b-8gb?src=raspberrypi', 
        'https://www.canakit.com/raspberry-pi-4-starter-kit.html'
        ]

try:
    t = time.time()
    logging.info('-' * 22 + 'Starting process' + '-' * 22)
    logging.info(f'Checking availability of items at given urls every {INTERVAL} seconds.')
    
    # Main loop
    while True:
        delta_t = time.time()
        if delta_t - t > 300:
            t = delta_t
            logging.info(f'Monitoring product availability')

        for url in urls:

            # Parse page
            result = requests.get(url)
            doc = BeautifulSoup(result.text, "html.parser")
            
            if result.status_code == 200:
                send_message(doc, url)
            else:
                logging.error(result)
            
        time.sleep(INTERVAL)
except Exception as e:
    logging.exception(e)
finally:
    logging.info('-' * 23 + 'Ending process' + '-' * 23)
