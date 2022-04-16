import socket,cv2, pickle,struct
import pyshine as ps # pip install pyshine
import imutils # pip install imutils

camera = True
if camera == True:
	vid = cv2.VideoCapture(0)
else:
	vid = cv2.VideoCapture('D://UNI Work/Uni DATA/Sem 8/FYP 2/samp.mp4')
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '192.168.18.73' # Here according to your server ip write the address

port = 9999
client_socket.connect((host_ip,port))

if client_socket: 
	while True:
		try:
			img, frame = vid.read()
			frame = imutils.resize(frame,width=380)
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