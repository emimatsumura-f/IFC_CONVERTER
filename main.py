import ifcopenshell
file = ifcopenshell.open('20241102.ifc')
columns = file.by_type('IfcColumn')
for i in columns:
    print(i.Name)