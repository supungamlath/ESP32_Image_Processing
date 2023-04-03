import time
import cv2
import urllib.request
import urllib.parse
import numpy as np
from line_follow import detect_centering, detect_color_squares, detect_lines
from data_transfer import send_control_packet

url = 'http://192.168.230.24'

mode = 0
# used to record the time when we processed last frame
prev_frame_time = 0

# used to record the time at which we processed current frame
new_frame_time = 0

params = {
    "left": "0",
    "right": "0",
    "gimbal": "142"
}


def setLeftSpeed(left_speed):
    params["left"] = str(left_speed)


def setRightSpeed(right_speed):
    params["right"] = str(right_speed)


while True:
    new_frame_time = time.time()
    query_string = urllib.parse.urlencode(params, encoding='utf-8')
    img_resp = urllib.request.urlopen(url + '/stream?' + query_string)
    imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
    frame = cv2.imdecode(imgnp, -1)
    frame = cv2.flip(frame, 1)

    # if not detect_color_squares(frame):
    # detect_lines(frame)
    line = detect_centering(frame)
    if line:
        cx, cy = line
        if cx >= 200:
            setLeftSpeed(0)
            setRightSpeed(150)
            print("Turn Left")
        if cx < 180 and cx > 140:
            setLeftSpeed(150)
            setRightSpeed(150)
            print("Go Straight")
        if cx <= 150:
            setLeftSpeed(150)
            setRightSpeed(0)
            print("Turn Right")
    else:
        setLeftSpeed(0)
        setRightSpeed(0)
        print("No Line")

    # send_control_packet(url, {'left': -255, 'right': 255, 'gimbal': 100})

    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
    fps = str(int(fps))

    # Display the resulting frame
    cv2.putText(frame, fps, (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 0, 255), 1, cv2.LINE_AA)
    cv2.putText(frame, params["left"], (10, 220), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(frame, params["right"], (290, 220), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.imshow('frame', frame)

    key = cv2.waitKey(5)
    if key == ord('w'):
        setLeftSpeed(int(params["left"]) + 10)
        setRightSpeed(int(params["right"]) + 10)
    if key == ord('s'):
        setLeftSpeed(int(params["left"]) - 10)
        setRightSpeed(int(params["right"]) - 10)
    if key == ord('q'):
        break

cv2.destroyAllWindows()
