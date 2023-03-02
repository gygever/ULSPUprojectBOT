import json, datetime
from requests import get

def schedule(prname, day):
    raspis=''
    prname = prname.replace(' ', '%20', 1)
    day = datetime.datetime.strptime(day, "%Y-%m-%d").date()
    req=get(f"https://raspi.ulspu.ru/json/dashboard/events?mode=teacher&value={prname}")
    rawsch = json.loads(req.text)
    for item in rawsch['data']:
        dayrspis = datetime.datetime.strptime(item['start'], "%Y-%m-%dT%H:%M:%S.%fZ").date()
        if day == dayrspis:
            startt = datetime.datetime.strptime(item['start'], "%Y-%m-%dT%H:%M:%S.%fZ").time()
            starttime = datetime.timedelta(hours=startt.hour, minutes=startt.minute, seconds=startt.second, microseconds=startt.microsecond) + datetime.timedelta(hours=4, minutes=0, seconds=0, microseconds=0)
            endt = datetime.datetime.strptime(item['end'], "%Y-%m-%dT%H:%M:%S.%fZ").time()
            endtime = datetime.timedelta(hours=endt.hour, minutes=endt.minute, seconds=endt.second, microseconds=endt.microsecond) + datetime.timedelta(hours=4, minutes=0, seconds=0, microseconds=0)
            raspis = raspis + item['title'] + ' Время: ' + str(starttime)[:-3] + '-' + str(endtime)[:-3] + '\n'
    if len(raspis) == 0:
        raspis = f'У {prname.replace("%20", " ")} нет в занятий в этот день.'
        return raspis
    else:
        return raspis