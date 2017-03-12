# FaceDetector

## Install
apt dependencies
```
sudo apt-get install python-pip cmake python-opencv python-tk python-imaging python-imaging-tk libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev libboost-all-dev
```

python dependencies
```
sudo pip2 install -r requirements.txt
```

install torch
```
git clone https://github.com/torch/distro.git ~/torch --recursive
cd ~/torch; bash install-deps;
./install.sh
```

install openface dependencies
```
sudo apt-get install luarocks
for NAME in dpnn nn optim optnet csvigo cutorch cunn fblualib torchx tds; do luarocks install $NAME; done
```

install openface
```
git clone https://github.com/cmusatyalab/openface/ ~/openface --recursive
cd ~/openface
sudo python2 setup.py install
bash models/get-models.sh
```

breath sigh of relief, well done!

## Use

Install

Run FaceDetector.py

Enable or disable different filters in the menu


## TODO

### CV2

Re-implement training as another layer

### Dlib

Implement training in Dlib

Train Dlib with other objects

* Eyes
* Hands
* Geometric shapes
* Other simple objects

#### Data sets

Hundreds of datasets
http://homepages.inf.ed.ac.uk/rbf/CVonline/Imagedbase.htm#face



