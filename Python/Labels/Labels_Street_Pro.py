def FindLabel ( [FDPRE] , [FNAME] ,  [FTYPE] ):
  type = [FTYPE]
  if type == "STREET":
    type = "ST"
  if type == "BOULEVARD":
    type = "BLVD"
  if type == "ROAD":
    type = "RD"
  if type == "HIGHWAY":
    type = "HWY"
  if type == 'DRIVE':
    type = "DR"
  if type == "LANE":
    type = "LN"
  if type == "AVENUE":
    type = "Ave"
  if type == "PLACE":
    type = "PL"
  if type == "COURT":
    type = "CT"
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
      name2 = name.upper()
  except:
    name2 = name.title()

  return name2 + " " + type