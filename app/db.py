from django.db import connection
from datetime import datetime

class DB:
    def __init__(self):
        self.cursor = connection.cursor()
    
    def get_venues(self):
        self.cursor.execute("SELECT * FROM venues")
        venues = self.cursor.fetchall()

        return {'records': venues}
    
    def get_bbq_schedule(self):
        availtimes = []
        curryear = 2022
        currmonth = 2
        currdate = 2
        starttime = 8
        endtime = 22
        
        self.cursor.execute("SELECT eventstartdate FROM bookings WHERE venue='BBQ Pit'")
        fetched = self.cursor.fetchall()
        
        unavailtimes = list(sum(fetched, ()))
        
        for i in range(endtime - starttime):
            startstamp = datetime(curryear, currmonth, currdate, i + starttime, 0)
            endstamp = datetime(curryear, currmonth, currdate, i + starttime + 1, 0)
            availtimes.append([startstamp, endstamp, startstamp in unavailtimes])
        
        return {'available': availtimes}

    def get_tenniscourt_schedule(self):
        availtimes = []
        curryear = 2022
        currmonth = 2
        currdate = 2
        starttime = 8
        endtime = 22
        
        self.cursor.execute("SELECT eventstartdate FROM bookings WHERE venue='Tennis Court'")
        fetched = self.cursor.fetchall()
        
        unavailtimes = list(sum(fetched, ()))
        
        for i in range(endtime - starttime):
            startstamp = datetime(curryear, currmonth, currdate, i + starttime, 0)
            endstamp = datetime(curryear, currmonth, currdate, i + starttime + 1, 0)
            availtimes.append([startstamp, endstamp, startstamp in unavailtimes])
        
        return {'available': availtimes}

    def get_mph_schedule(self):
        availtimes = []
        curryear = 2022
        currmonth = 2
        currdate = 2
        starttime = 8
        endtime = 22
        
        self.cursor.execute("SELECT eventstartdate FROM bookings WHERE venue='MPH'")
        fetched = self.cursor.fetchall()
        
        unavailtimes = list(sum(fetched, ()))
        
        for i in range(endtime - starttime):
            startstamp = datetime(curryear, currmonth, currdate, i + starttime, 0)
            endstamp = datetime(curryear, currmonth, currdate, i + starttime + 1, 0)
            availtimes.append([startstamp, endstamp, startstamp in unavailtimes])
        
        return {'available': availtimes}

    def get_tabletennis_schedule(self):
        availtimes = []
        curryear = 2022
        currmonth = 2
        currdate = 2
        starttime = 8
        endtime = 22
        
        self.cursor.execute("SELECT eventstartdate FROM bookings WHERE venue='Table Tennis'")
        fetched = self.cursor.fetchall()
        
        unavailtimes = list(sum(fetched, ()))
        
        for i in range(endtime - starttime):
            startstamp = datetime(curryear, currmonth, currdate, i + starttime, 0)
            endstamp = datetime(curryear, currmonth, currdate, i + starttime + 1, 0)
            availtimes.append([startstamp, endstamp, startstamp in unavailtimes])

        return {'available': availtimes}

