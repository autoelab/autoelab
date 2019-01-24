import shutil, json, os

skills = ['daa']

for skill in skills:

    jsonfolder = skill + '_question_table\\'
    jsonfiles = os.listdir(jsonfolder)
    
    for jsonfile in jsonfiles:

        with open(jsonfolder + jsonfile) as f:
            question = json.load(f)
    
        sname = (question['S_NAME']).replace(':','').replace('?','').strip()
        qname = (question['Q_NAME']).replace(':','').replace('?','').strip()
        
        try:
            os.rename(jsonfolder + jsonfile, jsonfolder + sname  + ' - ' + qname + '.json')
        except:
            print(jsonfile)
            pass