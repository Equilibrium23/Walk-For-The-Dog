from datetime import datetime

# def mergeTimes(data):
#     merged = {}
#     for person, info in data.items():
#         merged[person] = {}
#         for dog, datas in info.items():
#             merged[person][dog] = {}
#             temp={}
#             for date in datas:
#                 temp[date.day]=[]

#             for date in datas:
#                 temp[date.day].append((date.start_hour.strftime("%H:%M"), date.end_hour.strftime("%H:%M")))

#             for date, times in temp.items():
#                 result = []
#                 times.sort()
#                 t_old = times[0]
#                 for t in times[1:]:
#                     if t_old[1] >= t[0]:
#                         t_old = (min(t_old[0], t[0]), max(t_old[1], t[1]))
#                     else:
#                         result.append(t_old)
#                         t_old = t
#                 else:
#                     result.append(t_old)
                
#                 fixed_result=[]
#                 for t in result:
#                     fixed_result.append((datetime.strptime(t[0], '%H:%M').time(), datetime.strptime(t[1], '%H:%M').time()))

#                 merged[person][dog][date]=fixed_result

#     return merged

from register_and_login.models import Profile
from dog_editing.models import Dog
from time_management.models import TimePeriod
from users.models import Match

def get_helper_matches(request):
    helper_profile = Profile.objects.all().get(user = request.user)
    matches = Match.objects.all().filter(helper_id = helper_profile.id).filter( is_match_accepted = True )
    return_data = {}

    for match in matches:
        owner = Profile.objects.get(id = match.owner_id)
        dog = Dog.objects.get(id = match.dog_id)
        return_data[owner] = { dog: [] }

    for match in matches:
        owner = Profile.objects.get(id = match.owner_id)
        time = TimePeriod.objects.get( id = match.helper_time_period_id )
        dog = Dog.objects.get(id = match.dog_id)
        return_data[owner][dog].append(time)

    return return_data
