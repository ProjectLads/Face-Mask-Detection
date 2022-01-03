import cv2
import matplotlib.pyplot as plt
DATA_DIR = "data.csv"
IMAGE_MASK_DIR = "D:\Projectlads\Face-Mask-Detection\src\db_stuffs\images\mask"
IMAGE_UNMASK_DIR = "D:\Projectlads\Face-Mask-Detection\src\db_stuffs\images\withoutMask" 
info =[]
image = []

def detect_face(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = faceCascade.detectMultiScale(gray, 1.1, 4)
    for x, y, w, h in faces:
        #roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 2)
        facess = faceCascade.detectMultiScale(roi_color)
    if len(facess) == 0:
        print("Face not detected")
        face_roi =''
    else:
        for (ex, ey, ew, eh) in facess:
            face_roi = roi_color[ey: ey+eh, ex: ex+ew]
    
    return face_roi
            
            
with open(DATA_DIR) as data:
    for row in data:
        info.append(row.split(',')[1:6])
    #print(info[1:])
    
    info = info[1:]
    for row in info:
        image.append((IMAGE_MASK_DIR + '\\' + row[0] + '.jpeg', IMAGE_UNMASK_DIR + '\\' + row[0] + '.jpeg'))
    #print(image)
 

for i in image:
    #print(i[0])
    img = cv2.imread(i[1])
    img_ret = detect_face(img)
    #print(img_ret)
    cv2.imshow('img', img_ret)
    #plt.imshow(cv2.cvtColor(img_ret, cv2.COLOR_BGR2RGB))
    #plt.show()
    input()
    
    