# dmway

## Presentation

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

## Getting started

### OS tested

* Raspbian Strech (desktop and lite version)
* Raspbian Buster (desktop and lite version)

### Prerequisites

#### Thingsboard

First, you must have Thingsboard platform running.

If not, you can follow the Thingsboard installation guides : https://thingsboard.io/docs/guides/#AnchorIDInstallationGuides

#### Git tool

You may also need to install the git tool for cloning the dmway project from Github :

```
$ sudo apt install -y git
```

#### Python package

dmway requires at least Python 3.5 version so you don't need to upgrade Python to a newer version : 

```
$ sudo apt update
$ sudo apt install -y python3.5 python3-pip
```

#### Python dependancies

```
$ pip3 install -r requirements.txt
```

#### Eclipse Mosquitto

You can install a MQTT broker locally or use a MQTT broker on the cloud.
These follwing two ways are using Mosquitto broker but you can use your own MQTT broker.

##### Local MQTT broker

```
$ sudo apt install -y mosquitto mosquitto-clients
```

##### Cloud MQTT broker

```
$ sudo apt install -y mosquitto-clients
```

### Running dmway

Clone the dmway source code and execute the app.py Python file :
```
$ git clone https://github.com/martindenion/dmway.git
$ cd dmway
$ python3 app.py
Output: 
Connecting to SQLite database ...
Connected to SQLite database 2.6.0
Connected with result code 0
```

dmway is now waiting for receiving JSON data by MQTT.

### Test and configuration

#### Format of the message to send

Your JSON message must contain at least these three fields :
* mac
* device
* type

It can also contain these following fields :
* temperature
* humidity
* pressure
* luminosity
* loudness
* gas
* iaq

Example of json_message : 
```
{"mac":"00:12:4b:00:18:d6:f8:9e","device":"zolertia00:12:4b:00:18:d6:f8:9e","type":"remote","ts":1483228800000,"loudness":3228,"luminosity":212,"temperature":24,"humidity":27,"pressure":9899}
```
#### Format of the topic

To publish from your shell, you can replace '+' with what you want.  

Example of topic : 
```
/dev/temperature/data
```

For the moment, dmway subscribes to all topics in the following format  : 
```
/dev/+/data
```

#### With local MQTT broker

Execute the following command line :
```
$ mosquitto_pub -h localhost -m "json_message" -t "/dev/+/data"
```

The following diagram describes the MQTT publish and subscribe command around dmway with a local Mosquitto Broker :

<img src="./img/pubandsubdmway2.jpg?raw=true">

#### With cloud MQTT broker

Execute the following command line :

```
$ mosquitto_pub -h test.mosquitto.org -m "json_message" -t "/dev/+/data"
```
The following diagram describes the MQTT publish and subscribe command around dmway with a cloud Mosquitto Broker :

<img src="./img/cloudbroker.jpg?raw=true">

## Sources

* https://thingsboard.io/docs/iot-gateway/what-is-iot-gateway/
* https://www.startupbootcamp.org/startups/zolertia/
* https://obrienlabs.net/how-to-setup-your-own-mqtt-broker/
