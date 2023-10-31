import json
from selenium.webdriver.common.by import By
import time
import undetected_chromedriver as uc
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures as cf
from tqdm import tqdm


options = uc.ChromeOptions()
options.add_argument('--headless=new')
# options.headless = False
driver = uc.Chrome(use_subprocess=True, options=options)
driver.maximize_window()

driver.get("https://www.turkanime.co/")
driver.find_element(By.XPATH, '//*[@id="aktif-sekme"]/li[2]/a').click()
time.sleep(2)
allAnimes = [{'anime': a.get_attribute('title'), 'url': a.get_attribute('href')} for a in
             driver.find_elements(By.XPATH, '//*[@id="sagScroll"]/ul/li/a[2]')]
print('Found -> ', len(allAnimes))

chrome_pool = []
max_drivers = 5
driver_statuses = [False] * max_drivers  # False indicates a driver is not in use

# Initialize the Chrome driver pool
for _ in range(max_drivers):
    options = uc.ChromeOptions()
    options.add_argument('--headless=new')
    driver = uc.Chrome(use_subprocess=True, options=options)
    chrome_pool.append(driver)

def findSubHeader(text):
    datalist = {
        "Kategori": "category",
        "İngilizce": "englishName",
        "Diğer Adları": "otherNames",
        "Japonca": "japanese",
        "Anime Türü": "types",
        "Bölüm Sayısı": "episodeCount",
        "Başlama Tarihi": "startDate",
        "Yayın Günü": "publishDate",
        "Yaş Sınırı": "ageLimit",
        "Yapımcı": "creator",
        "Stüdyo": "studio",
        "Bölüm Süresi": "episodeLength",
        "Puanı": "points",
        "Oylama": 'oylama-',
        "Fansub": "fansubs",
        "Altyazı": "cc",
        "Beğeniler": 'likes-',
        "Özet;": "content",
    }

    return datalist[text]


def translateConnectedAnimes(text):
    datalist = {
        "Ana Hikâye": "mainStory",
        "Önceki Hikâye": "previousSeasons",
        "Sonraki Hikâye": "nextSeasons",
        "Alternatif Versiyon": "otherVersions",
        "Yan Hikâye": "sideStory",
        "Özet": "shortStory",
        "Karakter": "character",
        "Alternatif Seçenek": "alternatif",
        "Diğerleri": "other"
    }

    if not datalist[text]:
        return "notfound"

    return datalist[text]


def get_available_driver_index():
    for i, status in enumerate(driver_statuses):
        if not status:
            driver_statuses[i] = True  # Mark the driver as in use
            return i
    return None  # No available drivers


def threaded_getAnimeInformation(anime):
    driver_index = get_available_driver_index()
    if driver_index is None:
        return None  # No available drivers, skip this task

    options_local = uc.ChromeOptions()
    options_local.add_argument('--headless=new')
    local_driver = uc.Chrome(use_subprocess=True, options=options_local)
    local_driver.maximize_window()

    try:
        return getAnimeInformation(anime['url'], local_driver)
    finally:
        local_driver.quit()
        driver_statuses[driver_index] = False  # Mark the driver as available



