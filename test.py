import math
import os
import time

#templates = os.popen('wc -l < ./temp_files/RopScan637a350f822e43028d4af23eb10acd0adefault.txt').read()
total = "200"

for l in range(1,201):
    rf = (l / int(total)) * 100
    print(math.trunc(int(rf)))
    #print(type(rf))
    #time.sleep(0.1)