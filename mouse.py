import cv2
import numpy as np
import pyautogui as pa

captura = cv2.VideoCapture(0)

ct = 0
mmx = 0
mmy = 0

mx = np.zeros(6)
my = np.zeros(6)

s_width = pa.size().width
s_height = pa.size().height

print('Width: '+str(s_width/2)+' Height: '+str(s_height/2))

pa.moveTo(s_width/2,s_height/2)

def direct(image,i):
	nivel = i+1
	font                   = cv2.FONT_HERSHEY_SIMPLEX
	bottomLeftCornerOfText = (25,40*nivel)
	fontScale              = 1
	color             	   = (255,255,255)
	lineType               = 2

	if i == 0:
		#up
		cv2.putText(image, 'UP', bottomLeftCornerOfText, font, fontScale, color, lineType)
		pa.moveRel(0,-50)
	if i == 1:
		#down
		cv2.putText(image, 'DOWN', bottomLeftCornerOfText, font, fontScale, color, lineType)
		pa.moveRel(0,50)
	if i == 2:
		#left
		cv2.putText(image, 'RIGHT', bottomLeftCornerOfText, font, fontScale, color, lineType)
		pa.moveRel(50,0)
	if i == 3:
		#right
		cv2.putText(image, 'LEFT', bottomLeftCornerOfText, font, fontScale, color, lineType)
		pa.moveRel(-50,0)

	return image

while(True):
	ret, frame = captura.read()

	image = frame.copy()

	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.equalizeHist(gray) 

	face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
	faces  = face_cascade.detectMultiScale(gray, scaleFactor = 1.3, minNeighbors = 5)

	for (sx, sy, sw, sh) in faces:
		cv2.rectangle(gray, (sx, sy), ((sx + sw), (sy + sh)), (255, 255, 255), 2)
		
		'''
		roi = gray[sy:sy+sh,sx:sx+sw] # primeira abordagem
		roi = cv2.equalizeHist(roi)
		gray[sy:sy+sh,sx:sx+sw] = roi
		'''

		roi1 = gray[sy:sy+int(sh/2),sx:sx+int(sw/2)]
		roi2 = gray[sy:sy+int(sh/2),sx+int(sw/2):sx+sw]
		roi3 = gray[sy+int(sh/2):sy+sh,sx:sx+int(sw/2)]
		roi4 = gray[sy:sy+sh,sx+int(sw/2):sx+sw]

		roi1 = cv2.equalizeHist(roi1)
		roi2 = cv2.equalizeHist(roi2)
		roi3 = cv2.equalizeHist(roi3)
		roi4 = cv2.equalizeHist(roi4)

		gray[sy:sy+int(sh/2),sx:sx+int(sw/2)] = roi1
		gray[sy:sy+int(sh/2),sx+int(sw/2):sx+sw] = roi2
		gray[sy+int(sh/2):sy+sh,sx:sx+int(sw/2)] = roi3
		gray[sy:sy+sh,sx+int(sw/2):sx+sw] = roi4

		roi = gray[sy:sy+sh,sx:sx+sw]

		eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
		eyes  = eye_cascade.detectMultiScale(roi, scaleFactor = 1.1, minNeighbors = 7)

		eyes_ord = np.zeros((len(eyes),5), dtype=int)

		for i in range(len(eyes)):
			eyes_ord[i] = [int((eyes[i][0]**2)+(eyes[i][1]**2)),int(eyes[i][0]),int(eyes[i][1]),int(eyes[i][2]),int(eyes[i][3])]

		eyes_ord = eyes_ord[np.argsort(eyes_ord[:, 0])]

		if len(eyes_ord) >= 2:
			lim = 2
		else:
			lim = len(eyes_ord)

		eyes_ord = eyes_ord[0:lim,1:5]

		#print('\n')
		#print(eyes_ord)
		#print(eyes)
		#print('\n')

		middle_point = np.zeros((lim,2), dtype=int)
		i = 0

		for (sxe, sye, swe, she) in eyes_ord:
			mx[5] = mx[4]
			mx[4] = mx[3]
			mx[3] = mx[2]
			mx[2] = mx[1]
			mx[1] = mx[0]
			mx[0] = int(sxe+(swe/2)+sx)
			
			my[5] = my[4]
			my[4] = my[3]
			my[3] = my[2]
			my[2] = my[1]
			my[1] = my[0]
			my[0] = int(sye+(she/2)+sy)

			if int(np.mean(mx)) > mmx+(sw*0.07) and ct>30:
				direct(image,3)
			if int(np.mean(my)) > mmy+(sh*0.07) and ct>30:
				direct(image,1)
			if int(np.mean(mx)) < mmx-(sw*0.07) and ct>30:
				direct(image,2)
			if int(np.mean(my)) < mmy-(sh*0.07) and ct>30:
				direct(image,0)

			cv2.rectangle(image, (int(mmx-(sw*0.07)), int(mmy-(sh*0.07))), (int(mmx+(sw*0.07)), int(mmy+(sh*0.07))), (255, 255, 255), 1)

			#print('MMX: '+str(mmx)+' | MMY: '+str(mmy))
			#print('mx: '+str(mx)+' | my: '+str(my))

			middle_point[i] = [np.mean(mx),np.mean(my)]
			sxe = sxe+sx
			sye = sye+sy
			cv2.rectangle(image, (int(np.mean(mx)), int(np.mean(my))), ((int(np.mean(mx)) + 4), (int(np.mean(my)) + 4)), (255, 255, 255), 2)
			#cv2.rectangle(image, (sxe, sye), ((sxe + swe), (sye + she)), (255, 255, 255), 2) #olhos

			i = i+1

		#print(middle_point)

		if ct%2 == 0 and i != 0:
			mmx = int(np.mean(middle_point[:,0]))
			mmy = int(np.mean(middle_point[:,1]))

		#cv2.rectangle(gray, (int(0.95*mmx), int(0.95*mmy)), (int(mmx*1.05), int(mmy*1.05)), (255, 255, 255), 2)

	cv2.imshow("Eyes Mouse", image)

	k = cv2.waitKey(30) & 0xff
	if k == 27:
		break

	ct = ct + 1