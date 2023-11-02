import requests
import json
from selenium.webdriver.common.by import By
import time
import undetected_chromedriver as uc

options = uc.ChromeOptions()
# options.add_argument('--headless=new')
options.headless = False
driver = uc.Chrome(use_subprocess=True, options=options)
driver.maximize_window()

driver.get("https://www.turkanime.co/")
time.sleep(3)
cl = driver.get_cookies()
print(cl)
cookies_dict = {}
for c in cl:
    cookies_dict[c['name']] = c['value']

url = "https://www.turkanime.co/"

payload = {}
headers = {
    'Host': 'www.turkanime.co',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Cookie': '; '.join([f"{name}={value}" for name, value in cookies_dict.items()])  # Include cookies in the header
}

response = requests.get(url, headers=headers, data=payload)

print(response)

driver.quit()

# [{'domain': '.turkanime.co', 'expiry': 1730466363, 'httpOnly': True, 'name': 'cf_clearance', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'LDKGZu6lT35sgzj.jmWjuW.YQI8DNiaL6dXPpI9.aAA-1698930362-0-1-e037d2aa.2dedb22f.b3ac77b0-0.2.1698930362'}, {'domain': '.turkanime.co', 'expiry': 1733490362, 'httpOnly': False, 'name': '_ga', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GA1.1.1438311793.1698930363'}, {'domain': '.turkanime.co', 'expiry': 1733490362, 'httpOnly': False, 'name': '_ga_X5VBMNE3D1', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GS1.1.1698930362.1.0.1698930362.60.0.0'}, {'domain': 'www.turkanime.co', 'httpOnly': True, 'name': 'PHPSESSID', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': 'd25uh8q8pr9v7t240mubli4hv3'}]