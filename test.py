import cfscrape

scraper = cfscrape.create_scraper()  # returns a CloudflareScraper instance

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7',
    'Accept': '*/*',
    'Accept-Language': 'tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br'
}

response = scraper.get("https://turkanime.co", headers=headers)
# response = scraper.get("https://turkanime.co")
print(response.text)