GOOGLE_MAP_KEY = 'AIzaSyA108_naJOcONel1ZhwxrjhmVYDjiPU2Ps'
import urllib.request
import json

def check_location(location_A,location_B,helping_radius):
    url = '''https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins={}&destinations={}&key={}'''.format(location_A,location_B,GOOGLE_MAP_KEY)
    response = urllib.request.urlopen(url)
    result = json.loads(response.read())
    status = result['rows'][0]['elements'][0]['status']
    if status == 'OK':
        distance = [result['rows'][0]['elements'][0]['distance']['text'],{'m':result['rows'][0]['elements'][0]['distance']['value']}]
        print("location_A = {}, location_B = {} helping radius = {}, real_distance = {}".format(location_A,location_B,helping_radius,distance[1]['m']))
        with open("data.txt",'w') as file: # Use file to refer to the file object
            file.write(str(distance[1]['m']))
        # expected_time = [result['rows'][0]['elements'][0]['duration']['text'],{'s':result['rows'][0]['elements'][0]['duration']['value']}]
        return True if float(distance[1]['m']) <= float(helping_radius*1000) else False 
        