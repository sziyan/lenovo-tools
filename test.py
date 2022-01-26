import requests
from bs4 import BeautifulSoup
import re
import json
from openpyxl import load_workbook
from datetime import datetime
import time
from telegram import Bot
import config
import warranty
import urllib
import urllib3
import requests



# serial = 'R90QH3GL'   
# model = 'thinkpad l380'

serial = 'NXVD4SG005724190607600'   
model = 'acer'
brand, url = warranty.get_url(serial=serial, model=model)
#warranty_date = warranty.get_warranty(url)
warranty_date = warranty.get_acer_warranty(serial)

print(warranty_date)

# serial = 'NXEG8SG00K1480014C0201'
# #serial = 'sdjfskjfsd'
# model = 'acer'
# url = 'http://support.acer.com.sg/support/checkwarrantyresults.asp'

# formData = {
#     '__VIEWSTATE': 'wEPDwUJNDA4Mzc4NTUxZGQazEtBaHJpnK06W95ZaNAwjHPGdC3C2rmOWwCv9qkuBw==',
#     'pserialno': serial
# }

# r = requests.post(url, data = formData)
# data = r.text
# soup = BeautifulSoup(data, 'html.parser')
# row = soup.find_all('td')

# for i in range(len(row)):
#     try:
#         if row[i].strong.text == 'Onsite Expiry:':
#             unformatted_warranty_date = row[i+1].text
#             unformatted = datetime.strptime(unformatted_warranty_date, '%d %B, %Y')
#             warranty = unformatted.strftime('%d %b %Y')
#             break
#     except:
#         warranty = 'Error'

# print(warranty)




#url = 'https://pcsupport.lenovo.com/sg/en/products/laptops-and-netbooks/thinkpad-l-series-laptops/thinkpad-l14-type-20u1-20u2/20u2/20u2cto1ww/{}/warranty'.format(serial)


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


# def get_warranty(url):
#     r = requests.get(url)
#     data = r.text
#     soup = BeautifulSoup(data, 'html.parser')
#     script = soup.find_all('script')
#     for sr in script:
#         try:
#             if 'var ds_warranties' in sr.string:
#                 warranty_string = sr.string
#                 ds_warranties = re.findall('window.ds_warranties \|\| ({[\w\W]+});', warranty_string)[0]
#                 js = json.loads(ds_warranties)
#                 warranty = js.get('BaseUpmaWarranties')[0].get('End')
#                 break
#         except:
#             warranty = 'Unable to find warranty date'
#     return warranty
