from time import strptime
from django.db import connection
from datetime import datetime, date

class DB:
    def __init__(self):
        self.cursor = connection.cursor()
        
    def delete_entry(self, starttime, venue):
        self.cursor.execute(""" DELETE FROM bookings WHERE eventstarttime=%s AND venue=%s """, [starttime, venue])
        connection.commit()
    
    def create_user(self, fname, lname, unitno, residentid):
        self.cursor.execute("INSERT INTO usertable VALUES (%s, %s, %s, %s, %s)", [unitno, fname, lname, residentid, False])
    
    def create_admin(self, fname, lname, unitno, residentid):
        self.cursor.execute("INSERT INTO usertable VALUES (%s, %s, %s, %s, %s)", [unitno, fname, lname, residentid, True])
        
    def create_entry(self, starttime, venue, residentid):
        self.cursor.execute(""" INSERT INTO bookings VALUES (%s, %s, %s, %s) """, [starttime, date.today(), venue, residentid])
        connection.commit()
        
    def check_admin(self, residentid):
        self.cursor.execute("SELECT isadmin FROM usertable WHERE residentid=%s", [residentid])
        isadmin = self.cursor.fetchone()
        return isadmin[0]
        
    def create_venue_view(self, venue, date):
        self.cursor.execute(""" CREATE OR REPLACE VIEW venueavailtimes AS
            SELECT a.starttime, b.residentid
            FROM availtimes a
            LEFT JOIN bookings b
            ON b.eventstarttime = a.starttime
            AND b.eventdate = %s
            AND b.venue = %s """, [date, venue])
        connection.commit()
    
    def get_venues(self):
        self.cursor.execute("SELECT * FROM venues")
        venues = self.cursor.fetchall()

        return {'records': venues}
    
    def get_bbq_schedule(self):
        self.create_venue_view('BBQ Pit', date.today())
        self.cursor.execute("SELECT * from venueavailtimes")
        fetched = self.cursor.fetchall()
        
        availtimes = []
        for item in fetched:
            templist = []
            templist.append(item[0].strftime('%H:%M'))
            templist.append(item[1])
            availtimes.append(templist)

        return {'availtimes': availtimes, 'date': date.today()}

    def get_tenniscourt_schedule(self):
        self.create_venue_view('Tennis Court', date.today())
        self.cursor.execute("SELECT * from venueavailtimes")
        fetched = self.cursor.fetchall()
        
        availtimes = []
        for item in fetched:
            templist = []
            templist.append(item[0].strftime('%H:%M'))
            templist.append(item[1])
            availtimes.append(templist)

        return {'availtimes': availtimes, 'date': date.today()}

    def get_mph_schedule(self):
        self.create_venue_view('Multi-Purpose Hall', date.today())
        self.cursor.execute("SELECT * from venueavailtimes")
        fetched = self.cursor.fetchall()
        
        availtimes = []
        for item in fetched:
            templist = []
            templist.append(item[0].strftime('%H:%M'))
            templist.append(item[1])
            availtimes.append(templist)

        return {'availtimes': availtimes, 'date': date.today()}

    def get_tabletennis_schedule(self):
        self.create_venue_view('Table Tennis', date.today())
        self.cursor.execute("SELECT * from venueavailtimes")
        fetched = self.cursor.fetchall()
        
        availtimes = []
        for item in fetched:
            templist = []
            templist.append(item[0].strftime('%H:%M'))
            templist.append(item[1])
            availtimes.append(templist)

        return {'availtimes': availtimes, 'date': date.today()}
    
    def get_booking_count(self):
        self.cursor.execute("""SELECT v.venue_name, COUNT(*)
            FROM venues v, bookings b, usertable ut
            WHERE v.venue_name = b.venue
            AND b.residentid = ut.residentid
            AND ut.isadmin = 'False'
            GROUP BY v.venue_name
            ORDER BY COUNT(*) DESC""")
        fetched = self.cursor.fetchall()
        return fetched
    
    def get_least_booked(self):
        self.cursor.execute("""SELECT b1.venue, COUNT(*)
            FROM bookings b1, usertable ut
            WHERE b1.residentid = ut.residentid
            AND ut.isadmin = 'False'
            GROUP BY venue
            HAVING COUNT(*) <= ALL(
                SELECT COUNT(*)
                FROM bookings b2
                GROUP BY VENUE);""")
        fetched = self.cursor.fetchall()
        return fetched
    
    def get_most_booked(self):
        self.cursor.execute("""SELECT b1.venue, COUNT(*)
            FROM bookings b1, usertable ut
            WHERE b1.residentid = ut.residentid
            AND ut.isadmin = 'False'
            GROUP BY venue
            HAVING COUNT(*) >= ALL(
                SELECT COUNT(*)
                FROM bookings b2, usertable ut1
                WHERE b2.residentid = ut1.residentid
                AND ut1.isadmin = 'False'
                GROUP BY VENUE);""")
        fetched = self.cursor.fetchall()
        return fetched
    
    def get_most_booked_resident(self):
        self.cursor.execute("""SELECT ut.firstname, ut.lastname, u.unitnumber, COUNT(*)
            FROM unit u, usertable ut, bookings b1
            WHERE u.unitnumber = ut.unitnumber
            AND ut.residentid = b1.residentid
            AND ut.isadmin = 'False'
            GROUP BY ut.firstname, ut.lastname, u.unitnumber
            HAVING COUNT(*) >= ALL(
                SELECT COUNT(*)
                FROM bookings b2, usertable ut1
                WHERE b2.residentid = ut1.residentid
                AND ut1.isadmin = 'False'
                GROUP BY b2.residentid);""")
        fetched = self.cursor.fetchall()
        return fetched

