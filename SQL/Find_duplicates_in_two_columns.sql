/****** find and count the number of duplicates in two columns ******/

SELECT CornerID, year_adj, 
COUNT(*) as dupes
from dbo.gps
group by cornerID, year_adj
having count(*) > 1
order by year_adj desc