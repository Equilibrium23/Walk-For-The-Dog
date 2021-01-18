from .googleMapsUtils import check_location
from register_and_login.models import Profile
from dog_editing.models import Dog
from time_management.models import TimePeriod, DogTime
from .models import Match

def check_dog_size(temp_user_dogs, helper_max_size_dog):
    size_values = {'S':1,'M':2,'B':3}
    match = False
    matched_dogs = []
    for temp_user_dog in temp_user_dogs:
        dog_object = Dog.objects.get( id = temp_user_dog.dog_id )
        if size_values[ dog_object.size ] <= size_values[helper_max_size_dog]:
            matched_dogs.append(temp_user_dog)
            match = True
    return  ( matched_dogs, match )

def check_time(helper, dogs):
    helper_time_period = TimePeriod.objects.all().filter( person_id = helper.user_id ).filter(time_type = 'F')
    matched_dogs_and_time = {Dog.objects.get( id = dog.dog_id ):[] for dog in dogs}
    match = False
    for dog in dogs:
        dog_time_period = TimePeriod.objects.get( id = dog.time_period_id )
        for helper_time in helper_time_period:
            if (helper_time.day == dog_time_period.day) and (helper_time.start_hour == dog_time_period.start_hour ) and (helper_time.end_hour == dog_time_period.end_hour):
                matched_dogs_and_time[Dog.objects.get( id = dog.dog_id )].append(dog_time_period)
                match = True
    return (matched_dogs_and_time,match)

def saveMatch(matchData):
    for user,dog_and_time in matchData.items():
        for dog,time_periods in dog_and_time.items():
            for time in time_periods:
                helper_time = TimePeriod.objects.all().filter( person_id = user.user_id ).filter(day = time.day).filter(start_hour = time.start_hour)
                helper_time_id = helper_time[0].id
                try:
                    Match(dog_id = dog.id , owner_time_period_id = time.id , owner_id = dog.owner_id , helper_time_period_id = helper_time_id, helper_id = user.id ).save()
                except:
                    pass
    
def matchUsers(request):
    temp_user = Profile.objects.all().filter(user = request.user)
    temp_user_dogs_need_walk = DogTime.objects.all().filter(owner_id = temp_user[0].id).filter(match = False)
    helpers = Profile.objects.all().filter(account_type='H')
    #####################################################################################################################
    #match temp user with helpers by dog size
    dict_of_helpers_dog_size = {} # { matched_helper : list of dogs which helper can walk with (from DogTime table) }
    for helper in helpers:
        match_by_dog_size = check_dog_size(temp_user_dogs_need_walk, helper.max_dog_size)
        if match_by_dog_size[1] == True:
            dict_of_helpers_dog_size[helper] = match_by_dog_size[0]
    #####################################################################################################################
    #match temp user with helpers by time
    dict_of_helpers_time = {} # { matched_helper (from Profile table) : { dog (from Dog table) : time for walk (from TimePeriod table) }
    for helper, dogs in dict_of_helpers_dog_size.items():
        match_by_time = check_time(helper, dogs)
        if match_by_time[1] == True:
            dict_of_helpers_time[helper] = match_by_time[0]
    #####################################################################################################################
    #match temp user with helpers by distance 
    list_of_helpers_distance = { helper:data for helper,data in dict_of_helpers_time.items() if check_location( temp_user[0].location, helper.location, helper.helping_radius) }
    saveMatch(list_of_helpers_distance)

def getMatches(request):
    owner = Profile.objects.get(user = request.user)
    matches = Match.objects.all().filter( owner_id = owner.id ).filter(is_match_accepted = False)
    return_data = {}
    for match in matches:
        helper = Profile.objects.get(id = match.helper_id)
        return_data[helper] = {}

    for match in matches:
        helper = Profile.objects.get(id = match.helper_id)
        dog = Dog.objects.get(id = match.dog_id)
        return_data[helper].update({dog:[]})

    for match in matches:
        helper = Profile.objects.get(id = match.helper_id)
        time = TimePeriod.objects.get( id = match.owner_time_period_id )
        dog = Dog.objects.get(id = match.dog_id)
        return_data[helper][dog].append(time)
    return return_data