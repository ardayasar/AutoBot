import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import undetected_chromedriver as uc

options = uc.ChromeOptions()
options.add_argument('--headless')
driver = uc.Chrome(use_subprocess=True, options=options)
driver.maximize_window()

driver.get("https://www.turkanime.co/")
driver.find_element(By.XPATH, '//*[@id="aktif-sekme"]/li[2]/a').click()
time.sleep(2)
allAnimes = [{'anime': a.get_attribute('title'), 'url': a.get_attribute('href')} for a in driver.find_elements(By.XPATH, '//*[@id="sagScroll"]/ul/li/a[2]')]
print(allAnimes)



def getAnimeInformation(url):
    driver.get(url)

    a = driver.find_elements(By.XPATH, '/html/body/article/div/div[3]/div[2]/div/div[3]/div/div/div[2]/div/table/tbody/tr/td[2]/div/table/tbody/tr')
    animeName = driver.find_element(By.CSS_SELECTOR, "#detayPaylas > div > div.panel-ust > div").text
    episodes = [a.get_attribute('href') for a in driver.find_elements(By.XPATH, '//*[@id="sagScroll"]/ul/li/a[2]')]

    generalInformation = {'anime': animeName, 'information': {}, 'episodes': episodes}
    for i in range(len(a)):
        try:
            b = a[i].find_element(By.CSS_SELECTOR, 'td:nth-child(1)').text
            c = a[i].find_element(By.CSS_SELECTOR, 'td:nth-child(3)').text
            if b == "Anime Türü":
                c = [k.text for k in
                    a[i].find_element(By.CSS_SELECTOR, 'td:nth-child(3)').find_elements(By.CSS_SELECTOR, 'a')]
            generalInformation['information'][b] = c
        except Exception as ex:
            continue

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
            # print(videoPlayers_names)
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


# animeInformation = getAnimeInformation("https://www.turkanime.co/anime/saikyou-onmyouji-no-isekai-tenseiki")
# for episode in animeInformation['episodes']:
#     episodeInformation = getEpisodeInformation(episode)
#     print(episodeInformation)

animeInformationList = []

for anime in allAnimes:
    print('Gathering -> ', anime)
    animeInformation = getAnimeInformation(anime['url'])
    animeInformationList.append(animeInformation)
    with open("animeList.json", "w") as file:
        file.write(json.dumps(animeInformationList))
    # for episode in animeInformation['episodes']:
    #     episodeInformation = getEpisodeInformation(episode)
    #     print(episodeInformation)

