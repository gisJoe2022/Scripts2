/* 
first query create a system table (all_survnum) with rows numbering 
 from 1 - 34551.

the second query joins the suvey_image db table TO the all_survnum 
system generated table by surveynumber then selects the records that 
have a null value = missing numbers in the surveynumber sequence

 */


with all_survnum as (
	select n = ROW_NUMBER() over (order by number)
	from master..spt_values
	where type = 'P'
	and number between 1 and 34551
	)

	select all_survnum.n as missing_survnum
	from all_survnum
	left join dbo.Survey_Image on all_survnum.n = dbo.Survey_Image.Surveynumber
	where dbo.Survey_Image.Surveynumber is null;