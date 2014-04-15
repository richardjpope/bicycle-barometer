import os
from flask import Flask
from flask import render_template
from flask import request
from helpers.tube import line_status, station_open
from helpers.metoffice import get_forcast
app = Flask(__name__)
app.debug = True

def get_value(station, line):
    result = 100

    forcast =  get_forcast()

    print "Feels Like Temperature: %s" % forcast['Feels Like Temperature']
    print "Weather Type: %s" % forcast['Weather Type']
    print "Wind Speed: %s" % forcast['Wind Speed']
    print "Line status: %s" % line_status(line)

    #0 remove points for cold
    if int(forcast['Feels Like Temperature']) <= 15 and int(forcast['Feels Like Temperature']) > 5:
        print "Removing 15 points because temperature > 5 and <= 15"
        result = result - 10

    if int(forcast['Feels Like Temperature']) <= 5 and int(forcast['Feels Like Temperature']) > 0:
        print "Removing 25 points because temperature > 0 and <= 5"
        result = result - 15

    if int(forcast['Feels Like Temperature']) <= 0:
        print "Removing 50 points because temperature < 0"
        result = result - 45

    # 1) remove points for cycling based on different weather conditions (http://www.metoffice.gov.uk/datapoint/support/code-definitions)


    if int(forcast['Weather Type']) in (9, 10, 11, 12):
        print "Removing 30 points for weather type"
        result = result - 30

    if int(forcast['Weather Type']) in (13, 14, 15,):
        print "Removing 45 points for weather type"
        result = result - 45

    if int(forcast['Weather Type']) in (16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30):
        print "Removing 75 points for weather type"
        result = result - 75

    #2)  remove points for wind
    if int(forcast['Wind Speed']) > 10 and int(forcast['Wind Speed']) <= 15:
        result = result - 10

    if int(forcast['Wind Speed']) > 15 and int(forcast['Wind Speed']) <= 25:
        print "Removing 20 points because wind speed > 15 and < 25"
        result = result - 20

    if int(forcast['Wind Speed']) > 25:
        print "Removing 35 points because wind speed > 25"
        result = result - 35

    #3)  add points for cycling based on status of line
    if line_status(line) != 'Good Service':
        print "Adding 35 points tube line not running well"
        result = result + 35

    #4) if station shut, need to get on a bike whatever the weather
    if not station_open(station):
        print "Forced 100 as station is shut"
        result = 100

    #make sure value is between 0 and 100
    if result > 100:
        result = 100
    if result < 0:
        result = 0

    return result

@app.route("/")
def index():
    station = request.args.get('station') or "Brixton"
    line = request.args.get('line') or "Victoria"
    value = 100 - get_value(station, line)
    return render_template('index.html', value=value)

@app.route("/api")
def api():
    station = request.args.get('station') or "Brixton"
    line = request.args.get('line') or "Victoria"
    value = get_value(station, line)
    return render_template('api.html', value=value)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
