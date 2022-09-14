import subprocess,os,functions,math,time





# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
def run_nuclei(conf,user):
    from packages_dir import crud
    from pathlib import Path
    from packages_dir.database import engine, SessionLocal
    from sqlalchemy.orm import Session
    from packages_dir import database
    import users
    from fastapi import Depends, FastAPI, HTTPException, status, Request
    db = Session(Depends(users.get_db))


    #print(db)
    urlsList = "./temp_files/" + functions.makefilename(conf.scan_name) + ".txt"
    selected_tmp = "./temp_files/" + functions.makefilename(conf.scan_name) + "selected.txt"
    results = "./temp_files/" + functions.makefilename(conf.scan_name) + "results.txt"

    severtys = str(conf.severty).replace("[", '').replace("]", '').replace("'", '').replace(" ", '')

    for ts in conf.templates:
        if ts == 'None':
            temps = functions.default_path(conf.scan_name, severtys)
            templates = f'./temp_files/{temps[0]}'
            total = temps[1]
            #print(f'Hello {templates}')
            tsp = 'D'
            break
        else:
            tsp = 'S'
            subprocess.check_output("echo " + ts + " >>" + selected_tmp, shell=True)

    if tsp == 'D':
        tsp = templates

    else:
        if tsp == 'S':
            tsp = selected_tmp
            templates = os.popen(f'wc -l < {selected_tmp}').read()
            total = templates.replace("\n", '')
            print(total)

    for domain in conf.domains:  # Adding targets to file to be readed later
        subprocess.check_output("echo " + domain + " >>" + urlsList, shell=True)

    fetch_temp = open(tsp, "rt")
    scan_db = crud.add_scan(conf, user)
    for index, line in enumerate(fetch_temp):

        cmd = f'./tools/nuclei -duc -l {urlsList} -t {line.strip()} -json -o {results}'
        progress = ((index + 1) / int(total)) * 100
        bar = math.trunc(int(progress))
        print(f'{bar}%')
        os.system(cmd)
        if Path(results).is_file():
            crud.vulns_to_db(results, scan_db.id)  # Pass Results to database

        time.sleep(conf.time_delay)
        crud.update_scan_progress(scan_db.id, bar)

    # clear temp files
    subprocess.check_output(f'rm {urlsList} {tsp}', shell=True)


#subprocess.check_output("rm -f ./temp_files/urlsScan.txt", shell=True)
#subprocess.check_output("cat ./temp_files/selected_temps.txt", shell=True)

      #./nuclei -u https://sfzco.com -t /home/ya7ya/nuclei-templates/exposures/backups/zip-backup-files.yaml -json -o test.txt

# As a first domain name make directory with random numbers for storing selected templates temporary