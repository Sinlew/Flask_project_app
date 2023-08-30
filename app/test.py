import re

number = "p89999090900"
pattern_number = '^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'
if re.fullmatch(pattern_number, number):
   print("ok")