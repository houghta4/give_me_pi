import unittest
import requests
from bs4 import BeautifulSoup
from give_me_pi import item_availability

class TestAvailabilityMethod(unittest.TestCase):
    """
    Note to self: these links will not always work as products will be available/sold out as time goes on. This is just to test initial setup
    """
    
    def test_canakit(self):
        url = 'https://www.canakit.com/raspberry-pi-4-starter-kit.html'
        result = requests.get(url)
        doc = BeautifulSoup(result.text, "html.parser")
        self.assertTrue(item_availability(doc, 'canakit', 'Pi 4 2GB Starter Kit - 32GB'), msg=f'{url} should be available.')

    def test_canakit_sold_out(self):
        url = 'https://www.canakit.com/raspberry-pi-4-starter-kit.html'
        result = requests.get(url)
        doc = BeautifulSoup(result.text, "html.parser")
        self.assertFalse(item_availability(doc, 'canakit'), msg=f'{url} should NOT be available.')

    def test_vilros(self):
        url = 'https://vilros.com/collections/raspberry-pi-boards/products/raspberry-pi-pico-wireless'
        result = requests.get(url)
        doc = BeautifulSoup(result.text, "html.parser")
        self.assertTrue(item_availability(doc, 'vilros'), msg=f'{url} should be available.')

    def test_vilros_sold_out(self):
        url = 'https://vilros.com/products/raspberry-pi-4-model-b-8gb-ram?src=raspberrypi'
        result = requests.get(url)
        doc = BeautifulSoup(result.text, "html.parser")
        self.assertFalse(item_availability(doc, 'vilros'), msg=f'{url} should NOT be available.')


    def test_adafruit(self):
        url = 'https://www.adafruit.com/product/2830'
        result = requests.get(url)
        doc = BeautifulSoup(result.text, "html.parser")
        self.assertTrue(item_availability(doc, 'adafruit'), msg=f'{url} should be available.')

    def test_adafruit_sold_out(self):
        url = 'https://www.adafruit.com/product/4564'
        result = requests.get(url)
        doc = BeautifulSoup(result.text, "html.parser")
        self.assertFalse(item_availability(doc, 'adafruit'), msg=f'{url} should NOT be available.')

    def test_pishop(self):
        url = 'https://www.pishop.us/product/raspberry-pi-pico-w-with-pre-soldered-headers/'
        result = requests.get(url)
        doc = BeautifulSoup(result.text, "html.parser")
        self.assertTrue(item_availability(doc, 'pishop'), msg=f'{url} should be available.')

    def test_pishop_sold_out(self):
        url = 'https://www.pishop.us/product/raspberry-pi-4-model-b-8gb/'
        result = requests.get(url)
        doc = BeautifulSoup(result.text, "html.parser")
        self.assertFalse(item_availability(doc, 'pishop'), msg=f'{url} should NOT be available.')

    

if __name__ == '__main__':
    unittest.main()