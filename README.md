# dmway

## What is it ?

<img src="./img/dmway2.png?raw=true" width="265" height="159">

d for dynamic, m for mapping and way from gateway.

The objective of this project is to develop an application that links a network of sensors and Thingsboard.
This application includes :
- checking the format of the data received by the sensors
- data persistence
- the creation of sensors on Thingsboard
- the provision of data on Thingsboard

This approach is a direct alternative to Thingsboard Gateway, offering a more generic view by providing dynamic mapping.

Here is how dmway fits into our network architecture :

<img src="./img/Zolertia-DMWAY-Thingsboard.jpg?raw=true">

If you want a lower-level view to understand how dmway works, a [flowchart](https://github.com/martindenion/dmway/wiki/dmway-flowchart) is available.

## Getting started

### OS tested

* Raspbian Strech (desktop and lite version)
* Raspbian Buster (desktop and lite version)

### Prerequisites

#### Thingsboard

First, you must have Thingsboard platform running.

If not, you can follow the [Thingsboard installation guides](https://thingsboard.io/docs/guides/#AnchorIDInstallationGuides).

#### Eclipse Mosquitto

You can install a MQTT broker locally or use a MQTT broker on the cloud.

These following way use a local Mosquitto broker but you can use your own MQTT broker.

```
$ sudo apt update
$ sudo apt install -y mosquitto mosquitto-clients
```

#### Git tool

You may also need to install the git tool for cloning the dmway project from Github :

```
$ sudo apt install -y git
```

#### Python package

dmway requires at least Python 3.5 version so you don't need to upgrade Python to a newer version : 

```
$ sudo apt install -y python3.5 python3-pip
```

### Cloning dmway

Clone the dmway source code and install dmway dependancies : 
```
$ git clone https://github.com/martindenion/dmway.git
$ cd dmway
$ sudo pip3 install -r requirements.txt
```

### Running dmway 

To run dmway, 3 methods are possible depending on the needs : 

#### For development 

Then, you can execute the app.py Python file :
```
$ cd dmway
$ python3 app.py
Output: 
Connecting to SQLite database ...
Connected to SQLite database 2.6.0
Connected with result code 0
```
dmway is now waiting for receiving JSON data by MQTT.

#### For deployment with systemd

```
$ cd dmway
$ chmod +x make_service.sh
$ sudo ./make_service.sh 'dmway' '/home/pi/dmway/app.py' 'dmway.service' yes
```
dmway is now waiting for receiving JSON data by MQTT.

#### For deployment with Docker

*TO DO*

### Quick start test

#### Publish json_message with local MQTT broker

Considering this [format](https://github.com/martindenion/dmway/wiki/JSON-message-and-topic-format), execute the following command line :

```
$ mosquitto_pub -h localhost -m "json_message" -t "topic"
```

Note : if you ran dmway using the development way, execute this previous command line from another duplicated shell to let dmway running correctly.

In order to better understand what does this command in the dmway context, see this [diagram](https://github.com/martindenion/dmway/wiki/Pub-and-Sub-command-around-dmway).

## Sources

* https://thingsboard.io/docs/iot-gateway/what-is-iot-gateway/
* https://www.startupbootcamp.org/startups/zolertia/
* https://obrienlabs.net/how-to-setup-your-own-mqtt-broker/
