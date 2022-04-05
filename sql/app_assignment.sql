DROP VIEW IF EXISTS venueavailtime;
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS usertable;
DROP TABLE IF EXISTS venues;
DROP TABLE IF EXISTS unit;
DROP TABLE IF EXISTS availtimes;

CREATE TABLE IF NOT EXISTS unit (
	unitnumber VARCHAR(64) PRIMARY KEY);

CREATE TABLE IF NOT EXISTS usertable (
	unitnumber VARCHAR(64) REFERENCES unit(unitnumber) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
	firstname VARCHAR(64) NOT NULL,
	lastname VARCHAR(64) NOT NULL,
	residentid VARCHAR(64) PRIMARY KEY,
	isadmin BOOLEAN NOT NULL);

CREATE TABLE IF NOT EXISTS venues (
	venue_name VARCHAR(64) UNIQUE NOT NULL,
	description VARCHAR(64) NOT NULL,
	image_path VARCHAR(64) UNIQUE NOT NULL);

CREATE TABLE IF NOT EXISTS bookings (
	eventstarttime TIME NOT NULL CHECK (eventstarttime >= '08:00:00' AND eventstarttime <= '22:00:00'),
	eventdate DATE NOT NULL,
	venue VARCHAR(64) REFERENCES venues(venue_name) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
	residentid VARCHAR(64) REFERENCES usertable(residentid) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY (venue, eventstarttime, eventdate));

CREATE TABLE IF NOT EXISTS availtimes (
	starttime TIME NOT NULL CHECK (starttime >= '08:00:00' AND starttime <= '22:00:00'));
	
INSERT INTO venues VALUES ('BBQ Pit', 'BBQ', 'bbqpit');
INSERT INTO venues VALUES ('Tennis Court', 'Tennis', 'tenniscourt');
INSERT INTO venues VALUES ('Multi-Purpose Hall', 'MPH', 'mph');
INSERT INTO venues VALUES ('Table Tennis', 'Ping Pong', 'tabletennis');

-- INSERT INTO usertable VALUES ('first', 'user', 'email@email.com', '2010-10-10', '2022-10-10', 'unique_id', false);
-- INSERT INTO bookings VALUES ('2022-02-02 20:00', '2022-02-02 21:00', 'BBQ Pit', 'unique_id');

INSERT INTO unit VALUES ('admin');
INSERT INTO unit VALUES ('01-01');
INSERT INTO unit VALUES ('01-02');
INSERT INTO unit VALUES ('01-03');
INSERT INTO unit VALUES ('01-04');
INSERT INTO unit VALUES ('01-05');
INSERT INTO unit VALUES ('01-06');
INSERT INTO unit VALUES ('01-07');
INSERT INTO unit VALUES ('01-08');
INSERT INTO unit VALUES ('01-09');
INSERT INTO unit VALUES ('01-10');
INSERT INTO unit VALUES ('01-11');
INSERT INTO unit VALUES ('01-12');

INSERT INTO availtimes VALUES ('08:00:00');
INSERT INTO availtimes VALUES ('09:00:00');
INSERT INTO availtimes VALUES ('10:00:00');
INSERT INTO availtimes VALUES ('11:00:00');
INSERT INTO availtimes VALUES ('12:00:00');
INSERT INTO availtimes VALUES ('13:00:00');
INSERT INTO availtimes VALUES ('14:00:00');
INSERT INTO availtimes VALUES ('15:00:00');
INSERT INTO availtimes VALUES ('16:00:00');
INSERT INTO availtimes VALUES ('17:00:00');
INSERT INTO availtimes VALUES ('18:00:00');
INSERT INTO availtimes VALUES ('19:00:00');
INSERT INTO availtimes VALUES ('20:00:00');
INSERT INTO availtimes VALUES ('21:00:00');
INSERT INTO availtimes VALUES ('22:00:00');

INSERT INTO usertable VALUES ('01-01', 'first', 'user', '1user', False);
INSERT INTO usertable VALUES ('01-02', 'second', 'user', '2user', False);
INSERT INTO usertable VALUES ('01-03', 'third', 'user', '3user', False);
INSERT INTO usertable VALUES ('01-04', 'fourth', 'user', '4user', False);
INSERT INTO usertable VALUES ('01-05', 'fifth', 'user', '5user', False);
INSERT INTO usertable VALUES ('01-06', 'sixth', 'user', '6user', False);
INSERT INTO usertable VALUES ('01-07', 'seventh', 'user', '7user', False);
INSERT INTO usertable VALUES ('01-08', 'eighth', 'user', '8user', False);
INSERT INTO usertable VALUES ('01-09', 'nineth', 'user', '9user', False);
INSERT INTO usertable VALUES ('01-10', 'tenth', 'user', '10user', False);
INSERT INTO usertable VALUES ('01-11', 'eleventh', 'user', '11user', False);
INSERT INTO usertable VALUES ('01-12', 'twelfth', 'user', '12user', False);
INSERT INTO usertable VALUES ('admin', 'admin', 'one', 'admin1', True);

INSERT INTO bookings VALUES ('20:00', '2022-04-02', 'BBQ Pit', '1user');
INSERT INTO bookings VALUES ('20:00', '2022-04-03', 'Tennis Court', '2user');
INSERT INTO bookings VALUES ('20:00', '2022-04-04', 'BBQ Pit', '3user');
INSERT INTO bookings VALUES ('20:00', '2022-04-05', 'BBQ Pit', '4user');
INSERT INTO bookings VALUES ('20:00', '2022-04-06', 'BBQ Pit', '2user');
INSERT INTO bookings VALUES ('20:00', '2022-04-07', 'BBQ Pit', '1user');
INSERT INTO bookings VALUES ('20:00', '2022-04-08', 'Tennis Court', '2user');
INSERT INTO bookings VALUES ('20:00', '2022-04-09', 'Tennis Court', '6user');
INSERT INTO bookings VALUES ('20:00', '2022-04-10', 'Tennis Court', '1user');
INSERT INTO bookings VALUES ('20:00', '2022-04-11', 'BBQ Pit', '7user');
INSERT INTO bookings VALUES ('20:00', '2022-04-12', 'BBQ Pit', '1user');
INSERT INTO bookings VALUES ('20:00', '2022-04-13', 'BBQ Pit', '8user');
INSERT INTO bookings VALUES ('20:00', '2022-04-14', 'Multi-Purpose Hall', '1user');
INSERT INTO bookings VALUES ('20:00', '2022-04-15', 'BBQ Pit', '6user');
INSERT INTO bookings VALUES ('20:00', '2022-04-16', 'BBQ Pit', '6user');
INSERT INTO bookings VALUES ('20:00', '2022-04-17', 'BBQ Pit', '6user');
INSERT INTO bookings VALUES ('20:00', '2022-04-18', 'BBQ Pit', '6user');
