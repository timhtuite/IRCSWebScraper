# IrcSheriffScraperModule.py
import requests
from bs4 import BeautifulSoup
from SafeConsoleModule import safe_print

formUrl = "https://ircsheriff.org/inmate-search"
searchUrl = "https://www.ircsheriff.org/booking-search/search"

def InmateSearch(day, token, results, cookieDict):
    safe_print("Getting records for date: {}".format(day))
    myobj = {
    'dob': day,
    '_token': token
    }
    arrestSearchResult = requests.post(searchUrl, data = myobj, cookies=cookieDict, verify=False)
    #print(arrestSearchResult.text)
    arrestSearchSoup = BeautifulSoup(arrestSearchResult.content, "html.parser")
    arrestTitles = arrestSearchSoup.find_all("div", {"class":"inmate inmate-list clearfix"})

    for arrest in arrestTitles:
        fullname = arrest.find("h4")

        image = arrest.find("div", {"class":"inmate-image"})
        content = arrest.find("div", {"class":"inmate-content"})
        raceGender = content.find("p").text.split("/")
        linkToArrestRecord = image.find("a")
        # write a row to the csv file
        name = fullname.text.strip()
        link = linkToArrestRecord['href']
        race = raceGender[0].strip()
        gender = raceGender[1].strip()
        results.append([name,gender,race,link,day])
        #print(image);
        safe_print("{} {} {}".format(name, gender, race))
        safe_print(link)