def getAnimeInformation(url, driver_thread):
    driver_thread.get(url)

    a = driver_thread.find_elements(By.XPATH,
                                    '/html/body/article/div/div[3]/div[2]/div/div[3]/div/div/div[2]/div/table/tbody/tr/td[2]/div/table/tbody/tr')
    animeName = driver_thread.find_element(By.CSS_SELECTOR, "#detayPaylas > div > div.panel-ust > div").text
    episodes = [a.get_attribute('href') for a in
                driver_thread.find_elements(By.XPATH, '//*[@id="sagScroll"]/ul/li/a[2]')]

    generalInformation = {'anime': animeName, 'url': url, 'information': {}, 'episodes': episodes, 'connectedAnimes': {}}
    for i in range(len(a)):
        try:
            b = findSubHeader(a[i].find_element(By.CSS_SELECTOR, 'td:nth-child(1)').text)

            c = a[i].find_element(By.CSS_SELECTOR, 'td:nth-child(3)').text
            if b == "Anime Türü":
                c = [k.text for k in
                     a[i].find_element(By.CSS_SELECTOR, 'td:nth-child(3)').find_elements(By.CSS_SELECTOR, 'a')]

            generalInformation['information'][b] = c
        except Exception as ex:
            continue

    driver_thread.find_element(By.CSS_SELECTOR, '#detayPaylas > div > div.panel-body > div > table > tbody > tr > td:nth-child(1) > table > tbody > tr:nth-child(2) > td > div > a:nth-child(3)').click()
    time.sleep(1)
    d = driver_thread.find_elements(By.CSS_SELECTOR, 'div.list-group.baglanti')
    for f in d:
        g = translateConnectedAnimes(f.find_element(By.CSS_SELECTOR, 'div.list-group-item > h5.list-group-item-heading').text)
        generalInformation['connectedAnimes'][g] = []
        i = f.find_elements(By.CSS_SELECTOR, 'a.list-group-item')
        for j in i:
            j_href = j.get_attribute('href')
            j_name = j.find_element(By.CSS_SELECTOR, 'h4.list-group-item-heading').text
            generalInformation['connectedAnimes'][g].append({'anime': j_name, 'url': j_href})

    driver_thread.close()
    return generalInformation


def getEpisodeInformation(url):
    driver.get(url)

    fansubs = driver.find_elements(By.CSS_SELECTOR, "#videodetay div div.pull-right button")
    fansubs_length = len(fansubs)
    fansubs_names = [a.text for a in fansubs]
    del fansubs

    returnList = []
    for i in range(fansubs_length):
        try:
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, f"#videodetay div div.pull-right button:nth-child({i + 1})").click()
            time.sleep(1)
            videoPlayers = driver.find_elements(By.XPATH, '//*[@id="videodetay"]/div/div[4]/button')
            videoPlayers_length = len(videoPlayers)
            videoPlayers_names = [a.text for a in videoPlayers]
            del videoPlayers

            fansub_players = []
            fansub_uploads = {'fansub': fansubs_names[i], 'players': videoPlayers_names, 'urls': fansub_players}

            for player in range(videoPlayers_length):
                if "SIBNET" in videoPlayers_names[player]:
                    # print(videoPlayers_names[player])
                    driver.find_element(By.XPATH, f'//*[@id="videodetay"]/div/div[4]/button[{player + 1}]').click()
                    time.sleep(5)
                    iframe = driver.find_element(By.CSS_SELECTOR, f"#videodetay div div.video-icerik iframe")
                    driver.switch_to.frame(iframe)
                    fansub_players.append(
                        driver.find_element(By.XPATH, f'//*[@id="iframe-container"]/iframe').get_attribute("src"))
                    driver.switch_to.default_content()
                else:
                    fansub_players.append("")

            returnList.append(fansub_uploads)
        except Exception as e:
            print(e)
            return 0

    with open("animes.json", "w") as file:
        file.write(json.dumps(returnList))
    return returnList


animeInformationList = []
total_animes = len(allAnimes)
completed_animes = 0  # Initialize the counter for completed tasks

with tqdm(total=total_animes) as pbar:
    with ThreadPoolExecutor(max_workers=max_drivers) as executor:
        future_to_anime = {executor.submit(threaded_getAnimeInformation, anime): anime for anime in allAnimes}

        for future in cf.as_completed(future_to_anime):
            anime = future_to_anime[future]
            try:
                animeInformation = future.result()
                if animeInformation:
                    animeInformationList.append(animeInformation)
                    completed_animes += 1

                    # Update the progress bar
                    pbar.update(1)

                    with open("seasonList.json", "w") as file:
                        file.write(json.dumps(animeInformationList))
            except Exception as e:
                print(f"Error gathering info for {anime}: {e}")

