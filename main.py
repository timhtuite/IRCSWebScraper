# Tim Tuite
# Scrape data from indian river county sheriff site
# first we have to get a valid token from the form page
# then we can programatically call the search endpoint
import requests
from bs4 import BeautifulSoup
import datetime
from datetime import date
import csv
from datesInSchoolYearModule import GetNextDayInSchoolYear
import threading
from SafeConsoleModule import safe_print
from IrcSheriffScraperModule import InmateSearch

# ignore requests SSL warning
import warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

#Program Variables
header = ["Name","Gender","Race","Link","DOB"]
gradYear = 2014
today = date.today()
concurreny = 6
results = []
# dd/mm/YY
todayString = today.strftime("%m%d%Y")
fileName = "ArrestsGradYear{}AsOf{}.csv".format(gradYear,todayString)
#Set up file to write to
# open the file in the write mode
f = open(fileName, 'w')

# create the csv writer
writer = csv.writer(f)
# write the header
writer.writerow(header)

formUrl = "https://ircsheriff.org/inmate-search"
formPage = requests.get(formUrl, verify=False)
#print(formPage.text)
cookieDict = formPage.cookies.get_dict(domain="ircsheriff.org")
print cookieDict
formPageSoup = BeautifulSoup(formPage.content, "html.parser")
token = formPageSoup.find("input",{"name":"_token"})['value']
#print token

threads = []
for day in GetNextDayInSchoolYear(gradYear - 18):
    th = threading.Thread(target=InmateSearch, args=(day, token, results, cookieDict))
    #InmateSearch(day, token, writer, cookieDict)
    threads.append(th)
executedThreadCount = 0
tail = (len(threads) % concurreny)
count = len(threads) - tail
while(executedThreadCount < count):
    for i in range(concurreny):
        threads[i + executedThreadCount].start()
    for i in range(concurreny):
        threads[i + executedThreadCount].join()
    executedThreadCount += concurreny
# execute what is left
for i in range(tail):
    threads[i + executedThreadCount].start()
for i in range(tail):
    threads[i + executedThreadCount].join()

for result in results:
    writer.writerow(result)
# close the file
f.close()
