import cv2
import numpy as np
import dlib
from math import hypot
import pyglet
import time
import pyttsx3

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


# let's load the sound
# sound = pyglet.media.load('sound.wav')
# leftSound = pyglet.media.load('left.wav')
# rightSound = pyglet.media.load('right.wav')

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


def calmidpoint(p1, p2):
    return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)


def getBlinkingRation(points, facil_landmarks):
    left_point = (landmarks.part(points[0]).x, landmarks.part(points[0]).y)
    right_point = (landmarks.part(points[3]).x, landmarks.part(points[3]).y)
    centerTop = calmidpoint(landmarks.part(points[1]), landmarks.part(points[2]))
    centerBottom = calmidpoint(landmarks.part(points[5]), landmarks.part(points[4]))

    # h_line = cv2.line(frame, left_point, right_point, (0, 255, 00), 1)
    # centerPoint = cv2.line(frame, centerTop, centerBottom, (0, 255, 0), 1)
    # cv2.circle(frame, (x, y), 3, (255, 0, 0,), -1)
    hor_line = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    ver_line = hypot((centerTop[0] - centerBottom[0]), (centerTop[1] - centerBottom[1]))
    # print(ver_line)
    ratio = hor_line / ver_line
    return ratio


def getGazeration(eyepoints, landmarks):
    leftEyeRegion = np.array([(landmarks.part(eyepoints[0]).x, landmarks.part(eyepoints[0]).y),
                              (landmarks.part(eyepoints[1]).x, landmarks.part(eyepoints[1]).y),
                              (landmarks.part(eyepoints[2]).x, landmarks.part(eyepoints[2]).y),
                              (landmarks.part(eyepoints[3]).x, landmarks.part(eyepoints[3]).y),
                              (landmarks.part(eyepoints[4]).x, landmarks.part(eyepoints[4]).y),
                              (landmarks.part(eyepoints[5]).x, landmarks.part(eyepoints[5]).y)], np.int32)

    # rightEyeRegion = np.array([(landmarks.part(42).x, landmarks.part(42).y),
    #                            (landmarks.part(43).x, landmarks.part(43).y),
    #                            (landmarks.part(44).x, landmarks.part(44).y),
    #                            (landmarks.part(45).x, landmarks.part(45).y),
    #                            (landmarks.part(46).x, landmarks.part(46).y),
    #                            (landmarks.part(47).x, landmarks.part(47).y)], np.int32)

    # cv2.polylines(frame, [leftEyeRegion], True, (0, 255, 0), 1)
    # cv2.polylines(frame, [rightEyeRegion], True, (0, 255, 0), 1)

    # Let's create a mask
    height, width, _ = frame.shape
    mask = np.zeros((height, width), np.uint8)

    # Let's fill the mask with our eye region
    cv2.polylines(mask, [leftEyeRegion], True, 255, 1)
    cv2.fillPoly(mask, [leftEyeRegion], 255)
    eye = cv2.bitwise_and(gray, gray, mask=mask)

    # cv2.polylines(mask, [rightEyeRegion], True, 255, 2)
    # cv2.fillPoly(mask, [rightEyeRation], 255)

    minX = np.min(leftEyeRegion[:, 0])
    maxX = np.max(leftEyeRegion[:, 0])
    minY = np.min(leftEyeRegion[:, 1])
    maxY = np.max(leftEyeRegion[:, 1])

    gray_eye = eye[minY:maxY, minX:maxX]
    _, thresholdEye = cv2.threshold(gray_eye, 60, 255, cv2.THRESH_BINARY)

    # Let's Divide the threshold to detect left and right side
    height, width = thresholdEye.shape
    leftSideThreshold = thresholdEye[0:height, 0:int(width / 2)]
    # leftSideThreshold = cv2.resize(leftSideThreshold, None, fx=5, fy=5)
    leftSideWhite = cv2.countNonZero(leftSideThreshold)

    rightSideThreshold = thresholdEye[0:height, int(width / 2):width]
    rightSideWhite = cv2.countNonZero(rightSideThreshold)

    if leftSideWhite == 0:
        ratio = 1
    elif rightSideWhite == 0:
        ratio = 5
    else:
        ratio = leftSideWhite / rightSideWhite
    return ratio


