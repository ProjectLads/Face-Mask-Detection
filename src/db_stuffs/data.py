import cv2 
import matplotlib.pyplot as plt
DATA_DIR = "C:/Users/hp/Desktop/ProjectLads/Face-Mask-Detection/src/db_stuffs/data.csv"
IMAGE_MASK_DIR = "C:/Users/hp/Desktop/ProjectLads/Face-Mask-Detection/src/db_stuffs/images/mask"

IMAGE_UNMASK_DIR = "C:/Users/hp/Desktop/ProjectLads/Face-Mask-Detection\src/db_stuffs/images/withoutMask" 
MASK_DIR = "/home/rupam/Face-Mask-Detection/src/db_stuffs/images/mask"


UNMASK_DIR = "/home/rupam/Face-Mask-Detection/src/db_stuffs/images/withoutMask" 

info =[]
image = []

def detect_face(frame):
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    boxes = faceCascade.detectMultiScale(gray, 1.1, 4)
    for x, y, w, h in boxes:
        #roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 2)
        faces = faceCascade.detectMultiScale(roi_color)

        # Box has a face
        if len(faces) > 0:
            return roi_color

    print("No face")
    return frame

            
            
with open(DATA_DIR) as data:
    for row in data:
        info.append(row.split(',')[1:6])
    #print(info[1:])
    
    info = info[1:]
    for row in info:
        image.append((IMAGE_MASK_DIR + '\\' + row[0] + '.jpeg', IMAGE_UNMASK_DIR + '\\' + row[0] + '.jpeg'))
        #image.append((MASK_DIR + '/' + row[0] + '.jpeg', UNMASK_DIR + '/' + row[0] + '.jpeg'))

    #print(image)

for i in image:
    #print(i[0])

    #img = cv2.imread(i[1]) #unmask run
    img = cv2.imread(i[0]) #mask run
    img_ret = detect_face(img)
    #print(img_ret)
    
    img_ret = cv2.resize(img_ret , (224 , 224))
    plt.imshow(cv2.cvtColor(img_ret, cv2.COLOR_BGR2RGB))
    plt.show()
    input()
    
    
