def FindLabel ([LABEL] , [CITY]):
  type = [LABEL]
  city = [CITY]
  if type == "A":
    type = "Area A"
  if type == "AOI":
    type = "Area of Interest"
  if type == "B":
    type = "Area B"
  if type == "C":
    type = "Area C"
  if type == "City":
    type = ", City of"
  if type == "UPA":
    type = "Urban Planning Area"
  if type == "URPA":
    type = "Urban Reserve Planning Area"
  if type == "URPAU":
    type = "Urban Reserve - Planning Responsibility Undefined"
  if type == "URSA":
    type = "Banks - Urban Reserve Study Area"
  if city == "None":
    city = " "
  else:
    type = type
      
  return city.title() + " " + type


  """ name = [FNAME]
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

  return [FDPRE] + " " + name2 + " " + type """