DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS usertable;
DROP TABLE IF EXISTS venues;

CREATE TABLE IF NOT EXISTS unit (
	unitnumber VARCHAR(64) PRIMARY KEY,
	residentid VARCHAR(64) UNIQUE NOT NULL);

-- CREATE TABLE IF NOT EXISTS usertable (
-- 	first_name VARCHAR(64) NOT NULL,
-- 	last_name VARCHAR(64) NOT NULL,
-- 	email VARCHAR(64) UNIQUE NOT NULL,
-- 	dob DATE NOT NULL,
-- 	since DATE NOT NULL,
-- 	residentid VARCHAR(16) PRIMARY KEY,
-- 	isadmin BOOLEAN NOT NULL
-- 	);

CREATE TABLE IF NOT EXISTS usertable (
	residentid VARCHAR(64) PRIMARY KEY REFERENCES unit(residentid) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
	firstname VARCHAR(64) NOT NULL,
	lastname VARCHAR(64) NOT NULL,
	email VARCHAR(64) UNIQUE NOT NULL,
	password VARCHAR(64) NOT NULL,
	isadmin BOOLEAN NOT NULL);

CREATE TABLE IF NOT EXISTS venues (
	venue_name VARCHAR(64) UNIQUE NOT NULL,
	description VARCHAR(64) NOT NULL,
	image_path VARCHAR(64) UNIQUE NOT NULL);
		
-- CREATE TABLE IF NOT EXISTS bookings (
-- 	eventstartdate timestamp NOT NULL,
-- 	eventenddate timestamp NOT NULL,
-- 	venue VARCHAR(32) REFERENCES venues(venue_name) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
-- 	residentid VARCHAR(16) REFERENCES usertable(residentid) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
-- 	PRIMARY KEY (residentid, venue));

CREATE TABLE IF NOT EXISTS bookings (
	eventstart timestamp NOT NULL,
	eventend timestamp NOT NULL,
	venue VARCHAR(32) REFERENCES venues(venue_name) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
	residentid VARCHAR(16) REFERENCES usertable(residentid) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY (venue, eventstart));
	
INSERT INTO venues VALUES ('BBQ Pit', 'BBQ', 'bbqpit');
INSERT INTO venues VALUES ('Tennis Court', 'Tennis', 'tenniscourt');
INSERT INTO venues VALUES ('Multi-Purpose Hall', 'MPH', 'mph');
INSERT INTO venues VALUES ('Table Tennis', 'Ping Pong', 'tabletennis');

-- INSERT INTO usertable VALUES ('first', 'user', 'email@email.com', '2010-10-10', '2022-10-10', 'unique_id', false);
-- INSERT INTO bookings VALUES ('2022-02-02 20:00', '2022-02-02 21:00', 'BBQ Pit', 'unique_id');

INSERT INTO unit VALUES ('01-01', 1);
INSERT INTO unit VALUES ('01-02', 2);
INSERT INTO unit VALUES ('01-03', 3);
INSERT INTO unit VALUES ('01-04', 4);
INSERT INTO unit VALUES ('01-05', 5);
INSERT INTO unit VALUES ('01-06', 6);
INSERT INTO unit VALUES ('01-07', 7);
INSERT INTO unit VALUES ('01-08', 8);
INSERT INTO unit VALUES ('01-09', 9);
INSERT INTO unit VALUES ('01-10', 10);
INSERT INTO unit VALUES ('01-11', 11);
INSERT INTO unit VALUES ('01-12', 12);

INSERT INTO usertable VALUES ('1', 'first', 'user', '1user@gmail.com', '1234', False);
INSERT INTO usertable VALUES ('2', 'second', 'user', '2user@gmail.com', '1234', False);
INSERT INTO usertable VALUES ('3', 'third', 'user', '3user@gmail.com', '1234', False);
INSERT INTO usertable VALUES ('4', 'fourth', 'user', '4user@gmail.com', '1234', False);
INSERT INTO usertable VALUES ('5', 'fifth', 'user', '5user@gmail.com', '1234', False);
INSERT INTO usertable VALUES ('6', 'sixth', 'user', '6user@gmail.com', '1234', False);
INSERT INTO usertable VALUES ('7', 'seventh', 'user', '7user@gmail.com', '1234', False);
INSERT INTO usertable VALUES ('8', 'eighth', 'user', '8user@gmail.com', '1234', False);
INSERT INTO usertable VALUES ('9', 'nineth', 'user', '9user@gmail.com', '1234', False);
INSERT INTO usertable VALUES ('10', 'tenth', 'user', '10user@gmail.com', '1234', False);
INSERT INTO usertable VALUES ('11', 'eleventh', 'user', '11user@gmail.com', '1234', False);
INSERT INTO usertable VALUES ('12', 'twelfth', 'user', '12user@gmail.com', '1234', False);

