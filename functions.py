import os
import subprocess
import uuid
##################################File Name Generator###################################
#Pass String and return valid file name with time in miliseconds

def makefilename(name):

    filename = "".join(i for i in name if i not in "\/:*?<>| ") + str(uuid.uuid4().hex)
    return (filename)
########################################################################################


#########################Find all *.yaml and return the output with filename######################
def default_path(temp,severtys):
    Default_templates_path=makefilename(temp)+"default.txt"
    sub_sev =severtys.split(",")
    for sev in sub_sev:
        subprocess.check_output(f'grep -Ril ": {sev}" tools/nuclei_uploaded/DefaultTemplates/ >>./temp_files/{Default_templates_path}', shell=True)

    templates = os.popen(f'wc -l < ./temp_files/{Default_templates_path}').read()
    total = templates.replace("\n", '')
        #print(f'grep -Ril ": {sev}" tools/nuclei_uploaded/DefaultTemplates/ >>./temp_files/{Default_templates_path}')
    #subprocess.check_output("find tools/nuclei_uploaded/DefaultTemplates/ -name *.yaml >>temp_files/"+Default_templates_path , shell=True)

    return (Default_templates_path,total)
####################################################################################################
#a= default_path("dd","High,Critical")
#print(f'Templates Count: {a[1]}')
