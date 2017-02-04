# FaceDetector

## Install
```
sudo apt-get install python-opencv python-tk python-imaging python-imaging-tk libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev libboost-all-dev
sudo pip2 install -r requirements.txt
```

## Use

To enroll a new user: 
1. Run main and then click 'Enrol'
2. Enter a unique name for the user
3. Allow around 100 pictures to be taken
4. Press esc and allow training to run

Detecting faces
- Run real time test and check if the user's face is detected and the correct name is displayed

Counting movement
- Run counting_line
- Move the user's head up and down so that the central red dot crosses the line
