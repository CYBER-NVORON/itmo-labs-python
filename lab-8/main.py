import cv2
import numpy as np
import time

def task_1():
    print("Задание 1:")
    image = cv2.imread('variant-8.jpg')

    center = image.shape
    w, h = 400, 400
    x = (center[1] - w)//2
    y = (center[0] - h)//2

    crop_img = image[y:y+h, x:x+w]

    cv2.imwrite("result.jpg", crop_img)

    print("Файл сохранён!")

def task_2():
    print("Задание 2 + модификация:")
    cap = cv2.VideoCapture(0)
    i = 0

    while True:
        flag, frame = cap.read()
        
        if not flag:
            break

        h, w = frame.shape[:2]

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h_min = np.array((113, 100, 100), np.uint8) #Эти значения - нижний и верхний порог нужного цвета
        h_max = np.array((133, 255, 255), np.uint8) #Для этого надо сделать скриншот и пепеткой вытащить RGB расцветку и засунуть в picker.py
        thresh = cv2.inRange(hsv, h_min, h_max)
        moments = cv2.moments(thresh, 1)
        dM01 = moments["m01"]
        dM10 = moments["m10"]
        dArea = moments["m00"]
        
        if dArea > 100:

            x=int(dM10/dArea)
            y=int(dM01/dArea)

            cv2.line(frame, (x,0), (x,h), (0,255,255), 5)
            cv2.line(frame, (0,y), (w,y), (0,255,255), 5)

        cv2.imshow('frame', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.001)
        i += 1

    cap.release()


if __name__ == "__main__":
    print("Вариант 8:")
    task_1()
    task_2()