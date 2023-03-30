import json, datetime
from requests import get

def dayweek(day):
    day = datetime.datetime.strptime(day, "%Y-%m-%d").date()
    day=day.weekday()
    if day==0:
        return ' (понедельник)'
    elif day==1:
        return ' (вторник)'
    elif day==2:
        return ' (среда)'
    elif day==3:
        return ' (четверг)'
    elif day==4:
        return ' (пятница)'
    elif day==5:
        return ' (суббота)'
    elif day==6:
        return ' (воскресенье)'

def ListSchedule(prname, day):
    prname = prname.replace(' ', '%20')
    day = datetime.datetime.strptime(day, "%Y-%m-%d").date()
    req = get(f"https://raspi.ulspu.ru/json/dashboard/events?mode=teacher&value={prname}")
    rawsch = json.loads(req.text)
    rawraspis = []
    for item in rawsch['data']:
        dayrspis = datetime.datetime.strptime(item['start'], "%Y-%m-%dT%H:%M:%S.%fZ").date()
        if day == dayrspis:
            rawraspis.append(item)
    return sorted(rawraspis, key=lambda x: datetime.datetime.strptime(x['start'], "%Y-%m-%dT%H:%M:%S.%fZ").time())

def SplitTitle(rlist):
    for item in rlist:
        hlp1=item['title'].split(' - ')
        hlp2=hlp1[2].split(' (')
        hlp2[1]=hlp2[1].replace(')',' ')
        for i in hlp2:
            hlp1.append(i)
        hlp1.pop(2)
        item['title']=hlp1
    return rlist

def FormatTitle(rlist):
    rlist=SplitTitle((rlist))
    for item in rlist:
        item['title'] = '*Дисциплина:* '+ item['title'][0] + ' \n*Тип занятия:* '+ item['title'][1] + ' \n*Группа:*     ' + item['title'][2] + ' \n*Аудитория:* ' + item['title'][3]
    return rlist

def teacher(prname):
    req = get('https://raspi.ulspu.ru/json/dashboard/teachers')
    tecsp = json.loads(req.text)
    for item in tecsp['rows']:
        if prname in item:
            tecsp = None
            return item
    if tecsp:
        return None

def StrReversDate(date):
    date=date.split('.')
    date[0], date[2] = '20'+date[2], date[0]
    return date[0]+'-'+date[1]+'-'+date[2]

def DateReversdate(date):
    date = str(date)
    date = date.split('-')
    date[0], date[2] = date[2], date[0]
    return date[0] + '.' + date[1] + '.' + date[2]

def schedule(prname, day):
    prname = teacher(prname)
    if prname:
        if type(day) == str:
            raspis = 'Расписание на ' + day + ' ' + dayweek(StrReversDate(day)) + ':\n\n'
            rawraspis = ListSchedule(prname, StrReversDate(day))
        elif type(day) == datetime.date:
            raspis = 'Расписание на ' + DateReversdate(day) + ' ' + dayweek(str(day)) + ':\n\n'
            rawraspis = ListSchedule(prname, str(day))
        para = 1
        prodpara = datetime.timedelta(hours=1, minutes=30)
        lasttime = datetime.timedelta(hours=8, minutes=30)
        nopara = ''
        rawraspis = FormatTitle(rawraspis)
        for item in rawraspis:
            startt = datetime.datetime.strptime(item['start'], "%Y-%m-%dT%H:%M:%S.%fZ").time()
            starttime = datetime.timedelta(hours=startt.hour, minutes=startt.minute, seconds=startt.second, microseconds=startt.microsecond) + datetime.timedelta(hours=4, minutes=0, seconds=0, microseconds=0)
            endt = datetime.datetime.strptime(item['end'], "%Y-%m-%dT%H:%M:%S.%fZ").time()
            endtime = datetime.timedelta(hours=endt.hour, minutes=endt.minute, seconds=endt.second, microseconds=endt.microsecond) + datetime.timedelta(hours=4, minutes=0, seconds=0, microseconds=0)
            if starttime == lasttime:
                raspis = raspis + item['title'] + ' \n*Время:* ' + str(starttime)[:-3] + '-' + str(endtime)[:-3] + '\n \n'
            else:
                nopara = starttime - lasttime
                if nopara // prodpara > 4:
                    para = para + nopara // prodpara - 1
                else:
                    para = para + nopara // prodpara
                raspis = raspis + str(para) + ' пара \n' + item['title'] + ' \n*Время:* ' + str(starttime)[:-3] + '-' + str(
                    endtime)[:-3] + '\n \n'
                lasttime = starttime
        if len(raspis) <= 37:
            raspis = f'У {prname.replace("%20", " ")} нет в занятий в этот день.'
            return raspis
        else:
            return raspis
    else:
        return 'На данного преподавателя нет расписания. Убедитесь, что правильно ввели фамилию и инициалы преподавателя. '

def TodayRaspis(prname):
    day = datetime.datetime.today().date()
    return schedule(prname, day)

def TomorrowRaspis(prname):
    day = datetime.date.today() + datetime.timedelta(days=1)
    return schedule(prname, day)
