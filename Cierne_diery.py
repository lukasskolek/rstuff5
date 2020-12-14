import requests
import re
import time
from random import randint
import smtplib
from email.message import EmailMessage
from urllib.request import urlopen
import json
import os
from bs4 import BeautifulSoup as bs
#print ("done importing")
cache = []
time.sleep(randint(1,30))
if os.path.isfile('./cachefile.json'):
    with open('./cachefile.json') as fh:
        try:
            cache = json.load(fh)
        except json.decoder.JSONDecodeError:
            os.remove('./cachefile.json')
url = "https://eshop.ciernediery.sk/"
page = urlopen(url)
soup = bs((page.read()),features="lxml")


all = [x for x in set(filter(lambda x: 'product' in x,[x.get('href') for x in soup.find_all('a')]))]
new = [x for x in filter(lambda x: x not in cache, all)]
cache += new
grafiky = 'Tieto su nove: \n'
for x in new:
    grafiky += x + '\n'

with open('./cachefile.json','w') as fh:
    json.dump(cache,fh)

if new:
    msg = EmailMessage()
    msg.set_content(grafiky)
    msg['From'] = 'diery2020cierne@gmail.com'
    msg['Subject'] = 'CIERNE DIERY Whoop Whoop dali nove grafiky tak kupujeme!'
    fromaddr = 'diery2020cierne@gmail.com'
    toaddrs = 'luky.skolek@gmail.com', 'jurasluky@gmail.com', 'filip.alexander.uhlarik@gmail.com', 'kristina.lappyova@gmail.com'
    msg['To'] = ", ".join(toaddrs)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login('diery2020cierne@gmail.com', '3P6ciaUaLJiraKk')
    server.send_message(msg)
    server.quit()
    response = urlopen(url).read()
else:
    print('All has been seen')
