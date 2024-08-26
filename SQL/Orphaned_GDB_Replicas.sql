/* Checks for orphaned versions on an enterprise GDB
   orphaned versions will have a NULL GDB name field.
   They can be deleted using the delete replica GP tool or
   in the DB using SSMS.
  */

/* SDE DB */
select distinct Left(SubString(v.name, PatIndex('%[0-9.-]%', v.name), 10), PatIndex('%[^0-9.-]%', SubString(v.name, PatIndex('%[0-9.-]%', v.name), 10) + 'X')-1) as ID, v.name, g.Name as GDB_Name, g.DatasetInfo1
from sde.SDE_versions v left join sde.GDB_ITEMS g
on Left(SubString(v.name, PatIndex('%[0-9.-]%', v.name), 10), PatIndex('%[^0-9.-]%', SubString(v.name, PatIndex('%[0-9.-]%', v.name), 10) + 'X')-1) = g.ObjectID
where v.name like 'SYNC%'
order by GDB_Name;

/* dbo DB */
select distinct Left(SubString(v.name, PatIndex('%[0-9.-]%', v.name), 10), PatIndex('%[^0-9.-]%', SubString(v.name, PatIndex('%[0-9.-]%', v.name), 10) + 'X')-1) as ID, v.name, g.Name as GDB_Name, g.DatasetInfo1
from dbo.SDE_versions v left join dbo.GDB_ITEMS g
on Left(SubString(v.name, PatIndex('%[0-9.-]%', v.name), 10), PatIndex('%[^0-9.-]%', SubString(v.name, PatIndex('%[0-9.-]%', v.name), 10) + 'X')-1) = g.ObjectID
where v.name like 'SYNC%'
order by GDB_Name;