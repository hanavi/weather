#!/home/james/.local/python/python3.7/bin/python
# coding: utf-8

import re
import requests
from bs4 import BeautifulSoup as bs
import os
import tempfile
import sys

# Gets rid of InsecureRequestWarning that crops up due to BCBSAL Proxy
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

image_url = re.compile(".*url\(([^)]+)\).*")
site_url = "https://weather.com/weather/today/l/USMA0062:1:US"

req = requests.get(site_url,verify=False)
soup = bs(req.content, features='lxml')

# divs = soup.find("div", attrs={'id': 'ts-0'})
divs = soup.find_all("div")
for div in divs:
    url_match = image_url.match(str(div.get('style')))
    if url_match:
        break
        # print(url_match.group(1))

# sys.exit()

img_url = "https:" + url_match.group(1)
dl = requests.get(img_url, verify=False)

# with open('image.jpg', 'wb') as fd:
#     fd.write(dl.content)

if os.name == "nt":
    tmpfile = tempfile.mkstemp(suffix='.jpg', prefix=r"\temp\weather_")
else:
    tmpfile = tempfile.mkstemp(suffix='.jpg', prefix="/tmp/weather_")

fd = tmpfile[0]
fname = tmpfile[1]

os.write(fd, dl.content)
os.close(fd)

if os.name == "nt":
    os.system(f"{fname}")
else:
    os.system(f"feh {fname}")


