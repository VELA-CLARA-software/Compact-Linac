import numpy as np
import cv2
import time
import requests
import threading
from threading import Thread, Event, ThreadError
import sys
import datetime
import os

class capture_image():

    def __init__(self, url, label='', directory='.'):
        self.label = label
        self.stream = requests.get(url, stream=True)
        self.thread_cancelled = False
        self.thread = Thread(target=self.run)
        self.start()
        self.dir = directory
        if not os.path.isdir(self.dir):
            os.makedirs(self.dir)

    def start(self):
        self.thread.start()

    def run(self):
        bytes=''
        while not self.thread_cancelled:
            try:
                bytes+=self.stream.raw.read(1024)
                a = bytes.find('\xff\xd8')
                b = bytes.find('\xff\xd9')
                if a!=-1 and b!=-1:
                    jpg = bytes[a:b+2]
                    bytes= bytes[b+2:]
                    img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
                    # cv2.imshow('cam',img)
                    currenttimestamp = '{:%Y-%m-%d %H.%M.%S}'.format(datetime.datetime.now())
                    print self.dir+'/'+currenttimestamp+'_'+self.label+'.png'
                    cv2.imwrite(self.dir+'/'+currenttimestamp+'_'+self.label+'.png',img)
                    return True
            except ThreadError:
                self.thread_cancelled = True

    def is_running(self):
        return self.thread.isAlive()

    def shut_down(self):
        self.thread_cancelled = True
        #block while waiting for thread to terminate
        while self.thread.isAlive():
            time.sleep(1)
        return True

class show_image():

    def __init__(self, url, label='', directory='.'):
        self.label = label
        self.stream = requests.get(url, stream=True)
        self.thread_cancelled = False
        self.thread = Thread(target=self.run)
        self.start()
        self.dir = directory
        if not os.path.isdir(self.dir):
            os.makedirs(self.dir)

    def start(self):
        self.thread.start()

    def run(self):
        bytes=''
        while not self.thread_cancelled:
            try:
                bytes+=self.stream.raw.read(1024)
                a = bytes.find('\xff\xd8')
                b = bytes.find('\xff\xd9')
                if a!=-1 and b!=-1:
                    jpg = bytes[a:b+2]
                    bytes= bytes[b+2:]
                    img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
                    cv2.imshow('cam',img)
                    k = cv2.waitKey(100)
                    if k == 27:
                        currenttimestamp = '{:%Y-%m-%d %H.%M.%S}'.format(datetime.datetime.now())
                        cv2.imwrite(currenttimestamp+'_'+'.png',img)
                        return True # esc to quit
                    elif k == ord('s'):
                        currenttimestamp = '{:%Y-%m-%d %H.%M.%S}'.format(datetime.datetime.now())
                        cv2.imwrite(currenttimestamp+'_'+'.png',img)
            except ThreadError:
                self.thread_cancelled = True

    def is_running(self):
        return self.thread.isAlive()

    def shut_down(self):
        self.thread_cancelled = True
        #block while waiting for thread to terminate
        while self.thread.isAlive():
            time.sleep(1)
        return True

if __name__ == "__main__":
    url = 'http://148.79.170.34/mjpg/video.mjpg'
    cam = show_image(url,'test')
