import logging
import datetime

import celery

import livestreamer
import cv2
import dateutil.tz

logger = logging.getLogger(__name__)


def schedule_collect(info):
    # capture info
    for counter in range(5):
        for product in info["products"]:
            meta = {}
            meta.update(info)
            meta.update(product)
            utc = dateutil.tz.tzutc()
            t = datetime.datetime.now(utc)
            meta['t'] = t
            meta['counter'] = counter
            yield collect(meta)

def collect(info):
    streams = livestreamer.streams(info['url'])
    stream = streams[info['stream']]
    cap = get_capture_from_livestream(stream)
    succes, img_bgr = cap.read()
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    logger.debug('captured: %s', info)
    # return numpy array and info
    return img_rgb, info



def capture_stations(stations):
    # capture objects
    for station in stations:
        for camera in station['cameras']:
            info = {}
            info.update(station)
            info.update(camera)
            info['station'] = station['id']
            info['camera'] = camera['id']
            for img_rgb, info in schedule_collect(info):
                yield img_rgb, info

def get_capture_from_livestream(stream):
    """open a stream and return an opencv capture object"""

    cap = cv2.VideoCapture()
    try:
        cap.open(stream.url)
    except AttributeError:
        # url for rtmp streams (bambuser/flash)
        if 'playpath' in stream.params:
            cap.open(stream.params['rtmp'] + '/' + stream.params['playpath'])
        else:
            cap.open(stream.params['rtmp'])
    return cap
