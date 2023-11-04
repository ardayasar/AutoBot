import time
import requests
import undetected_chromedriver as uc

url = "https://www.turkanime.co/"
# cf_clearence = "jHovKfcDmZaCkJs19oPyk6IaXf45MGMLzjF3pnzr2i0-1698930985-0-1-5333897d.d646b197.432d69d-250.2.1698930985"
# PHPSESSID = "8qbstno7ocuqvofchqbcm0it1m"


def create_headers(cf_clearence, PHPSESSID):
  headers = {
    'host': 'www.turkanime.co',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'accept-language': 'tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3',
    'accept-encoding': 'gzip, deflate, br',
    'connection': 'keep-alive',
    'cookie': f'cf_clearance={cf_clearence}; PHPSESSID={PHPSESSID}',
    'upgrade-insecure-requests': '1',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'x-postman-captr': '9409557'
  }

  return headers


def create_payload():
  return {}


def getCookies(driver):
  try:
    cf_clearance = driver.get_cookie('cf_clearance')['value']
    PHPSESSID = driver.get_cookie('PHPSESSID')['value']
    return [cf_clearance, PHPSESSID]
  except:
    return [None, None]


options = uc.ChromeOptions()
# options.add_argument('--headless=new')
options.headless = False
driver = uc.Chrome(use_subprocess=True, options=options)
driver.maximize_window()

driver.get(url)
time.sleep(2)

[cf_clearence, PHPSESSID] = getCookies(driver)

response = requests.request("GET", url, headers=create_headers(cf_clearence, PHPSESSID), data=create_payload())
print(response.text)
