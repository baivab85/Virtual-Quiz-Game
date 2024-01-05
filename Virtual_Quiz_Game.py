import cv2
import time
import csv
from cvzone.HandTrackingModule import HandDetector
import cvzone


cap = cv2.VideoCapture(0)
cap.set(3,1288)
cap.set(4,720)
detector = HandDetector(detectionCon=0.8)

class Mcq:
    def __init__(self,data):
        self.question=data[0]
        self.choice1=data[1]
        self.choice2=data[2]
        self.choice3=data[3]
        self.choice4=data[4]
        self.answer=int(data[5])
        
        self.userAns = None

    def update(self,cur,bboxs):
        for x,bbox in enumerate(bboxs):
            x1,y1,x2,y2 = bbox
            if x1<cursor[0]<x2 and y1<cursor[1]<y2:
                self.userAns=x+1
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),cv2.FILLED)


pathCsv="qs.csv"
with open(pathCsv,newline='\n') as f:
    reader=csv.reader(f)
    dataAll = list(reader)[1:]
qNo=0
qTotal=len(dataAll)

mcqlist=[]
for q in dataAll:
    mcqlist.append(Mcq(q))


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands,img =detector.findHands(img,flipType=False) 
    
    if qNo<qTotal:
        
       mcq=mcqlist[qNo]
    
       img,bbox=cvzone.putTextRect(img,mcq.question,[100,100],2,2,offset=50,border=5)
       img,bbox1=cvzone.putTextRect(img,mcq.choice1,[100,250],2,2,offset=50,border=5)
       img,bbox2=cvzone.putTextRect(img,mcq.choice2,[400,250],2,2,offset=50,border=5)
       img,bbox3=cvzone.putTextRect(img,mcq.choice3,[100,400],2,2,offset=50,border=5)
       img,bbox4=cvzone.putTextRect(img,mcq.choice4,[400,400],2,2,offset=50,border=5)
    
       if hands:
          lmList = hands[0]['lmList']
          cursor = lmList[8]
          length, info ,img= detector.findDistance((cursor[0], cursor[1]), (lmList[12][0], lmList[12][1]), img)

          if length < 50:
               mcq.update(cursor,[bbox1,bbox2,bbox3,bbox4])
               print(mcq.userAns)
             
               if mcq.userAns is not None:
                  time.sleep(0.3)
                  qNo+=1
    
    else:
        score=0
        for mcq in mcqlist:
            if mcq.answer == mcq.userAns:
                score+=1
                
        score = round((score/qTotal)*100,2)
        img, _ =cvzone.putTextRect(img,"Quiz Completed",[250,300],2,2,offset=50, border=5)
        img, _ =cvzone.putTextRect(img,f'Your Score: {score}%',[700,300],2,2,offset=50, border=5)
    
    
    
    
    barValue= 150+ (950//qTotal)*qNo
    
    cv2.rectangle(img,(150,600),(barValue,650),(0,255,0),cv2.FILLED)
    cv2.rectangle(img,(150,600),(1100,650),(255,0,255),5)
    
    
    cv2.imshow("Img", img)
    
    
    key = cv2.waitKey(1) & 0xFF
    
    # Check if the "Esc" key is pressed
    if key == 27:  # 27 is the ASCII code for the "Esc" key
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
