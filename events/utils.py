import datetime
import math
import re
import requests
from django.conf import settings


from django.utils.html import strip_tags


def count_words(html_string):
    # html_string = """
    # <h1>This is a title</h1>
    # """
    word_string = strip_tags(html_string)
    matching_words = re.findall(r'\w+', word_string)
    count = len(matching_words) #joincfe.com/projects/
    return count


def get_read_time(html_string):
    count = count_words(html_string)
    read_time_min = math.ceil(count/200.0) #assuming 200wpm reading
    # read_time_sec = read_time_min * 60
    # read_time = str(datetime.timedelta(seconds=read_time_sec))
    # read_time = str(datetime.timedelta(minutes=read_time_min))
    return int(read_time_min)

def today_name_in_short_form():
    today = datetime.date.today()
    return today.strftime("%a")

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
    
    return ip


class Ward:

    def format_location(self, latitude, longitude, location):
        ward = self.get_by_geo_location(latitude, longitude)

        return {
            'name': location,
            'coordinates': f'{latitude},{longitude}',
            'ward_id': ward['ward_id'] or None,
            'ward': ward['ward_name'] or None,
            'city_id': ward['city_id'] or None,
            'city': ward['city_name'] or None
        }

    def get_by_geo_location(self, latitude, longitude):
        url = settings.LOCATION_API_GATEWAY_URL + 'by-geo-coordinates'
        headers = {'Accept': 'application/json;version=1.0', 'Accept-Language': 'en'}
        payload = {'latitude': latitude, 'longitude': longitude}
        
        try:
            res = requests.get(url, params=payload, headers=headers, timeout=5)

            if res.status_code == 200:
                content = res.json()
                return content['data']
        except requests.exceptions.Timeout:
            return 'Server timeout'

        return

        



