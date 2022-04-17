from http import client
import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow,QStyledItemDelegate,QListWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5 import QtWidgets
from PyQt5 import QtCore



import sqlite3

import cv2



from PyQt5 import QtGui, QtWidgets, QtPrintSupport


from PyQt5.QtWidgets import QMessageBox


import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow,QStyledItemDelegate
from PyQt5.QtGui import QPixmap
import PyQt5

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from os import environ

import sqlite3

import sys

from PyQt5 import QtGui, QtWidgets, QtPrintSupport




                     ############  Dashboard PROCTOR SCREEN ###############

class dashboard_scr_proctor(QMainWindow):
    def __init__(self):
        super(dashboard_scr_proctor,self).__init__()
        loadUi('Dashboard_proctor_pannel.ui', self)
        self.Moniter_exam_btn.clicked.connect(self.goto_moniter_exam)
        self.Manage_exams_btn.clicked.connect(self.goto_manage_screen)
        self.Add_Exam_btn.clicked.connect(self.goto_add_exam)
        
    def goto_manage_screen(self):
        manage_exam = manage_exam_proctor_scr()
        print('asdasd')
        widget.addWidget(manage_exam)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def goto_moniter_exam(self):
       # self.Worker1 = Worker1()
      #  self.Worker1.start()
        moniter_exam = moniter_exam_proctor_scr()
        #self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
        widget.addWidget(moniter_exam)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def goto_add_exam(self):
        add_exam = Add_exam_proctor_scr()
        widget.addWidget(add_exam)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
                ############ ADD EXAM PROCTOR SCREEN ###############
        
class Add_exam_proctor_scr(QMainWindow):
    def __init__(self):
        super(Add_exam_proctor_scr,self).__init__()
        loadUi('Add_exam_Window.ui', self)
        
        self.Upload_pdf_btn.clicked.connect(self.upload_exam_image)
        self.add_student_pushButton.clicked.connect(self.Add_roll_number)
        self.dashboard_btn.clicked.connect(self.goto_dashboard)
   

        #  self.Save_btn.clicked.connect(self.save_to_database)
        
#     def save_to_database(self):
#         exam_name_db = self.exam_name_lineEdit.text()
#         exam_date_db = self.exam_date_lineEdit.text()
#         exam_time_db = self.exam_time_lineEdit.text()
#         lst = self.roll_number_listWidget                               #to be edited list widget
#         items = []
#         for x in range(lst.count()):
#             items.append(lst.item(x).text())
#         print(items) 
                   #to be edited
#         connection  = sqlite3.connect("Exam_beam_proctor.db")
#         c = connection.cursor()        
#         #query = 'select * from Employee limit 20 '
#         c.execute(query)
#         result = c.fetchall()
#        # print(result)
#        self.lcdNumber.display(result)
#         connection.commit()
#                         #close connection
#         connection.close()   
    def goto_dashboard(self):
        dash = dashboard_scr_proctor()
        widget.addWidget(dash)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
        
    def upload_exam_image(self):
        image = QFileDialog.getOpenFileName(None, 'OpenFile', '', 'All Files (*.*)')
        imagePath = image[0]
        if imagePath != (""):
            self.error_label.setText("Exam uploaded successfully")
        else:
            self.error_label.setText("Exam upload error ")
        return imagePath
    
           
    def Add_roll_number(self):
        roll_number = self.add_student_lineEdit.text()
        if roll_number != "":
            self.roll_number_listWidget.addItem(roll_number)
            self.add_student_lineEdit.setText("")
            self.error_label.setText("")
        else:
            self.error_label.setText("Enter roll number")

    
                            ############ MANAGE EXAM PROCTOR SCREEN ###############
        
