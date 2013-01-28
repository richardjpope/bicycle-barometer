import json
import urllib
import os
from time import gmtime

def get_forcast():
    
    # get the forcast
    # http://www.metoffice.gov.uk/datapoint/product/uk-3hourly-site-specific-forecast/detailed-documentation
    key = os.environ['METOFFICE_DATAPOINT_KEY']
    url = "http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/353846?res=3hourly&key=" + key 
    forcast = json.load(urllib.urlopen(url))

    # sometimes returns old forcasts, so need to work out mins since midnight GMT and take best segment
    minutes_since_midnight_gmt = gmtime().tm_hour * 60
    latest_index = -1
    for rep in forcast['SiteRep']['DV']['Location']['Period'][0]['Rep']:
        if int(rep['$']) <= minutes_since_midnight_gmt:
            latest_index = latest_index + 1

    # grab the best forcast segment, then make the it make more sense by giving it some useful names        
    latest =  forcast['SiteRep']['DV']['Location']['Period'][0]['Rep'][latest_index]
    result =  {'Feels Like Temperature': latest['F'], 'Wind Gust': latest['G'], 'Visibility': latest['V'], 'Wind Speed': latest['S'], 'Weather Type': latest['W'], 'Precipitation Probability': latest['Pp'], 'Temperature': latest['T'],}

    return result