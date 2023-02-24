import json, datetime
from requests import get

def schedule(prname):
    raspis=''
    prname = prname.replace(' ', '%20', 1)
    req=get(f"https://raspi.ulspu.ru/json/dashboard/events?mode=teacher&value={prname}")
    rawsch = json.loads(req.text)
    for item in rawsch['data']:
        raspis=raspis+item['title']+' Время: '+str(datetime.datetime.strptime(item['start'], "%Y-%m-%dT%H:%M:%S.%fZ").time())[:-3]+' - '+str(datetime.datetime.strptime(item['end'], "%Y-%m-%dT%H:%M:%S.%fZ").time())[:-3]+'\n'
    return raspis