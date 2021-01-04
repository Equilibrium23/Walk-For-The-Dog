from datetime import datetime
from register_and_login.models import Dog, Profile, TimePeriod
from django.contrib.auth.models import User

def mergeTimes(data):
    #matched_helper (from Profile table) : { dog (from Dog table) : time for walk (from TimePeriod table)
    merged = {}
    for person, info in data.items():
        merged[person] = {}
        for dog, datas in info.items():
            merged[person][dog] = {}
            temp={}
            for date in datas:
                temp[date.day]=[]

            for date in datas:
                temp[date.day].append((date.start_hour.strftime("%H:%M"), date.end_hour.strftime("%H:%M")))

            for date, times in temp.items():
                result = []
                times.sort()
                t_old = times[0]
                for t in times[1:]:
                    if t_old[1] >= t[0]:
                        t_old = (min(t_old[0], t[0]), max(t_old[1], t[1]))
                    else:
                        result.append(t_old)
                        t_old = t
                else:
                    result.append(t_old)
                
                fixed_result=[]
                for t in result:
                    fixed_result.append((datetime.strptime(t[0], '%H:%M').time(), datetime.strptime(t[1], '%H:%M').time()))

                merged[person][dog][date]=fixed_result

    return merged