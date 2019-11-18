# dmway

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

### Prerequisites

#### OS requirements

* Raspbian Strech (desktop and lite version)
* Raspbian Buster (desktop and lite version)

#### Packages requirements

dmway requires at least Python 3.5 version so you don't need to upgrade Python to a newer version.

You need to install the following package only if your OS is Raspbian Strech :
##### Python package

```
$ sudo apt update
$ sudo apt install -y python3-pip
```

Install this package to allow dmway to publish and subscribe by MQTT :
##### Eclipse Paho MQTT Python client library

```
$ pip3 install paho-mqtt
```

You may also need to install the git tool for cloning the dmway project from Github :

##### Git tool

```
$ sudo apt install -y git
```

### dmway installation

```
$ git clone https://github.com/martindenion/dmway.git
```

## Sources

* https://thingsboard.io/docs/iot-gateway/what-is-iot-gateway/
* https://www.startupbootcamp.org/startups/zolertia/
