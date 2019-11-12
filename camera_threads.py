from threading import Thread, Lock
import cv2
import time

class WebcamVideoStream:
    def __init__(self, width=1920, height=1080):
        self.stream = cv2.VideoCapture("http://192.168.1.117:8080/video")
        (self.grabbed, self.frame) = self.stream.read()
        self.started = False
        self.read_lock = Lock()

    def start(self):
        if self.started:
            print("already started!!")
            return None
        self.started = True
        self.thread = Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self) :
        while self.started :
            (grabbed, frame) = self.stream.read()
            self.read_lock.acquire()
            self.grabbed, self.frame = grabbed, frame
            self.read_lock.release()

    def read(self):
        time.sleep(1)
        self.read_lock.acquire()
        self.frame = self.frame.copy()
        self.read_lock.release()
        return self.frame

    def stop(self):
        self.started = False
        self.thread.join()

    def __exit__(self, exc_type, exc_value, traceback):
        self.stream.release()


if __name__ == "__main__":
    vs = WebcamVideoStream().start()
    while True:
        print("aaa")
        frame = vs.read()
        cv2.imshow('webcam', frame)
        if cv2.waitKey(1) == 27:
            break

    vs.stop()
    cv2.destroyAllWindows()