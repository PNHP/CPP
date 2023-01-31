import arcpy

biotics = "H://"

field_names = ["a","b","c","d"]
field_types = ["TEXT","TEXT","TEXT","FLOAT"]
field_length = [255,500,100,""]

for name,typ,length in zip(field_names,field_types,field_length):
    arcpy.management.AddField(biotics,name,typ,field_length=length)