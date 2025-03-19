import ifcopenshell
file = ifcopenshell.open('/Users/emyu/Downloads/20250316.ifc')
columns = file.by_type('IfcColumn')
for i in columns:
    print(i.Name)