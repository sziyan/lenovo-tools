import requests
from bs4 import BeautifulSoup
import re
import json
from openpyxl import load_workbook
from datetime import datetime
import time
from telegram import Bot
import config

serial = 'PF2KM0VZ'   
url = 'https://pcsupport.lenovo.com/sg/en/products/laptops-and-netbooks/thinkpad-l-series-laptops/thinkpad-l14-type-20u1-20u2/20u2/20u2cto1ww/{}/warranty'.format(serial)

# r = requests.get(url)
# data = r.text
# soup = BeautifulSoup(data, 'html.parser')
# script = soup.find_all('script')[22].string
# x = re.findall('var ds_warranties = window.ds_warranties \|\| ({[\w\W]+});', script)[0]
# js = json.loads(x)
# warranty = js.get('BaseUpmaWarranties')[0].get('End')
# print(warranty)

# r = requests.get(url)
# data = r.text
# soup = BeautifulSoup(data, 'html.parser')
# script = soup.find_all('script')
# for sr in script:
#     try:
#         if 'var ds_warranties' in sr.string:
#             warranty_string = sr.string
#             ds_warranties = re.findall('window.ds_warranties \|\| ({[\w\W]+});', warranty_string)[0]
#             js = json.loads(ds_warranties)
#             warranty = js.get('BaseUpmaWarranties')[0].get('End')
#             print(warranty)
#     except:
#         pass


def get_warranty(url):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')
    script = soup.find_all('script')
    for sr in script:
        try:
            if 'var ds_warranties' in sr.string:
                warranty_string = sr.string
                ds_warranties = re.findall('window.ds_warranties \|\| ({[\w\W]+});', warranty_string)[0]
                js = json.loads(ds_warranties)
                warranty = js.get('BaseUpmaWarranties')[0].get('End')
                break
        except:
            warranty = 'Unable to find warranty date'
    return warranty

myw = get_warranty(url)
print(myw)