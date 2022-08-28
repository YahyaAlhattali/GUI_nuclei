import time
import subprocess
import uuid
##################################File Name Generator###################################
#Pass String and return valid file name with time in miliseconds

def makefilename(name):

    filename = "".join(i for i in name if i not in "\/:*?<>| ") + str(uuid.uuid4().hex)
    return (filename)
########################################################################################


#########################Find all *.yaml and return the output with filename######################
def default_path(temp):
    Default_templates_path=makefilename(temp)+"default.txt"
    subprocess.check_output("find tools/nuclei_uploaded/DefaultTemplates/ -name *.yaml >>temp_files/"+Default_templates_path , shell=True)

    return (Default_templates_path)
####################################################################################################
