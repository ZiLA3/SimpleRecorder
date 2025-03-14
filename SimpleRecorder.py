import cv2 as cv
from datetime import datetime

keyMap = {"ESC" : 27 , "Space" : 32, "Tab" : 9}
now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
is_recording = False
is_negative = False

def set_time():
    global now_time
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def input_key(event_key):
    global is_recording, is_negative

    if event_key is keyMap["ESC"]:
        return False

    elif event_key is keyMap["Space"]:
        is_recording = not is_recording
        if is_recording:
            ready_record()
        else:
            recording_video.release()

    elif event_key is keyMap["Tab"]:
        is_negative = not is_negative

    return True

def ready_record():
    global recording_video

    file_name = f'{now_time}.avi'
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    h, w, _ = img.shape
    color = (img.ndim > 2) and (img.shape[2] > 1)

    recording_video.open(file_name, fourcc, fps, (w, h), color)

def record_video(canvas):
    set_time()
    recording_video.write(canvas)
    record_circle_pos = (24, 24)
    cv.circle(canvas, record_circle_pos, radius=8, color=(0, 0, 255), thickness=-1)


video = cv.VideoCapture(0)
recording_video = cv.VideoWriter()

if video.isOpened():
    fps = video.get(cv.CAP_PROP_FPS)
    wait_time = int(1 / fps * 1000)

    isRecording = False
    key = -1

    while input_key(key):
        valid, img = video.read()
        if not valid:
            break

        img = cv.flip(img, flipCode=1)

        if is_negative:
            img = cv.bitwise_not(img)

        if is_recording:
            record_video(img)

        cv.imshow("Simple Recorder", img)
        key = cv.waitKey(wait_time)

cv.destroyAllWindows()