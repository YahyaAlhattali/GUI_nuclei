import subprocess
import validators
import functions
def sub(domain,current_user):
  if validators.domain(domain) == True:
    try:
         subfinder_output = functions.makefilename("suboutput")+".txt"
         httpx_output = functions.makefilename("httpx")+".txt"
         subprocess.check_output("./tools/subfinder -d "+ domain +" -o temp_files/"+subfinder_output+ " | ./tools/httpx -l  temp_files/"+subfinder_output+" -o temp_files/"+httpx_output,shell=True)
         output = subprocess.check_output("cat temp_files/"+httpx_output, shell=True)
         subprocess.check_output("rm temp_files/" + httpx_output + " temp_files/"+subfinder_output, shell=True)
         return {
         "status" : "succsses",
         "urls":output,
             }



    except Exception as e:
        return {
         "status" : "Failed",
         "errortype":e.__str__(),
               }
  else:
      return {
          "status": "Failed",
          "errortype": "Invaild domain name",
      }