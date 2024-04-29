/****** find and count the number of duplicates in a single column ******/

SELECT CornerID, COUNT(*) as dupes /** column name, count, count column name **/
from dbo.gps /** table name **/
group by cornerID 
having count(*) > 1 
order by dupes desc  