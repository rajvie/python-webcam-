import cv2, time,pandas

from datetime import datetime



video = cv2.VideoCapture(0)

first_frame = None



status_list=[None,None]

df =  pandas.DataFrame(columns=["Start","End"])

while True:

    check, frame = video.read()

    status=0



    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    gray = cv2.GaussianBlur(gray,(21,21),0)

    if first_frame is None:

        first_frame = gray

        continue



    delta_frame = cv2.absdiff(first_frame,gray)

    thresh_frame = cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1]

    thresh_frame = cv2.dilate(thresh_frame, None, iterations=5)



    (cnts,_) = cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in cnts:

        if cv2.contourArea(c) < 1000:



            continue

        status =1

        (x,y,w,h) = cv2.boundingRect(c)

        cv2.rectangle(frame, (x,y),(x+w,y+h),(0,250,0),3)



    status_list.append(status)



    if status_list[-1] == 1 and status_list[-2]==0:

        with open("time.txt","a+") as file:

            file.write(str(datetime.now())+"\n")

            print("added")

    if status_list[-1] == 0 and status_list[-2]==1:

        with open("time.txt","a+") as   file:

            file.write(str(datetime.now())+"\n")

            print("added")

    cv2.imshow("Gray_frame",gray)

    cv2.imshow("delta_frame",delta_frame)

    cv2.imshow("thresh_frame",thresh_frame)

    cv2.imshow("frame",frame)



    key=cv2.waitKey(1)

    if key == ord('q'):

        print(status_list)

        if status == 1:

            with open("time.txt","a+") as file:

                file.write(str(datetime.now())+"\n")

        break



count=0

with open("time.txt","r") as file:

    for line in file.readlines():

        line=line.strip()

        if count%2 == 0:

            df= df.append({"Start":datetime.strptime(line,'%Y-%m-%d %H:%M:%S.%f')},ignore_index=True)

        elif count%2 ==1:

            df= df.append({"End":datetime.strptime(line,'%Y-%m-%d %H:%M:%S.%f')},ignore_index=True)

        count= count+1



df.to_csv("times.csv")

video.release()

cv2.destroyAllWindows