# let's set keyboard
keybord = np.ones((200, 500, 3), np.uint8)
board = np.zeros((150, 300), np.uint8)
board[:] = 255

key_set_1 = {0: 'Q', 1: 'W', 2: 'E', 3: 'R', 4: 'T', 5: 'Y', 6: 'U', 7: 'I', 8: 'O', 9: 'P',
             10: 'A', 11: 'S', 12: 'D', 13: 'F', 14: 'G', 15: 'H', 16: 'J', 17: 'K', 18: 'L',
             19: 'Z', 20: 'X', 21: 'C', 22: 'V', 23: 'B', 24: 'N', 25: 'M', 26: ' '}


def drawLetterRec(key_index, text):
    if key_index == 0:
        x = 0
        y = 0
    elif key_index == 1:
        x = 50
        y = 0
    elif key_index == 2:
        x = 100
        y = 0
    elif key_index == 3:
        x = 150
        y = 0
    elif key_index == 4:
        x = 200
        y = 0
    elif key_index == 5:
        x = 250
        y = 0
    elif key_index == 6:
        x = 300
        y = 0
    elif key_index == 7:
        x = 350
        y = 0
    elif key_index == 8:
        x = 400
        y = 0
    elif key_index == 9:
        x = 450
        y = 0
    elif key_index == 10:
        x = 500
        y = 0
    elif key_index == 11:
        x = 50
        y = 50
    elif key_index == 12:
        x = 100
        y = 50
    elif key_index == 13:
        x = 150
        y = 50
    elif key_index == 14:
        x = 200
        y = 50
    elif key_index == 15:
        x = 250
        y = 50
    elif key_index == 16:
        x = 300
        y = 50
    elif key_index == 17:
        x = 350
        y = 50
    elif key_index == 18:
        x = 400
        y = 50
    elif key_index == 19:
        x = 50
        y = 100
    elif key_index == 20:
        x = 100
        y = 100
    elif key_index == 21:
        x = 150
        y = 100
    elif key_index == 22:
        x = 200
        y = 100
    elif key_index == 23:
        x = 250
        y = 100
    elif key_index == 24:
        x = 300
        y = 100
    elif key_index == 25:
        x = 350
        y = 100
    elif key_index == 26:
        x = 120
        y = 150

    width = 50
    height = 50
    th = 1
    # if letter_index==26:
    #     if light is True:
    #         cv2.rectangle(keybord, (x + th, y + th), (x + 200 - th, y + 40 - th), (255, 255, 255), -1)
    #     else:
    #         cv2.rectangle(keybord, (x + th, y + th), (x + 200 - th, y + 40 - th), (255, 0, 0), th)
    # else:
    # if light is True:
    #     if key_index == 26:
    #         cv2.rectangle(keybord, (x + th, y + th), (x + 200 - th, y + height - th), (255, 255, 255), 1)
    #     else:
    #         cv2.rectangle(keybord, (x + th, y + th), (x + width - th, y + height - th), (255, 255, 255), 1)
    # else:
    if key_index == 26:
        cv2.rectangle(keybord, (x + th, y + th), (x + 200 - th, y + height - th), (255, 0, 0), th)
    else:
        cv2.rectangle(keybord, (x + th, y + th), (x + width - th, y + height - th), (255, 0, 0), th)

    # Let's set he text

    font_letter = cv2.FONT_HERSHEY_PLAIN
    font_scale = 2
    font_th = 1
    text_size = cv2.getTextSize(text, font_letter, font_scale, font_th)[0]
    text_width, text_height = text_size[0], text_size[1]
    if key_index == 26:
        text_x = int((120 - text_width) / 2) + x
        text_y = int((40 + text_height) / 2) + y
        cv2.putText(keybord, "Space", (text_x, text_y), font_letter, font_scale, (255, 0, 0), font_th)
    else:
        text_x = int((width - text_width) / 2) + x
        text_y = int((height + text_height) / 2) + y
        cv2.putText(keybord, text, (text_x, text_y), font_letter, font_scale, (255, 0, 0), font_th)


