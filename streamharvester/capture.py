import logging
import datetime

import livestreamer
import cv2

logger = logging.getLogger(__name__)


def capture_stations(stations):
    # capture objects
    caps = []
    for station in stations:
        for camera in station['cameras']:
            if camera['type'] == 'livestream':
                streams = livestreamer.streams(camera['url'])
                stream = streams[camera['stream']]
                cap = stream_capture(stream)
                caps.append(cap)
    for cap in caps:
        info = {}
        t = datetime.datetime.now()
        succes, img_bgr = cap.read()
        info['t'] = t
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        yield img_rgb, info


def stream_capture(stream):
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
