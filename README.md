## Introduction

The bicycle barometer takes data about the weather, the status of tube lines and stations and displays a value on a dial. [More info and a video here](http://blog.oftcc.net/post/39219681688/the-bicycle-barometer-takes-data-about-the).

Note: this code is a very scrappy minimum viable product, but I'm releasing it early as there has been lots of interest. There is a long todo list on the github issue tracker for this repo, feel free to fork and get involved.

The instructions here are for a Nanode, hopefully someone will get it working for an Arduino + ethernet shield and submit a pull request.

The code currently only works for UK weather and the London Tube system, Hopefully people will add wider coverage of transit systems and countries.

The bicycle barometer consists of two parts:

1. A web app that does the hard work of looking up the weather and tube status, and reduces them down to a single number
2. The device (a Nanode microprocessor plus servo), which looks up the number from the web app and moves a servo.

## What you will need
 * A nanode http://shop.nanode.eu/shop/nanodes/nanode-gateway/
 * A USB to Serial TTL converter http://shop.nanode.eu/shop/product/programming-lead/ or  http://www.amazon.co.uk/gp/product/B00514ZCHQ/
 * A 5v servo like this http://www.amazon.co.uk/TowerPro-Micro-Small-Servo-Helicopter/dp/B008Q8Q06G/
 * A square picture frame ~ 10 cm x 10xm or similar for housing the barometer
 * A piece of paper or card to print the face (see device/design/dial.svg)
 * An ethernet cable

## Setting up the web component

If you like you can skip this part and use the instance of the web app deployed at http://bicyclebarometer.oftcc.net (although it is hard coded to a particular tube line)

### Register for the Met Office DataPoint API
1. [Register](https://register.metoffice.gov.uk/WaveRegistrationClient/public/register.do?service=datapoint)
2. Make a note of the API key

### Setting up a local development copy
1. Install and setup virtualenv:

        $ easy_install virtualenv
        $ virtualenv .
        $ source bin/activate
2. Install requirements:

        $ pip install -r requirements.txt
3. Add the met office api key:

        $ export METOFFICE_DATAPOINT_KEY=ExAmPlEkEy
4. Run the app:

        $ python web/app.py

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
3. Find out the mac address of your nanode and make a note of it. You need to [run a script](https://github.com/sde1000/NanodeUNIO) to do this.
4. Open the sketch device/nanode/bicyclebarometer.io in the Arduino IDE app
5. Edit the mac address
6. Edit the following line to point at the web app:
	char website[] PROGMEM = "http://bicyclebarometer.oftcc.net";
7. Attach the servo to pin 9 and on the Arduino
7. Upload the sketch to your Nanode



 