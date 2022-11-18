def FindLabel ( [FDPRE] , [FNAME] ,  [FTYPE] ):
  type = [FTYPE]
  if type == "STREET":
    type = "St"
  if type == "BOULEVARD":
    type = "Blvd"
  if type == "ROAD":
    type = "Rd"
  if type == "HIGHWAY":
    type = "Hwy"
  if type == 'DRIVE':
    type = "Dr"
  if type == "LANE":
    type = "Ln"
  if type == "AVENUE":
    type = "Ave"
  if type == "PLACE":
    type = "Pl"
  if type == "COURT":
    type = "Ct"
  else:
    type = type.title()

  name = [FNAME]
  last = name[-2:]
  name_list = ["RD", "TH", "ST"]
  name1 = False
  name2 = name.title()

  
  if last in name_list:
    name1 = name[:-2]
  try:
    if float(name1):
      name2 = name.lower()
  except:
    name2 = name.title()

  return [FDPRE] + " " + name2 + " " + type