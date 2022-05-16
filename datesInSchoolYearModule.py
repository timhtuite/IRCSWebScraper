# datesInSchoolYearModule.py
import datetime

def GetNextDayInSchoolYear(year):
    d1 = datetime.date(year - 1, 9, 1)
    d2 = datetime.date(year, 9, 1)
    while(d1 < d2):
        yield d1.strftime('%m/%d/%Y')
        d1 = d1 + datetime.timedelta(days=1)

#for day in GetNextDayInSchoolYear(2015):
    #print(day)
