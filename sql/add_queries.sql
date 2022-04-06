--most booked venue-- 
SELECT v1.venue_name, COUNT(b1.venue) 
FROM venues v1 LEFT OUTER JOIN bookings b1 ON v1.venue_name = b1.venue 
GROUP BY v1.venue_name
HAVING COUNT(b1.venue) >= ALL( 
  SELECT COUNT(b2.venue) 
  FROM venues v2 LEFT OUTER JOIN bookings b2 ON v2.venue_name = b2.venue 
  GROUP BY v2.venue_name); 
  
--least booked venue-- 
SELECT v1.venue_name, COUNT(b1.venue) 
FROM venues v1 LEFT OUTER JOIN bookings b1 ON v1.venue_name = b1.venue 
GROUP BY v1.venue_name
HAVING COUNT(b1.venue) <= ALL( 
  SELECT COUNT(b2.venue) 
  FROM venues v2 LEFT OUTER JOIN bookings b2 ON v2.venue_name = b2.venue 
  GROUP BY v2.venue_name); 
 
--venue and number of bookings-- 
SELECT v.venue_name, COUNT(b.venue) 
FROM venues v LEFT OUTER JOIN bookings b ON v.venue_name = b.venue 
GROUP BY v.venue_name, b.venue 
ORDER BY COUNT(b.venue) DESC; 
 
--name and unit who booked most-- 
SELECT ut1.firstname, ut1.lastname, u.unitnumber 
FROM unit u, usertable ut1, bookings b1 
WHERE u.unitnumber = ut1.unitnumber 
AND ut1.residentid = b1.residentid 
GROUP BY ut1.firstname, ut1.lastname, u.unitnumber 
HAVING COUNT(*) >= ALL( 
  SELECT COUNT(*) 
  FROM bookings b2, usertable ut2 
  WHERE b2.residentid = ut2.residentid 
  AND ut2.isadmin = 'False' 
  GROUP BY b2.residentid); 
 
--name and unit who have never booked before-- 
SELECT ut1.firstname, ut1.lastname, u.unitnumber 
FROM unit u, usertable ut1 
WHERE u.unitnumber = ut1.unitnumber 
AND ut1.isadmin = 'False' 
AND u.unitnumber NOT IN ( 
  SELECT ut2.unitnumber 
  FROM usertable ut2, bookings b 
  WHERE ut2.residentid = b.residentid);
