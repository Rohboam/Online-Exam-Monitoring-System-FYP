import cv2 as cv
import time
Conf_threshold = 0.4
NMS_threshold = 0.4
COLORS = [(0, 255, 0), (0, 0, 255), (255, 0, 0),
          (255, 255, 0), (255, 0, 255), (0, 255, 255)]
		  

class_name = []
with open('classes.txt', 'r') as f:
    class_name = [cname.strip() for cname in f.readlines()]
# print(class_name)

# Read deep learninng network
net = cv.dnn.readNet('yolov4-tiny.weights', 'yolov4-tiny.cfg')

# Setting Computation Backends
net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)


#Create model from deep learning network
model = cv.dnn_DetectionModel(net)
model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)



import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMessageBox


import cv2
class Video_feed_screen(QMainWindow):
    def __init__(self):
        super(Video_feed_screen, self).__init__()
        loadUi("C:/Users/rohba/Python/FYP_Ali/video_feed.ui", self)
        self.Worker1 = Worker1()
        self.Worker1.start()
        self.Worker1.imageupdate.connect(self.imageupdateslot)
        self.backbtn.clicked.connect(self.cancelfeed)


    def imageupdateslot(self , image):
        self.feedlabel.setPixmap(QPixmap.fromImage(image))

    def cancelfeed(self):
        self.Worker1.stop()
		

class Worker1(QThread):
    imageupdate = pyqtSignal(QImage)
    
    def run(self):
        self.ThreadActive = True
        capture = cv2.VideoCapture(0)
        
        starting_time = time.time()
        frame_counter = 0
        
        while self.ThreadActive:
            ret,frame = capture.read()
            if ret:
                
                ####
                classes, scores, boxes = model.detect(frame, Conf_threshold, NMS_threshold)
                for (classid, score, box) in zip(classes, scores, boxes):
                    color = COLORS[int(classid) % len(COLORS)]
                    label = '%s: %f'% (class_name[classid], score)
                    cv.rectangle(frame, box, color, 1)
                    cv.putText(frame, label, (box[0], box[1]-10),
                               cv.FONT_HERSHEY_COMPLEX, 0.3, color, 1)
                    
                    #print(class_name[classid])
                    
                    # Generating Warning
                    if (class_name[classid] == 'cell phone'):
                        #print("i")
                        msg = QMessageBox()
                        msg.setWindowTitle("Warning Message")
                        msg.setText("Mobile Detected")
                        msg.setIcon(QMessageBox.Warning)
                        x = msg.exec_()
                        
                    
                endingTime = time.time() - starting_time
                fps = frame_counter/endingTime
                # print(fps)
                
                key = cv.waitKey(1)

                #######

                image = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)
                flipedimage = cv2.flip(image , 1)
                converttoqtformat = QImage(flipedimage.data , flipedimage.shape[1], flipedimage.shape[0], QImage.Format_RGB888,)


                pic = converttoqtformat.scaled(640 , 480 , Qt.KeepAspectRatio)
                self.imageupdate.emit(pic)


    def stop(self):
        self.ThreadActive = False
        self.quit()
		
		
if __name__ == "__main__":
    App = QApplication(sys.argv)
    Root = Video_feed_screen()
    Root.show()
    sys.exit(App.exec())