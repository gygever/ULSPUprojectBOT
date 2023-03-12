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

def schedule(prname, day):
    prname = prname.replace(' ', '%20', 1)
    raspis = 'Расписание на ' + day + dayweek(day) + ':\n'
    day=datetime.datetime.strptime(day, "%Y-%m-%d").date()
    req=get(f"https://raspi.ulspu.ru/json/dashboard/events?mode=teacher&value={prname}")
    rawsch = json.loads(req.text)
    rawraspis = []
    para = 1
    prodpara = datetime.timedelta(hours=1, minutes=30)
    lasttime = datetime.timedelta(hours=8, minutes=30)
    nopara = ''
    for item in rawsch['data']:
        dayrspis = datetime.datetime.strptime(item['start'], "%Y-%m-%dT%H:%M:%S.%fZ").date()
        if day == dayrspis:
            rawraspis.append(item)
    rawraspis = sorted(rawraspis, key=lambda x: datetime.datetime.strptime(x['start'], "%Y-%m-%dT%H:%M:%S.%fZ").time())
    for item in rawraspis:
        startt = datetime.datetime.strptime(item['start'], "%Y-%m-%dT%H:%M:%S.%fZ").time()
        starttime = datetime.timedelta(hours=startt.hour, minutes=startt.minute, seconds=startt.second, microseconds=startt.microsecond) + datetime.timedelta(hours=4, minutes=0, seconds=0, microseconds=0)
        endt = datetime.datetime.strptime(item['end'], "%Y-%m-%dT%H:%M:%S.%fZ").time()
        endtime = datetime.timedelta(hours=endt.hour, minutes=endt.minute, seconds=endt.second, microseconds=endt.microsecond) + datetime.timedelta(hours=4, minutes=0, seconds=0, microseconds=0)
        if starttime == lasttime:
            raspis = raspis + item['title'] + ' Время: ' + str(starttime)[:-3] + '-' + str(endtime)[:-3] + '\n'
        else:
            nopara = starttime - lasttime
            if nopara // prodpara > 4:
                para = para + nopara // prodpara - 1
            else:
                para = para + nopara // prodpara
            raspis = raspis + str(para) + ' пара \n' + item['title'] + ' Время: ' + str(starttime)[:-3] + '-' + str(
                endtime)[:-3] + '\n'
            lasttime = starttime
    if len(raspis) <= 40:
        raspis = f'У {prname.replace("%20", " ")} нет в занятий в этот день.'
        return raspis
    else:
        return raspis