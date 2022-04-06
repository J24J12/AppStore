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
        self.cursor.execute("""SELECT v.venue_name, COUNT(b.venue) 
            FROM venues v LEFT OUTER JOIN bookings b ON v.venue_name = b.venue 
            GROUP BY v.venue_name, b.venue 
            ORDER BY COUNT(b.venue) DESC;""")
        fetched = self.cursor.fetchall()
        return fetched
    
    def get_least_booked(self):
        self.cursor.execute("""SELECT v1.venue_name, COUNT(b1.venue) 
            FROM venues v1 LEFT OUTER JOIN bookings b1 ON v1.venue_name = b1.venue 
            GROUP BY v1.venue_name, b1.venue 
            HAVING COUNT(b1.venue) <= ALL( 
                SELECT COUNT(b2.venue) 
                FROM venues v2 LEFT OUTER JOIN bookings b2 ON v2.venue_name = b2.venue 
                GROUP BY v2.venue_name, b2.venue); 
                """)
        fetched = self.cursor.fetchall()
        return fetched
    
    def get_most_booked(self):
        self.cursor.execute("""SELECT v1.venue_name, COUNT(b1.venue) 
            FROM venues v1 LEFT OUTER JOIN bookings b1 ON v1.venue_name = b1.venue 
            GROUP BY v1.venue_name
            HAVING COUNT(b1.venue) >= ALL( 
                SELECT COUNT(b2.venue) 
                FROM venues v2 LEFT OUTER JOIN bookings b2 ON v2.venue_name = b2.venue 
                GROUP BY v2.venue_name); 
                """)
        fetched = self.cursor.fetchall()
        return fetched
    
    def get_most_booked_resident(self):
        self.cursor.execute("""SELECT ut1.firstname, ut1.lastname, u.unitnumber, COUNT(*)
            FROM unit u, usertable ut1, bookings b1 
            WHERE u.unitnumber = ut1.unitnumber 
            AND ut1.residentid = b1.residentid 
            GROUP BY ut1.firstname, ut1.lastname, u.unitnumber 
            HAVING COUNT(*) >= ALL( 
                SELECT COUNT(*) 
                FROM bookings b2, usertable ut2 
                WHERE b2.residentid = ut2.residentid 
                AND ut2.isadmin = 'False' 
                GROUP BY b2.residentid); """)
        fetched = self.cursor.fetchall()
        return fetched
    
    def never_booked_resident(self):
        self.cursor.execute("""SELECT ut1.firstname, ut1.lastname, u.unitnumber 
            FROM unit u, usertable ut1 
            WHERE u.unitnumber = ut1.unitnumber 
            AND ut1.isadmin = 'False' 
            AND u.unitnumber NOT IN ( 
                SELECT ut2.unitnumber 
                FROM usertable ut2, bookings b 
                WHERE ut2.residentid = b.residentid);""")
        fetched = self.cursor.fetchall()
        return fetched
    
    def get_latest_created_user(self):
        self.cursor.execute("SELECT * FROM latest_created_user")
        fetched = self.cursor.fetchall()
        return fetched

