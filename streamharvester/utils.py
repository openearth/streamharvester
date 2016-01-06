import signal
import subprocess
import threading
import time

class TimeoutSubprocess(threading.Thread):
    def __init__(self, cmd, timeout):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.timeout = timeout

    def run(self):
        self.p = subprocess.Popen(self.cmd)
        self.p.wait()

    def go(self):
        self.start()
        self.join(self.timeout)

        if self.is_alive():
            self.p.terminate()
            # use self.p.kill() if process needs a kill -9
            self.join()
    def output(self):
        return ''
