# RPI for face / door detection

## Prerequisites

* Starten mit hypriot-image (später dann [Razberry](http://razberry.z-wave.me/) )
* Prereq: Camera module available (check with `raspstill -o <image.jpg>`)
* Get a Dropbox API-key [here](https://www.dropbox.com/developers)

## Installation


```sh
apt-get update
sudo apt-get install libopencv-dev python-opencv python-dev
sudo apt-get install python-picamera
sudp apt-get python-dev
sudo apt-get python-pip
sudo pip install imutils
sudo pip install dropbox
```

## Configuration

* Edit conf.json
* Don't enter Dropbox-secret in conf.json but set env-variable `DROPBOX_SECRET`
* Enter Dropbox Access Token to env-variable `DROPBOX_ACCESSTOKEN`


## Links
* [Opencv and python](http://www.pyimagesearch.com/2015/06/01/home-surveillance-and-motion-detection-with-the-raspberry-pi-python-and-opencv/)
* [Face recognition](http://rpihome.blogspot.de/2015/03/face-detection-with-raspberry-pi.html)
