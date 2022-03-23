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