import time
from collections import OrderedDict

SAMPLES = 100
btime = 0
btimes = OrderedDict({})

def begin():
    global btime
    btime = time.time()

def end(label, do_print=True):
    t = (time.time() - btime) * 1000
    if do_print:
        print label[0:20] + "\t\t" + str(t)
    
    if label not in btimes:
        btimes[label] = []
    btimes[label].append(t)

def avg():
    avgs = []
    for key in btimes:
        avg = sum(btimes[key]) / SAMPLES
        print key[0:20] + "\t\t" + str(avg)
        avgs.append(avg)

    print "Total:\t\t\t\t" + str(sum(avgs))