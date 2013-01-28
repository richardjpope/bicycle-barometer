The bicycle barometer consists of two parts:

1. A web app that does the hard work of looking up the weather and tube status, and reduces them down to a single number
2. The device (a Nandode microprocessor plus servo), which looks up the number from the web app and moves a servo.

## What you will need
 * A nanode http://shop.nanode.eu/shop/nanodes/nanode-gateway/
 * A USB to Serial TTL converter http://shop.nanode.eu/shop/product/programming-lead/ or  http://www.amazon.co.uk/gp/product/B00514ZCHQ/
 * A 5v servo like this http://www.amazon.co.uk/TowerPro-Micro-Small-Servo-Helicopter/dp/B008Q8Q06G/
 * A square picture frame ~ 10 cm x 10xm or simular for housing the barometer
 * A peice of paper or card to print the face (see device/design/dial.svg)
 * An ethernet cable

## Setting up the web componant

If you like you can skip this part and use the instance of the web app deployed at http://bicyclebarometer.oftcc.net (although it is hard coded to a particular tube line)

### Register for the Met Office DataPoint API
1. [Register](https://register.metoffice.gov.uk/WaveRegistrationClient/public/register.do?service=datapoint)
2. Make a note of the API key

### Setting up a local development copy
1. Install and setup virtualenv:

        $ easy_install virtualenv
        $ virtualenv .
2. Install requirements:

        $ pip install -r requirements.txt
3. Add the met office api key:

        $ export METOFFICE_DATAPOINT_KEY=ExAmPlEkEy
4. Run the app:

        $ python run web/app.py

### Deploying to heroku
1. Create an account on [heroku.com](http://heroku.com) and install the toolbelt https://toolbelt.heroku.com/
2. Create a new heroku instance

        $ heroku create
3. Deploy:

        $ git push heroku master
4. Add the met office api key

        $ heroku config:add METOFFICE_DATAPOINT_KEY=ExAmPlEkEy

## Programming the nanode
1. Install the [Arduino IDE app](http://arduino.cc/en/main/software)
2. Follow [these instructions](http://wiki.london.hackspace.org.uk/view/Project:Nanode/Applications) to get your Nanode up and running.
3. Find out the mac adress of your nanode and make a note of it. You need to [https://github.com/sde1000/NanodeUNIO](run a script) to do this.
4. Open the sketch device/nanode/bicyclebarometer.io in the Arduino IDE app
5. Edit the mac address
6. Edit the following line to point at the web app:
	char website[] PROGMEM = "http://bicyclebarometer.oftcc.net";
7. Attach the setvo to pin 9 and  on the Arduino
7. Upload the sketch to your Nanode



 