class manage_exam_proctor_scr(QMainWindow):
    
    
    def __init__(self):
        super(manage_exam_proctor_scr,self).__init__()
        loadUi('Manage_exam.ui', self)
        self.Load_exam_data()
        self.Upload_pdf_btn.clicked.connect(self.upload_exam_image)
        self.dashboard_btn.clicked.connect(self.goto_dashboard)
        self.tableWidget.setColumnWidth(0,200)
        self.tableWidget.setColumnWidth(1,200)
        self.tableWidget.setColumnWidth(2,400)
     
    # self.add_student_pushButton.clicked.connect(self.Add_roll_number)
    
    def goto_dashboard(self):
        dash = dashboard_scr_proctor()
        widget.addWidget(dash)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def Load_exam_data(self):
        exam_name = self.exam_name_lineEdit.text()
        pass
        ### database code ###
        
    def upload_exam_image(self):
        image = QFileDialog.getOpenFileName(None, 'OpenFile', '', "Image file(*.jpg)")
        imagePath = image[0]
        pixmap = QPixmap(imagePath)
        self.pdf_document.setPixmap(pixmap)
        self.pdf_document.adjustSize()  # <---
        # print(ocr.resimden_yaziya(imagePath))
        print("this is the image path " , imagePath)
        return imagePath
    
    def Add_roll_number(self):
        roll_number = self.add_student_lineEdit.text()
        if roll_number != "":
        
            self.tableWidget.addItem(0,1,Qtwidgets.QtableWidgetItem(roll_number))               
            self.add_student_lineEdit.setText("")

        
        
        
                        ############ MONITER EXAM PROCTOR SCREEN ###############

Conf_threshold = 0.4
NMS_threshold = 0.4
COLORS = [(0, 255, 0), (0, 0, 255), (255, 0, 0),
          (255, 255, 0), (255, 0, 255), (0, 255, 255)]
          
class_name = []
with open('classes.txt', 'r') as f:
    class_name = [cname.strip() for cname in f.readlines()]

# Read deep learninng network
net = cv2.dnn.readNet('yolov4-tiny.weights', 'yolov4-tiny.cfg')

# Setting Computation Backends
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)

#Create model from deep learning network
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)

class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)
    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                #print('Type: ', type(Pic))
                
                self.ImageUpdate.emit(Pic)
    def stop(self):
        self.ThreadActive = False
        self.quit()  


import socket, cv2, pickle, struct
import imutils
import threading
import pyshine as ps # pip install pyshine

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host_ip = '192.168.1.13'
port = 9999
socket_address = (host_ip,port)
server_socket.bind(socket_address)
server_socket.listen()
print("Listening at",socket_address)





class Worker2(QThread):
    ImageUpdate = pyqtSignal(QImage)

    def show_client(self, addr,client_socket):
        try:
            print('CLIENT {} CONNECTED!'.format(addr))
            if client_socket: # if a client socket exists
                data = b""
                payload_size = struct.calcsize("Q")
                while True:
                    while len(data) < payload_size:
                        packet = client_socket.recv(4*1024) # 4K
                        if not packet: break
                        data+=packet
                    packed_msg_size = data[:payload_size]
                    data = data[payload_size:]
                    msg_size = struct.unpack("Q",packed_msg_size)[0]

                    #print("Msg Size: ", msg_size)

                    #warning = struct.unpack("Q",packed_msg_size)[1]

                    #print("Waring Count: ", warning)

                    while len(data) < msg_size:
                        data += client_socket.recv(4*1024)
                    frame_data = data[:msg_size]
                    data  = data[msg_size:]
                    frame = pickle.loads(frame_data)
                    text  =  f"CLIENT: {addr}"
                    frame =  ps.putBText(frame,text,10,10,vspace=10,hspace=1,font_scale=0.7, 						background_RGB=(255,0,0),text_RGB=(255,250,250))

                    
                    # PYQT Integration
                    Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    #frame = cv2.cvtColor(frame, cv2.COLOR_BG2BGR)
                    ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
                    #Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)

                    self.ImageUpdate.emit(ConvertToQtFormat)

                    cv2.imshow(f"FROM {addr}",frame)
                    key = cv2.waitKey(1) & 0xFF
                    if key  == ord('q'):
                        break
                client_socket.close()
        except Exception as e:
            print(f"CLINET {addr} DISCONNECTED")
            pass

    def get_warning(self):
        print("Getting msg at server side")
        server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socket_address = (host_ip,port-2)
        print('server listening at',socket_address)
        server_socket.bind(socket_address)
        server_socket.listen()

        client_socket,addr = server_socket.accept()
        print('Warning CLIENT {} CONNECTED!'.format(addr))
        # print("listening at",socket_address)
        print("done")

        # data = b""
        payload_size = struct.calcsize("Q")

        print("done2")

        # while True:
            # try:
        print('herere')
        # server_socket.close()

        data = client_socket.recv(1024)

        print("Recieved Data: ", data.decode())
                # while len(data) < payload_size:
                #     packet = server_socket.recv(4*1024) # 4K
                #     if not packet: break
                #     data+=packet
                # packed_msg_size = data[:payload_size]
                # data = data[payload_size:]
                # msg_size = struct.unpack("Q",packed_msg_size)[0]
                # while len(data) < msg_size:
                #     data += server_socket.recv(4*1024)
                # frame_data = data[:msg_size]
                # data  = data[msg_size:]
                # frame = pickle.loads(frame_data)
                # print('',end='\n')
                # print('CLIENT TEXT RECEIVED:',frame,end='\n')

            # except:
            #     break

        

    


    def run(self):
        self.ThreadActive = True
        #Capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            client_socket,addr = server_socket.accept()

            from concurrent.futures import ThreadPoolExecutor

            with ThreadPoolExecutor(max_workers=2) as executor:
                executor.submit(self.show_client, addr, client_socket)
                executor.submit(self.get_warning)
                #executor.shutdown(wait=True)
                
                
                
            # thread = threading.Thread(target=self.show_client, args=(addr,client_socket))
            # t2 = threading.Thread(target=self.get_warning, args=())
            # thread.start()
            # t2.start()

            print("TOTAL CLIENTS ",threading.activeCount() - 1)

    def stop(self):
        self.ThreadActive = False
        self.quit()          
            
            

            
