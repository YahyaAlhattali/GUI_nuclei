from functions import default_path
import subprocess
temp = default_path("test")
subprocess.check_output("cat " +temp , shell=True)


