DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS usertable;
DROP TABLE IF EXISTS venues;

CREATE TABLE IF NOT EXISTS usertable (
	first_name VARCHAR(64) NOT NULL,
	last_name VARCHAR(64) NOT NULL,
	email VARCHAR(64) UNIQUE NOT NULL,
	dob DATE NOT NULL,
	since DATE NOT NULL,
	residentid VARCHAR(16) PRIMARY KEY,
	isadmin BOOLEAN NOT NULL
	);

CREATE TABLE IF NOT EXISTS activeuser (
	residentid VARCHAR(16) REFERENCES usertable(residentid)
	);

CREATE TABLE IF NOT EXISTS venues (
	venue_name VARCHAR(64) UNIQUE NOT NULL,
	description VARCHAR(64) NOT NULL,
	image_path VARCHAR(64) UNIQUE NOT NULL);
		
CREATE TABLE IF NOT EXISTS bookings (
	eventstartdate timestamp NOT NULL,
	eventenddate timestamp NOT NULL,
	venue VARCHAR(32) REFERENCES venues(venue_name) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
	residentid VARCHAR(16) REFERENCES usertable(residentid) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY (residentid, venue));

	
INSERT INTO venues VALUES ('BBQ Pit', 'BBQ', 'bbqpit');
INSERT INTO venues VALUES ('Tennis Court', 'Tennis', 'tenniscourt');
INSERT INTO venues VALUES ('Multi-Purpose Hall', 'MPH', 'mph');
INSERT INTO venues VALUES ('Table Tennis', 'Ping Pong', 'tabletennis');

INSERT INTO usertable VALUES ('first', 'user', 'email@email.com', '2010-10-10', '2022-10-10', 'unique_id', false);
INSERT INTO bookings VALUES ('2022-02-02 20:00', '2022-02-02 21:00', 'BBQ Pit', 'unique_id');