import urllib
import  pywapi
from xml.dom import minidom

def test():
    # print weather()
    print "Station open: " + str(station_open('Brixton'))
    print "Line status: " + line_status('Victoria')

def line_status(line_name):
    # returns 'Part Suspended', 'Severe Delays', 'Good Service', 'Disrupted Service', 'Planned Closure', 'Part Closure', 'Suspended'????

    line_status = 'Severe Delays'
    url = "http://cloud.tfl.gov.uk/TrackerNet/LineStatus"
    xml = minidom.parse(urllib.urlopen(url))
    for node in xml.getElementsByTagName('LineStatus'):
        if node.getElementsByTagName('Line')[0].getAttribute('Name') == line_name:
            line_status = node.getElementsByTagName('Status')[0].getAttribute('Description')
    return line_status

def station_open(station_name):

    station_open = False
    url = "http://cloud.tfl.gov.uk/TrackerNet/StationStatus"
    xml = minidom.parse(urllib.urlopen(url))
    for node in xml.getElementsByTagName('StationStatus'):
        if node.getElementsByTagName('Station')[0].getAttribute('Name') == station_name:
            if node.getElementsByTagName('Status')[0].getAttribute('Description') in('Open', 'No Step Free Access'):
                station_open = True
    return station_open
