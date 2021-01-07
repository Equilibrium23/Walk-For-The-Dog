import urllib.request
import json

GOOGLE_MAP_KEY = 'AIzaSyBBcPbX-93uzhQq9qQosN7TzVYGtr3cFpg'

def check_location(location_A,location_B,helping_radius):
    url = '''https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins={}&destinations={}&key={}'''.format(location_A,location_B,GOOGLE_MAP_KEY)
    response = urllib.request.urlopen(url)
    result = json.loads(response.read())
    status = result['rows'][0]['elements'][0]['status']
    if status == 'OK':
        distance = [result['rows'][0]['elements'][0]['distance']['text'],{'m':result['rows'][0]['elements'][0]['distance']['value']}]
        return True if float(distance[1]['m']) <= float(helping_radius*1000) else False 