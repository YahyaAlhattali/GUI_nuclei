import subprocess
import validators
def sub(domain,current_user):
  if validators.domain(domain) == True:
    try:
         subprocess.check_output("rm sub.txt hxsub.txt | ./tools/subfinder -d "+ domain +" -o temp_files/sub.txt | ./tools/httpx -l  temp_files/sub.txt -o temp_files/hxsub.txt",shell=True)
         output = subprocess.check_output("cat temp_files/hxsub.txt", shell=True)
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