# This starts a web-server for face recognition

# To be used with zway home automation


import os, sys, time, re
lib_path = os.path.abspath(os.path.join('..','..','face_recognition'))
sys.path.append(lib_path)
import face_recognition
from picamera import PiCamera
import cv2
import numpy as np
from flask import Flask, jsonify, request, redirect
import threading

app = Flask(__name__)

is_recording = False
camera = PiCamera()
output = np.empty((240, 320, 3), dtype=np.uint8)
known_faces = {}
image_count=0


@app.route('/start', methods=['GET'])
def start_recording():
    global is_recording
    is_recording = True
    return 'Started'


@app.route('/stop', methods=['GET'])
def stop_recording():
    global is_recording
    is_recording = False
    return 'Stopped'

@app.route('/known', methods=['GET'])
def copy_known():
    return 'TBD'

def find_known_faces():
    global known_faces
    known_path = os.path.abspath(os.path.join('known'))

    # Load a sample picture and learn how to recognize it.
    print("Loading known face image(s) from {0}".format(known_path))

    for file in os.listdir(known_path):
        if not file.endswith('.jpg'):
            continue
        
        print("Path {}".format(known_path+'/'+file))
        try:
            image = face_recognition.load_image_file(known_path+'/'+file)

        except BaseException:
            print("Unexpected error:", sys.exc_info()[0])

        face_encoding = face_recognition.face_encodings(image)

        known_faces[file] = face_encoding
        

def get_image_count():
    global image_count
    unknown_path = os.path.abspath(os.path.join('unknown'))

    for file in os.listdir(unknown_path):
        if not file.endswith('.jpg'):
            continue
        
        num = int(re.findall(r'\d+',file)[0])
        if num > image_count:
            image_count = num+1

def write_image(img):
    global image_count
    unknown_path = os.path.abspath(os.path.join('unknown'))

    cv2.imwrite(unknown_path+'/'+str(image_count)+'.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

    image_count += 1


def init():
    # Get a reference to the Raspberry Pi camera.
    # If this fails, make sure you have a camera connected to the RPi and that you
    # enabled your camera in raspi-config and rebooted first.
    camera.resolution = (320, 240)

    # Load a sample picture and learn how to recognize it.
    # print("Loading known face image(s)")
    # obama_image = face_recognition.load_image_file("obama_small.jpg")
    # obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

    find_known_faces()
    get_image_count()


def do_record():
    global is_recording, known_faces, image_count, camera
    while True:
        if not is_recording:
            print("Sleeping")
            time.sleep(1)
            continue

        # Initialize some variables
        face_locations = []
        face_encodings = []

        print("Capturing image.")
        # Grab a single frame of video from the RPi camera as a numpy array
        camera.capture(output, format="bgr")
        
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(output)
        print("Found {} faces in image.".format(len(face_locations)))
        face_encodings = face_recognition.face_encodings(output, face_locations)

        # print("Writing image {}".format(count))
        # cv2.imwrite('/tmp/image_'+str(count)+'.jpg', output, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        # count+=1

        # Loop over each face found in the frame to see if it's someone we know.
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

            found_match = False
            for known in known_faces.keys():
                # See if the face is a match for the known face(s)
                match = face_recognition.compare_faces(known_faces[known], face_encoding)
                if match:
                    print("I see {}!".format(known))
                    found_match = True
                    break

            if found_match == False:
                print("Found unknown Image")
                img = output[top:bottom, left:right]
                write_image(img)
                # TODO: Send Image to Messenger


if __name__ == "__main__":
    init()
    is_recording = False
    t = threading.Thread(target=do_record)
    t.daemon = True
    t.start()

    app.run(host='0.0.0.0', port=5001, debug=False)
