# RPI for face / door detection

## Prerequisites

* Start with  [Razberry](http://razberry.z-wave.me/) imgage on rpi
* Camera for RPI (check with `raspstill -o <image.jpg>`)
* ZWave Door sensor (e.g. [Fibaro Door/Window Sensor](https://www.fibaro.com/de/products/door-window-sensor/) )
* Ansible available to do deployment
#* Get a Dropbox API-key [here](https://www.dropbox.com/developers)

## Installation

* role pi does basic rpi installation. Please adapt:
    * hosts
    * wpa_supplicant.conf
    * wlan.yml
    
* role face installs [face-recoginition](https://github.com/ageitgey/face_recognition)


## Run
```python
cd ./face_recognition/examples
python3 facerec_on_raspberry_pi.py
```



## Links
* [Razberry](http://razberry.z-wave.me/)
* [face-recoginition](https://github.com/ageitgey/face_recognition)
* [Opencv and python](http://www.pyimagesearch.com/2015/06/01/home-surveillance-and-motion-detection-with-the-raspberry-pi-python-and-opencv/)
* [Face recognition](http://rpihome.blogspot.de/2015/03/face-detection-with-raspberry-pi.html)