INSERT INTO bookings VALUES ('2022-02-02 20:00', '2022-02-02 21:00', 'BBQ Pit', '1');
INSERT INTO bookings VALUES ('2022-02-03 20:00', '2022-02-02 21:00', 'Tennis Court', '2');
INSERT INTO bookings VALUES ('2022-02-04 20:00', '2022-02-02 21:00', 'BBQ Pit', '3');
INSERT INTO bookings VALUES ('2022-02-05 20:00', '2022-02-02 21:00', 'BBQ Pit', '4');
INSERT INTO bookings VALUES ('2022-02-06 20:00', '2022-02-02 21:00', 'BBQ Pit', '2');
INSERT INTO bookings VALUES ('2022-02-07 20:00', '2022-02-02 21:00', 'BBQ Pit', '1');
INSERT INTO bookings VALUES ('2022-02-08 20:00', '2022-02-02 21:00', 'Tennis Court', '2');
INSERT INTO bookings VALUES ('2022-02-09 20:00', '2022-02-02 21:00', 'Tennis Court', '6');
INSERT INTO bookings VALUES ('2022-02-10 20:00', '2022-02-02 21:00', 'Tennis Court', '1');
INSERT INTO bookings VALUES ('2022-02-11 20:00', '2022-02-02 21:00', 'BBQ Pit', '7');
INSERT INTO bookings VALUES ('2022-02-12 20:00', '2022-02-02 21:00', 'BBQ Pit', '1');
INSERT INTO bookings VALUES ('2022-02-13 20:00', '2022-02-02 21:00', 'BBQ Pit', '8');
INSERT INTO bookings VALUES ('2022-02-14 20:00', '2022-02-02 21:00', 'Multi-Purpose Hall', '1');
INSERT INTO bookings VALUES ('2022-02-15 20:00', '2022-02-02 21:00', 'BBQ Pit', '6');
INSERT INTO bookings VALUES ('2022-02-16 20:00', '2022-02-02 21:00', 'BBQ Pit', '6');
INSERT INTO bookings VALUES ('2022-02-17 20:00', '2022-02-02 21:00', 'BBQ Pit', '6');
INSERT INTO bookings VALUES ('2022-02-18 20:00', '2022-02-02 21:00', 'BBQ Pit', '6');

--most booked venue--
SELECT b1.venue
FROM bookings b1
GROUP BY venue
HAVING COUNT(*) >= ALL(
  SELECT COUNT(*)
  FROM bookings b2
  GROUP BY VENUE);
  
--least booked venue--
SELECT b1.venue
FROM bookings b1
GROUP BY venue
HAVING COUNT(*) <= ALL(
  SELECT COUNT(*)
  FROM bookings b2
  GROUP BY VENUE);

--venue and number of bookings--
SELECT v.venue_name, COUNT(*)
FROM venues v, bookings b
WHERE v.venue_name = b.venue
GROUP BY v.venue_name
ORDER BY COUNT(*) DESC

--name and unit who booked most--
SELECT ut.firstname, ut.lastname, u.unitnumber
FROM unit u, usertable ut, bookings b1
WHERE u.residentid = ut.residentid
AND ut.residentid = b1.residentid
GROUP BY ut.firstname, ut.lastname, u.unitnumber
HAVING COUNT(*) >= ALL(
  SELECT COUNT(*)
  FROM bookings b2
  GROUP BY residentid);

--name and unit who have never booked before--
SELECT ut.firstname, ut.lastname, u.unitnumber
FROM unit u, usertable ut
WHERE u.residentid = ut.residentid
AND u.unitnumber NOT IN (
  SELECT u.unitnumber
  FROM unit u, bookings b
  WHERE u.residentid = b.residentid)