class moniter_exam_proctor_scr(QMainWindow):
    
    def __init__(self):
        super(moniter_exam_proctor_scr,self).__init__()
        loadUi('Moniter_exam_window.ui', self)
        self.dashboard_btn.clicked.connect(self.goto_dashboard)
        
        
        self.Worker2 = Worker2()

        self.Worker2.start()
        x=1
        self.Worker2.ImageUpdate.connect(self.ImageUpdateSlot)
        
        
        
    def logic_seleting_window(self,t):
        x = 0
        y =0 
        x =t
        return t
       
                
                
            
  
        
        
    def select_window(self):
        list1 = [self.student_window_1,self.student_window_2,self.student_window_3,self.student_window_4,self.student_window_5,self.student_window_6,self.student_window_7,self.student_window_8,self.student_window_9,self.student_window_10]
        for i in range(0,len(list1)):
            
#             print(list1[i].pixmap())
            if list1[i].pixmap() == None:
                print(list1[i].objectName())
                return list1[i].objectName()
            

    def ImageUpdateSlot(self, Image):
#         x =0 
#         listt = [0,1,0,1,0,1,1,1,0]
#         for i in listt:
#             print("x value = ",x)
#             y = 0
#         x = 5
        x = self.logic_seleting_window(5)
      
        flag = 1
        flag2 = 1
    #         print("window 1 = " , self.student_window_1.pixmap())
    #         print("window 2 = " , self.student_window_2.pixmap())
    #         print("window 3 = " , self.student_window_3.pixmap())
    #         print("window 4 = " , self.student_window_4.pixmap())
        if x>=4:
            if x>=4 and self.student_window_1.pixmap() == None or flag == 1:
               
                self.student_window_1.setPixmap(QPixmap.fromImage(Image))


            elif x>=4 and self.student_window_2.pixmap() == None or flag == 1  :
#                 print("at this point x value is ",x)
                self.student_window_2.setPixmap(QPixmap.fromImage(Image))
                



            elif self.student_window_3.pixmap() == None:
                self.student_window_3.setPixmap(QPixmap.fromImage(Image))

            elif self.student_window_4.pixmap() == None:
                self.student_window_4.setPixmap(QPixmap.fromImage(Image))

            else:

                self.student_window_5.setPixmap(QPixmap.fromImage(Image))
        
        
#         x += i

#         position = self.select_window()
#         print("position =" ,position)
#         print(type(position))
        
        
#         str_position ="student_window_" + str(position +1)
#         print(str_position)
        
        
#         self.student_window_6.setPixmap(QPixmap.fromImage(Image))    
    
   
        
    def goto_dashboard(self):
        self.Worker2.stop()    
        dash = dashboard_scr_proctor()
        widget.addWidget(dash)
        widget.setCurrentIndex(widget.currentIndex()+1)
        


if __name__ == "__main__":
    App = QApplication(sys.argv)
    Root = dashboard_scr_proctor()
    width = 1800
    height = 1000
    widget  = QtWidgets.QStackedWidget()
    widget.setFixedSize(width, height)
   # widget.setWindowFlags(
  #  QtCore.Qt.Window |
    #QtCore.Qt.CustomizeWindowHint |
   # QtCore.Qt.WindowTitleHint |
   # QtCore.Qt.WindowCloseButtonHint |
  #  QtCore.Qt.WindowStaysOnTopHint
   #     )
    widget.addWidget(Root)
    widget.show()
    
    sys.exit(App.exec())

