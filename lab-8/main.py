import time
import numpy as np
import cv2


def task_1():

    print("Задание 1:")

    image = cv2.imread("variant-8.jpg")

    center = image.shape
    w, h = 400, 400
    x = (center[1] - w) // 2
    y = (center[0] - h) // 2

    crop_img = image[y: y + h, x: x + w]

    cv2.imwrite("result.jpg", crop_img)

    print("Файл сохранён!")


def task_2():

    print("Задание 2 + модификация:")

    cap = cv2.VideoCapture(0)

    while True:
        flag, frame = cap.read()

        if not flag:
            break

        h, w = frame.shape[:2]

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h_min = np.array((113, 100, 100), np.uint8)
        h_max = np.array((133, 255, 255), np.uint8)
        thresh = cv2.inRange(hsv, h_min, h_max)
        moments = cv2.moments(thresh, 1)
        m01 = moments["m01"]
        m10 = moments["m10"]
        area = moments["m00"]

        if area > 100:

            x = int(m10 / area)
            y = int(m01 / area)

            cv2.line(frame, (x, 0), (x, h), (0, 255, 255), 5)
            cv2.line(frame, (0, y), (w, y), (0, 255, 255), 5)

        cv2.imshow("frame", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        time.sleep(0.001)

    cap.release()


def overlay(background, img, x, y):

    place = background[y: y + img.shape[0], x: x + img.shape[1]]
    place[...] = place + img
    return background.astype("uint8")


def extra():

    print("Дополнительное:")
    cap = cv2.VideoCapture(0)
    fly = cv2.imread("fly64.png")
    while True:
        flag, frame = cap.read()

        if not flag:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h_min = np.array((113, 100, 100), np.uint8)
        h_max = np.array((133, 255, 255), np.uint8)  # Use picker.py
        thresh = cv2.inRange(hsv, h_min, h_max)
        moments = cv2.moments(thresh, 1)
        m01 = moments["m01"]
        m10 = moments["m10"]
        area = moments["m00"]

        if area > 100:

            x = int(m10 / area - 32)
            y = int(m01 / area - 32)

            overlay(frame, fly, x, y)

        cv2.imshow("frame", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        time.sleep(0.001)

    cap.release()


if __name__ == "__main__":
    print("Вариант 8:")
    task_1()
    task_2()
    extra()