# Counter
frames = 0
letter_index = 0
blinkingFrames = 0
framesToBlink = 6
framesActive = 9
leftRightFrames = 0

text = " "
keybordSelected = 'left'
lastSelection = 'left'
selectKeyboradMenu = True

count = 0
while True:

    __, frame = cap.read()
    rows, cols, _ = frame.shape
    keybord[:] = (0, 0, 0)
    frames += 1
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    activeKey = key_set_1[letter_index]

    faces = detector(gray)
    for face in faces:
        x, y = face.left(), face.top()
        x1, y1 = face.right(), face.bottom()
        cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)

        landmarks = predictor(gray, face)
        leftEyeRation = getBlinkingRation([36, 37, 38, 39, 40, 41], landmarks)
        rightEyeRation = getBlinkingRation([42, 43, 44, 45, 46, 47], landmarks)
        blinkingration = (leftEyeRation + rightEyeRation) / 2
        # print(ratio)

        if blinkingration > 5.3:
            cv2.putText(frame, "BLINK", (50, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (255, 0, 0), 1)
            count += 1
            blinkingFrames += 1
            frames -= 1
            print(f"blinking frames {blinkingFrames}")
            # Type the letter
            if blinkingFrames == 5:
                text += activeKey
                speak("Pressed")

        else:
            blinkingFrames = 0

        # Detect Gaze#
        leftEyeGazeratio = getGazeration([36, 37, 38, 39, 40, 41], landmarks)

        rightEyeGazeration = getGazeration([42, 43, 44, 45, 46, 47], landmarks)

        gazeRatio = (leftEyeGazeratio + rightEyeGazeration) / 2

        cv2.putText(frame, str(gazeRatio), (70, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

        if gazeRatio < 0.5:
            cv2.putText(frame, "LEFT", (50, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            keybordSelected = 'right'
            leftRightFrames += 1
            print(leftRightFrames)

            # if keybordSelected != lastSelection and leftRightFrames==5:
            if keybordSelected != lastSelection and leftRightFrames == 5:
                print("enter into Left")
                letter_index -= 1
                frames-=1
                speak(activeKey[letter_index])
                speak("Right")
                lastSelection = keybordSelected
                leftRightFrames = 0

        else:
            leftRightFrames = 0

        if 1.90 < gazeRatio:

            keybordSelected = 'left'
            cv2.putText(frame, "RIGHT", (50, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            leftRightFrames += 1

            if keybordSelected != lastSelection and leftRightFrames == 5:
                print("enter into right")
                letter_index += 1
                speak(activeKey[letter_index])
                frames-=1

                speak("Left")
                lastSelection = keybordSelected
                leftRightFrames = 0
        else:
            leftRightFrames = 0

        # cv2.putText(frame, str(rightEyeGazeration), (50, 150), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), 2)

        # thresholdEye = cv2.resize(thresholdEye, None, fx=5, fy=5)
        #
        # eye = cv2.resize(gray_eye, None, fx=5, fy=5)
        #
        # eye = cv2.flip(eye, 1)
        # cv2.imshow("Eye", eye)
        # cv2.imshow('ThresEye', thresholdEye)
        # cv2.imshow("Left", leftSideThreshold)

    # if frames == 27:
    #     letter_index += 1
    #     frames = 0
    # if letter_index == 27:
    #     letter_index = 0

    for i in range(27):
        # if i == letter_index:
        #     li = True
        # else:
        #     li = False
        drawLetterRec(i, key_set_1[i])
    cv2.putText(board, text, (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, 0, 2)
    cv2.imshow("Frame", frame)
    cv2.imshow("Virtual Keyboard", keybord)
    cv2.imshow("Board", board)
    key = cv2.waitKey(1)
    if key == 27:
        break
print(count)
cap.release()
cv2.destroyAllWindows()
