import requests
from bs4 import BeautifulSoup
import re
import json
from openpyxl import load_workbook
from datetime import datetime
import time
from telegram import Bot
import config

serial = 'R911JBN3'   
url = 'https://pcsupport.lenovo.com/sg/en/products/laptops-and-netbooks/thinkpad-l-series-laptops/thinkpad-l13-type-20r3-20r4/20r4/20r4s5ta00/{}/warranty'.format(serial)

r = requests.get(url)
data = r.text
soup = BeautifulSoup(data, 'html.parser')
script = soup.find_all('script')[21].string
x = re.findall('var ds_warranties = window.ds_warranties \|\| ({[\w\W]+});', script)[0]
js = json.loads(x)
warranty = js.get('BaseUpmaWarranties')[0].get('End')
print(warranty)