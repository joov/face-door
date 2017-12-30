# RPI for face / door detection

## Prerequisites

* Start with  [Razberry](http://razberry.z-wave.me/) imgage on rpi
* Enable ssh-daemon (e.g. using `raspi-config`)
* Camera for RPI (check with `raspstill -o <image.jpg>`)
* ZWave Door sensor (e.g. [Fibaro Door/Window Sensor](https://www.fibaro.com/de/products/door-window-sensor/) )

## Installation

Presuming you have an basic raspbian operating system (no graphical user interface, can be a fork like razberry) up and running, further installation is done by ansible. 

### Get Ansible running
If you have a linux system as installation server ready, install ansible and continue.
If you have a windows based sytstem as installation server, you have to get Ansible running in a virtualbox. 

Git-clone this repository and change to folder `ansible`.
### Get Ansible running in virtualbox 
   
* Install [VirtualBox](http://www.oracle.com/technetwork/server-storage/virtualbox/downloads/index.html) and [Vagrant](https://www.vagrantup.com/downloads.html), then say `Vagrant up` in the main directory and you will have a Ansible-VM
* ssh to Ansible VM (using port 2222 for vagrant, username/passwd is vagrant/vagrant)
* change to folder `/vagrant/ansible`

### Ansible-based installation
* Excecute ansible-playbook with command `ansible-playbook playbook.yml -i hosts --ask-pass`
* role pi does basic rpi installation. Please adapt:
    * hosts
    * wpa_supplicant.conf
    * wlan.yml
    
* role face installs [face-recoginition](https://github.com/ageitgey/face_recognition)


## Run Example
```python
cd ./face_recognition/examples
python3 facerec_on_raspberry_pi.py
```

## Ask Interface
* Get Data changes since epoch 1497675668: `wget --header="Accept: application/json" --auth-no-challenge --http-user=admin --http-password=password http://127.0.0.1:8083/ZWaveAPI/Data/1497675668`

## Links
* [Razberry](http://razberry.z-wave.me/)
* [face-recoginition](https://github.com/ageitgey/face_recognition)
* [Opencv and python](http://www.pyimagesearch.com/2015/06/01/home-surveillance-and-motion-detection-with-the-raspberry-pi-python-and-opencv/)
* [Face recognition](http://rpihome.blogspot.de/2015/03/face-detection-with-raspberry-pi.html)
* [dlib](https://github.com/davisking)
* [opencsv](https://github.com/Itseez/opencv)

