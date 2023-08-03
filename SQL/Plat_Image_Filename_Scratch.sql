/* 1. select all records w/ doc # and replace fielanme with doc#+.pdf */
UPDATE dbo.Plat_Image_filename3 /* table with data */
SET Filename = CONCAT([Doc Number], '.pdf') /* filename is the field to be updated with CONCAT() */
where [Doc Number] is not null


/* 2. Remove duplicate CornerID records */
WITH CTE AS(
SELECT [Plat Name],
RN = ROW_NUMBER()OVER(PARTITION BY [Plat Name] ORDER BY [Recorded Date] desc)
FROM dbo.Plat_Image_filename3
)
DELETE FROM CTE WHERE RN > 1

select object_name(object_id),* from sys.key_constraints where object_name(parent_object_id) = 'Plat_Image_filename3'


/* 3. Filename is doc# but Doc Number field is blank */
/* test query*/
select *
from dbo.Plat_Image_filename3
where LEN(Filename) = 14 and [Doc Number] is null and Filename like '%.tif%'
order by Filename asc

/* update/replace query - replaces .tif with .pdf */
UPDATE 
    dbo.Plat_Image_filename3
SET 
    Filename = REPLACE(Filename,'.tif','.pdf')
WHERE 
    LEN(Filename) = 14 and [Doc Number] is null and Filename like '%.tif%'

/* 4. Plat names that r #s but have other fielname */
/* test query - will return no records after update query runs */
select *
from dbo.Plat_Image_filename3
where LEN([Plat Name]) = 8 and [Plat Name] like '%-%' and Filename not like '%-%'
order by [Plat Name] asc

/* update query */
UPDATE dbo.Plat_Image_filename3
SET Filename = CONCAT([Plat Name], '.pdf')
where LEN([Plat Name]) = 8 and [Plat Name] like '%-%' and Filename not like '%-%'

/* 5. use existing renaming filenames but replace .tif with .pdf */



