import socket,cv2, pickle,struct
import pyshine as ps # pip install pyshine
import imutils # pip install imutils

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
net = cv2.dnn.readNet('yolov4-tiny.weights', 'yolov4-tiny.cfg')

# Setting Computation Backends
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)

#Create model from deep learning network
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)

camera = True
if camera == True:
    vid = cv2.VideoCapture(0)
else:
    vid = cv2.VideoCapture('D://UNI Work/Uni DATA/Sem 8/FYP 2/samp.mp4')
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '192.168.1.13' # Here according to your server ip write the address

port = 9999
client_socket.connect((host_ip,port))

if client_socket: 
    while True:
        try:
            img, frame = vid.read()
            frame = imutils.resize(frame,width=380)
            
            classes, scores, boxes = model.detect(frame, Conf_threshold, NMS_threshold)

            for (classid, score, box) in zip(classes, scores, boxes):
                color = COLORS[int(classid) % len(COLORS)]
                label = '%s: %f' % (class_name[classid], score)
                cv2.rectangle(frame, box, color, 1)
                cv2.putText(frame, label, (box[0], box[1] - 10),
                           cv2.FONT_HERSHEY_COMPLEX, 0.3, color, 1)

                # Generating Warning
                if (class_name[classid] == 'cell phone'):
                    print("i")
            
            a = pickle.dumps(frame)
            message = struct.pack("Q",len(a))+a
            client_socket.sendall(message)
            #cv2.imshow(f"TO: {host_ip}",frame)
            key = cv2.waitKey(10)
            if key == 13:
                client_socket.close()
        except:
            print('VIDEO FINISHED!')
            break