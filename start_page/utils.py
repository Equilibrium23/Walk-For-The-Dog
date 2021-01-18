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
