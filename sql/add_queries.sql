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
  SELECT u1.unitnumber
  FROM unit u1, bookings b1, usertable ut1
  WHERE ut1.residentid = b1.residentid
  AND u1.unitnumber = ut1.unitnumber)