import json

#input file
fin = open("/home/ya7ya/results", "rt")


for line in fin:
 #print (type(line))
 json_object = json.loads(line)
 #data = json.loads(json_object)
 print (json_object["host"])




