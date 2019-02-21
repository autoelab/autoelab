import requests, ctypes, random, time, json, sys, re, os

version = '1.0.1'
ctypes.windll.kernel32.SetConsoleTitleW("autoelab")

def getquestion(questionno):
    global question 
    try:
        questionpage = session.get(quesurl + 'id={}&value={}'.format(level, questionno), headers=headers).text

    except:
        input('Error: Unable to access the question page.')
        sys.exit()

    try:
        questionid = re.search(r"(id=\"[0-9]{8,12}\")", questionpage).group(0)[4:-1]
        question = json.loads(requests.get(questiondb + questionid + '.json').text)

    except:
        qname = (re.search(r"(?<=Question Name:)(.*?)(?=\<)", questionpage).group(0)).replace(':','').replace('?','').strip()
        sname = (re.search(r"(?<=Session<)(.*?)(?=\<\/li>)", questionpage).group(0)[12:-1]).replace(':','').replace('?','').strip()
        question = json.loads(requests.get(questiondb + (sname + ' - ' + qname).replace(' ', '%20') + '.json').text)
        questionid = question['Q_ID']

    return(questionid)

def getanswers(questionid):
    global answers
    try: answers = json.loads(requests.get(answerdb + questionid + '.json').text)['files']
    except: return(False)
    else: return(True)

def alreadysolved():
    code = session.post(codeurl, headers=headers).text
    if len(code) > 3:
        codepayload = {'code':code,'input':''}
        if multilang:
            lang = 'cpp' if 'iostream' in code else 'c'
            codepayload['language'] = lang

        response = session.post(evalurl, data=codepayload, headers=headers).text
        result = json.loads(response)
        if result['error'] == 0 and result['score'] == 100: return(True)

def evaluate(questionid, answer):
    code = requests.get(answerdb + questionid + '/' + answer, 'r').text
    codepayload = {'code':code,'input':''}
    if multilang:
        lang = 'cpp' if 'iostream' in code else 'c'
        codepayload['language'] = lang

    response = session.post(evalurl, data=codepayload, headers=headers).text
    result = json.loads(response)
    if result['error'] == 0 and result['score'] == 100: return True

def reportgenerator(questionno):
    if not os.path.isdir('Reports'): os.mkdir('Reports')
    report = session.get(repourl, headers=headers)
    outfile = 'Reports\\{}.jpg'.format(str(questionno).rjust(2,'0'))
    open(outfile, 'wb').write(report.content)

def getskilltopic(skill):
    topic = skill
    if skill == 'ada': skill = 'daa'
    if skill == 'daa': topic = 'ada'
    return(skill, topic)

def login(username, password):
    loginpayload = {'userid': username,'password': password} 
    response = session.post(homeurl, data=loginpayload, headers=headers).text
    if response == '0':
        print('Invalid Username or Password')
        os.system('pause')
        sys.exit()

def getinput():

    global username, password, campuscode, department, skill, level, start, end, delay, generatereports

    username = config['username']
    if username == '': username = input('Username : ')

    password = config['password']
    if password == '': password = input('Password : ')

    campuscode = config['campuscode']
    if campuscode == '': campuscode = input('Campus (ktr|rmp|vdp) : ')

    department = config['department']
    if department == '': department = input('Department (cse|it) : ')

    skill = config['skill']
    if skill == '': skill = input('Skill (java|daa): ')

    level = config['level']
    if level == '': level = input('Level (1|2|3) : ')

    start = config['start']
    if start == '': start = input('Starting Question Number (0-99) : ')

    end = config['end']
    if end == '': end = input('Ending Question Number (0-99) : ')

    delay = config['delay']
    if delay == '': delay = '0'

    try: generatereports = config['generatereports']
    except: generatereports = False

    print()

def autoelab(username, password, campuscode, department, skill, level, start, end, delay, generatereports=False):

    global homeurl, codeurl, repourl, quesurl, evalurl, session, headers, multilang, questiondb, answerdb, questiondb, answerdb
    skill, topic = getskilltopic(skill)
    if skill in ['daa']: multilang = True
    else: multilang = False

    questiondb = 'https://raw.githubusercontent.com/autoelab/autoelab/master/data/' + skill + '_question_table/'
    answerdb = 'https://raw.githubusercontent.com/autoelab/autoelab/master/data/code/'  + skill + '/'

    homeurl = 'http://care.srmuniv.ac.in/{}{}{}/index.helper.php'.format(campuscode, department, topic)
    codeurl = 'http://care.srmuniv.ac.in/{}{}{}/login/studentnew/code/code.get.php'.format(campuscode, department, topic)
    repourl = 'http://care.srmuniv.ac.in/{}{}{}/login/studentnew/code/getReport.php'.format(campuscode, department, topic)
    quesurl = 'http://care.srmuniv.ac.in/{}{}{}/login/studentnew/code/{}/{}.code.php?'.format(campuscode, department, topic, skill, skill)
    evalurl = 'http://care.srmuniv.ac.in/{}{}{}/login/studentnew/code/{}/code.evaluate.elab.php'.format(campuscode, department, topic, skill)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    with requests.Session() as session:

        login(username, password)

        for questionno in range(start, end + 1):

            questionid = getquestion(questionno)

            if alreadysolved():
                print(str(questionno).rjust(2,'0') + ' - ' + question['Q_NAME'] + ' - Skipped')
                if generatereports: reportgenerator(questionno)
                continue

            else:
                print(str(questionno).rjust(2,'0') + ' - ' + question['Q_NAME'], end = '')
               
            if not getanswers(questionid):
                print(' - Failed')
                continue

            solved = False
            for answer in answers:
                if evaluate(questionid, answer):
                    solved = True
                    break

            if solved == False:
                print(' - Failed')
            
            else:
                print(' - Solved')
                if generatereports: reportgenerator(questionno)
                if not delay == 0:
                    totaldelay = delay + random.randint(1,5)
                    for t in range(totaldelay):
                        print('> Delay: {} minutes'.format(totaldelay - t))
                        time.sleep(60)

    input('\nAll done! Press Enter to exit.')
    sys.exit()

update = json.loads(requests.get('https://raw.githubusercontent.com/autoelab/autoelab/master/updater.json').text)
if not version == update['version']:
    input('An update is available! Get it from this link\n' + 'https://github.com/autoelab/autoelab/releases\n\nChangelog:\n' + 
        str(update['changes'])[1:-1].replace(", ","\n").replace("'","") + '\n\n')

if len(sys.argv) == 10:
    cdir, username, password, campuscode, department, skill, level, start, end, delay = sys.argv
    generatereports = False

elif not os.path.isfile('config.json'):
    sample = json.loads(requests.get('https://raw.githubusercontent.com/autoelab/autoelab/master/sampleconfig.json').text)
    with open('config.json', 'w') as f: json.dump(sample, f, indent=4)
    input(
        'Welcome! A sample config.json file has been created.\n' + 
        'Edit it, and fill the required information in there.\n' + 
        'Check https://github.com/autoelab/autoelab for help.\n' +
        'Press Enter to continue.\n')

with open('config.json', 'r') as f: config = json.load(f)
getinput()

autoelab(username, password, campuscode, department, skill, int(level), int(start), int(end), int(delay), generatereports)