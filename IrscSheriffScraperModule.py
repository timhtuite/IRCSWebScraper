# IrscSheriffScraperModule.py
import requests
from bs4 import BeautifulSoup
from SafeConsoleModule import safe_print
from dateutil import parser

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
        link = linkToArrestRecord['href']
        # write a row to the csv file
        d = GetInmateArrestInfo(link)
        name = fullname.text.strip()
        race = raceGender[0].strip()
        gender = raceGender[1].strip()
        arrestCount = d['NumberOfArrests']
        mostRecent = d['MostRecentArrestDate']

        results.append([name,gender,race,link,day,mostRecent,arrestCount])
        #print(image);
        safe_print("{} {} {}".format(name, gender, race))
        safe_print(link)

def GetInmateArrestInfo(url):
    d = dict();
    individualArrestPage = requests.get(url, verify=False)
    #print(arrestSearchResult.text)
    arrestInfoSoup = BeautifulSoup(individualArrestPage.content, "html.parser")
    select = arrestInfoSoup.find("select", {"id":"bookings"})
    bookingsElements = select.find_all("option");
    #print(image);
    numberOfArrests = len(bookingsElements)
    txt = bookingsElements[0].text
    mostRecentArrestDate = txt[txt.find("(")+1:txt.find(")")]
    d['NumberOfArrests'] = numberOfArrests
    d['MostRecentArrestDate'] = parser.parse(mostRecentArrestDate).strftime('%m/%d/%Y')
    return d
