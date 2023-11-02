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

# Prepare cookies for requests
cookies_dict = {}
for c in cl:
    cookies_dict[c['name']] = c['value']
    if 'domain' in c:
        cookies_dict[c['name']] += f"; Domain={c['domain']}"
    if 'path' in c:
        cookies_dict[c['name']] += f"; Path={c['path']}"
    if 'expires' in c:
        cookies_dict[c['name']] += f"; Expires={c['expires']}"
    if 'httpOnly' in c and c['httpOnly']:
        cookies_dict[c['name']] += "; HttpOnly"
    if 'secure' in c and c['secure']:
        cookies_dict[c['name']] += "; Secure"
    if 'sameSite' in c:
        cookies_dict[c['name']] += f"; SameSite={c['sameSite']}"

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
