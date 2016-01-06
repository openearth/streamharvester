from __future__ import absolute_import

import datetime
import subprocess

import matplotlib.pyplot as plt
import livestreamer
import dateutil
import cv2


from streamharvester.app import app
from streamharvester.capture import get_capture_from_livestream
from streamharvester.conventions import generate_filename
from streamharvester.utils import TimeoutSubprocess

@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)

@app.task
def video(meta):
    utc = dateutil.tz.tzutc()
    t = datetime.datetime.now(utc).isoformat()
    meta['t'] = t
    meta['product'] = 'video'
    meta['extension'] = 'flv'
    filename = generate_filename(meta)
    command = ['livestreamer',
               meta['url'],
               meta['stream'],
               '-f',
               '-o', filename]
    process = TimeoutSubprocess(command, 5)
    process.go()
    return process.output()


@app.task
def collect(meta):
    utc = dateutil.tz.tzutc()
    t = datetime.datetime.now(utc).isoformat()
    meta['t'] = t
    streams = livestreamer.streams(meta['url'])
    stream = streams[meta['stream']]
    cap = get_capture_from_livestream(stream)
    succes, img_bgr = cap.read()
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    # return numpy array and info
    filename = generate_filename(meta)
    meta['filename'] = filename
    plt.imsave(filename, img_rgb)
    return meta
