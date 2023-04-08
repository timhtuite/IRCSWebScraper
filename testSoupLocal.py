from __future__ import division, unicode_literals
import codecs
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf8')

f = codecs.open("TestData.html", 'r', 'utf-8')
document = BeautifulSoup(f.read(), "html.parser")
arrestTitles = document.find_all("div", {"class":"inmate inmate-list clearfix"})

for arrest in arrestTitles:
    fullname = arrest.find("h4")

    image = arrest.find("div", {"class":"inmate-image"})
    content = arrest.find("div", {"class":"inmate-content"})
    raceGender = content.find("p").text.split("/")
    race = raceGender[0].strip()
    gender = raceGender[1].strip()
    linkToArrestRecord = image.find("a")
    # write a row to the csv file
    name = fullname.text.strip()
    link = linkToArrestRecord['href']
    #print(image);
    print(name)
    print(race)
    print(gender)
    print(link)
