import requests

url = "https://www.turkanime.co/"

payload={}
headers = {
  'host': 'www.turkanime.co',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
  'accept-language': 'tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3',
  'accept-encoding': 'gzip, deflate, br',
  'connection': 'keep-alive',
  'cookie': 'cf_clearance=yKorcgPQ_yY7Sh30F.y4x1po51EmZZww1rPqK0gHDmk-1698920457-0-1-5333897d.d646b197.432d69d-250.2.1698920457; PHPSESSID=8qbstno7ocuqvofchqbcm0it1m',
  'upgrade-insecure-requests': '1',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'none',
  'sec-fetch-user': '?1',
  'x-postman-captr': '9535798'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
