import logging
import datetime

import livestreamer
import cv2
import dateutil.tz

logger = logging.getLogger(__name__)


def capture_stations(stations):
    # capture objects
    infos = []
    for station in stations:
        for camera in station['cameras']:
            if camera['type'] == 'livestream':
                streams = livestreamer.streams(camera['url'])
                stream = streams[camera['stream']]
                info = {}
                info['cap'] = stream_capture(stream)
                info['station'] = station['id']
                info['camera'] = camera['id']
                info['imgtype'] = 'snap'
                info['extension'] = 'jpg'
                infos.append(info)
    # capture info
    for info in infos:
        utc = dateutil.tz.tzutc()
        t = datetime.datetime.now(utc)
        succes, img_bgr = info['cap'].read()
        info['t'] = t
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        logger.debug('captured: %s', info)
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
