import cv2
from threading import Thread

class CameraStream():
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        self.success, self.frame = self.stream.read()
        self.stopped = False

    def start(self):
        Thread(target=self.update, args=(), daemon=True).start()
        return self

    def update(self):
        while not self.stopped:
            self.success, self.frame = self.stream.read()
        self.stream.release()

    def read(self):
        return self.success, self.frame

    def stop(self):
        self.stopped = True