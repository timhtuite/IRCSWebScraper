from __future__ import division, unicode_literals
import codecs
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf8')

f = codecs.open("TestDataIndividual.html", 'r', 'utf-8')
document = BeautifulSoup(f.read(), "html.parser")
bookingsElements = document.find("select", {"id":"bookings"}).find_all("option");
#print(image);
numberofArrests = len(bookingsElements)
txt = bookingsElements[0].text
mostRecentArrestDate = txt[txt.find("(")+1:txt.find(")")]
print("Number of Arrests: {}".format(numberofArrests))
print("Most recent Arrest: {}".format(mostRecentArrestDate))
