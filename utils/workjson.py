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


def list_schedule(prname, day):
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


def split_title(rlist):
    for item in rlist:
        hlp1=item['title'].split(' - ')
        hlp2=hlp1[2].split(' (')
        hlp2[1]=hlp2[1].replace(')',' ')
        for i in hlp2:
            hlp1.append(i)
        hlp1.pop(2)
        item['title']=hlp1
    return rlist


def format_tTitle(rlist):
    rlist=split_title((rlist))
    for item in rlist:
        item['title'] = '*Дисциплина:* '+ item['title'][0] + ' \n*Тип занятия:* '+ item['title'][1] + ' \n*Группа:* ' + item['title'][2] + ' \n*Аудитория:* ' + item['title'][3]
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


def str_revers_date(date):
    date=date.split('.')
    date[0], date[2] = '20'+date[2], date[0]
    return date[0]+'-'+date[1]+'-'+date[2]


def date_revers_date(date):
    date = str(date)
    date = date.split('-')
    date[0], date[2] = date[2], date[0]
    return date[0] + '.' + date[1] + '.' + date[2]


def schedule(prname, day):
    if type(day) == str:
        raspis = ['*Расписание на ' + day + ' ' + dayweek(str_revers_date(day)) + ':*\n\n']
        rawraspis = list_schedule(prname, str_revers_date(day))
        date = str_revers_date(day)
    elif type(day) == datetime.date:
        raspis = ['*Расписание на ' + date_revers_date(day) + ' ' + dayweek(str(day)) + ':*\n\n']
        rawraspis = list_schedule(prname, str(day))
        date = str(day)
        day = date_revers_date(day)
    para = 1
    prodpara = datetime.timedelta(hours=1, minutes=30)
    lasttime = datetime.timedelta(hours=8, minutes=30)
    nopara = ''
    rawraspis = format_tTitle(rawraspis)
    for item in rawraspis:
        startt = datetime.datetime.strptime(item['start'], "%Y-%m-%dT%H:%M:%S.%fZ").time()
        starttime = datetime.timedelta(hours=startt.hour, minutes=startt.minute, seconds=startt.second, microseconds=startt.microsecond) + datetime.timedelta(hours=4, minutes=0, seconds=0, microseconds=0)
        endt = datetime.datetime.strptime(item['end'], "%Y-%m-%dT%H:%M:%S.%fZ").time()
        endtime = datetime.timedelta(hours=endt.hour, minutes=endt.minute, seconds=endt.second, microseconds=endt.microsecond) + datetime.timedelta(hours=4, minutes=0, seconds=0, microseconds=0)
        if starttime == lasttime:
            raspis.append(item['title'] + ' \n*Время:* ' + str(starttime)[:-3] + '-' + str(endtime)[:-3] + '\n \n')
        else:
            nopara = starttime - lasttime
            if nopara // prodpara > 4:
                para = para + nopara // prodpara - 1
            else:
                para = para + nopara // prodpara
            raspis.append('*'+str(para) + ' пара* \n' + item['title'] + ' \n*Время:* ' + str(starttime)[:-3] + '-' + str(endtime)[:-3] + '\n \n')
            lasttime = starttime
    if len(raspis) <= 1:
        return [f'У {prname.replace("%20", " ")} нет в занятий в {day}{dayweek(date)}\n\n']
    else:
        return raspis


def today_raspis(prname):
    day = datetime.datetime.today().date()
    return schedule(prname, day)


def tomorrow_raspis(prname):
    day = datetime.date.today() + datetime.timedelta(days=1)
    return schedule(prname, day)


def week_date_list(nweek, nyear):
    nweek = str(nyear)+'-W'+str(nweek)
    weekDay = datetime.datetime.strptime(nweek + '-1', "%Y-W%W-%w").date()
    weekList = [weekDay]
    for i in range(1, 6):
        weekDay += datetime.timedelta(days=1)
        weekList.append(weekDay)
    return weekList


def this_week():
    return [datetime.datetime.today().isocalendar()[0], datetime.datetime.today().isocalendar()[1]]


def this_week_schedule(prname):
    raspis = []
    week = week_date_list(this_week()[1], this_week()[0])
    for i in week:
        for x in schedule(prname, i):
            raspis.append(x)
    return raspis


def next_week():
    return [(datetime.datetime.today()+datetime.timedelta(weeks=1)).isocalendar()[0], (datetime.datetime.today()+datetime.timedelta(weeks=1)).isocalendar()[1]]


def next_week_schedule(prname):
    raspis = []
    week = week_date_list(next_week()[1], next_week()[0])
    for i in week:
        for x in schedule(prname, i):
            raspis.append(x)
    return raspis