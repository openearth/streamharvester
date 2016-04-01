"""
This module provides code to synchronize execution
"""

import threading
import multiprocessing
import logging
import time

logger = logging.getLogger(__name__)


class Interval(threading.Thread):
    """Thread that executes code at certain intervals.
    It will try to wait to execute at fixed times. """
    def __init__(self, group=None, target=None, name=None,
                 interval=None, args=None, kwargs=None):
        # for consistency with kwargs
        if args is None:
            args = ()
        if kwargs is None:
            kwargs = {}
        super(Interval, self).__init__(group=group, target=target,
                                       name=name, args=args, kwargs=kwargs)
        self.event = threading.Event()
        # start of time (used to determine on which times we stop)
        self.epoch = 0.0

        # interval in seconds
        self.interval = interval
        # the function to be called
        self.target = target
        # the arguments to be passed to the target
        self.args = args
        self.kwargs = kwargs

    def run(self):
        """start the thread"""
        # wait for event to be set by calling .stop
        while not self.event.is_set():
            # how long have we been alive
            time_alive = time.time() - self.epoch
            # how long we have to wait depends on how long has past
            wait = self.interval - time_alive % self.interval
            # wait for a bit
            if not self.event.wait(wait):
                # if it timed out, then get to work
                self.target(*self.args, **self.kwargs)

    def stop(self):
        self.event.set()


class IntervalProcess(multiprocessing.Process):
    """Subprocess that executes code at certain intervals.
    It will try to wait to execute at fixed times. Note that this is not usable with OpenCV (under OSX) as it does not support forking. """
    def __init__(self, group=None, target=None, name=None,
                 interval=None, args=None, kwargs=None):
        # for consistency with kwargs
        if args is None:
            args = ()
        if kwargs is None:
            kwargs = {}
        super(IntervalProcess, self).__init__(group=group, target=target,
                                       name=name, args=args, kwargs=kwargs)
        self.event = multiprocessing.Event()
        # start of time (used to determine on which times we stop)
        self.epoch = 0.0

        # interval in seconds
        self.interval = interval
        # the function to be called
        self.target = target
        # the arguments to be passed to the target
        self.args = args
        self.kwargs = kwargs

    def run(self):
        """start the thread"""
        # wait for event to be set by calling .stop
        while not self.event.is_set():
            # how long have we been alive
            time_alive = time.time() - self.epoch
            # how long we have to wait depends on how long has past
            wait = self.interval - time_alive % self.interval
            # wait for a bit
            if not self.event.wait(wait):
                # if it timed out, then get to work
                self.target(*self.args, **self.kwargs)

    def stop(self):
        self.event.set()
