import urllib.request
import torch
import pandas as pd
import cv2
import time
from multiprocessing.pool import ThreadPool
from multiprocessing import cpu_count
import random
import numpy as np
import os
import socket
import requests

# VDO_PATH = os.path.join(os.getcwd(), 'videos')
# BASE_PATH = os.getcwd()

ip = '192.168.137.173'

URL_CAM1 = "http://"+ip+"/capture"

requests.get(URL_CAM1.split('capture')[0]+'control?var=framesize&val=10')

pool = ThreadPool(processes=cpu_count())

model = torch.hub.load(
    'ultralytics/yolov5',
    'custom',
    path="best-project.onnx"
)

model.conf = 0.50  # NMS confidence threshold/--
model.iou = 0.45  # NMS IoU threshold
# model.agnostic = False  # NMS class-agnostic
# model.multi_label = False  # NMS multiple labels per box
# (optional list) filter by class, i.e. = [0, 15, 16] for COCO persons, cats and dogs
model.classes = [0]
model.max_det = 1000  # maximum number of detections per image
# model.amp = False  # Automatic Mixed Precision (AMP) inference


def run(model, img):
    # results = model(img, size=640)
    results = model(img)
    # results.save()
    return results

color_name_dic = {}

def draw_box(img, x1, y1, x2, y2, color):
    return cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)


def draw_text(img, x, y, text, color):
    return cv2.putText(img, text, (x+5, y+17), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)


def draw_every_box(img, results):
    for i in range(len(results)):
        x1 = int(results.iloc[i]['xmin'])
        y1 = int(results.iloc[i]['ymin'])
        x2 = int(results.iloc[i]['xmax'])
        y2 = int(results.iloc[i]['ymax'])
        try:
            color = color_name_dic[results.iloc[i]['name']]
        except:
            color = (random.randint(0, 255), random.randint(
                0, 255), random.randint(0, 255))
            color_name_dic[results.iloc[i]['name']] = color
        # color = (0, 0, 255)
        img = draw_box(img, x1, y1, x2, y2, color)
        img = draw_text(
            img, x1, y1, results.iloc[i]['name']+":"+str(results.iloc[i]['confidence'])[:4], color)
    return img


def get_img_from_url(url):
    error_time = 0
    while True:
        req = urllib.request.urlopen(url)

        if req.getcode() != 200:
            if error_time > 2:
                break
            continue
        else:
            error_time = 0

        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)

        frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)  # 'Load it as it is'
        return frame


# camera = cv2.VideoCapture(0)


def crop_img(img, x_center, y_center, w, h):
    x_center = round(x_center)
    y_center = round(y_center)
    w /= 2
    w = round(w)
    h /= 2
    h = round(h)
    return img[x_center-w:x_center+w, y_center-h:y_center+h, :]


# all_time = 0
# round_time = 0
# if not os.path.exists(PIC_PATH):
#     # assert False, "Path does not exist"
#     os.makedirs(PIC_PATH, exist_ok=True)
# os.chdir(PIC_PATH)

# if not os.path.exists(VDO_PATH):
#     # assert False, "Path does not exist"
#     os.makedirs(VDO_PATH, exist_ok=True)
# os.chdir(VDO_PATH)

first_time = True

while True:
    # for i in range(round):
    # Capture frame-by-frame

    start = time.time()

    frame = pool.apply_async(get_img_from_url, args=(URL_CAM1,))

    frame = frame.get()

    # frame = pool.apply_async(cv2.resize, args=(
    #     frame, (round(frame.shape[1]*0.8), round(frame.shape[0]*0.8)), cv2.INTER_AREA))

    results = pool.apply_async(
        run, args=(model, frame[:, :, ::-1]))

    results = results.get()

    frame = pool.apply_async(draw_every_box, args=(
        frame, results.pandas().xyxy[0]))

    frame = frame.get()

    cv2.imshow('image', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # VDO_Writer.release()
        # os.chdir(BASE_PATH)
        break

    # all_time += time.time()-start

    print(results.pandas().xyxy[0])
    # print(results_person.pandas().xyxy[0])
    print("FPS: ", (1/(time.time()-start)))
    # round_time += 1
    # print("Avg. FPS", 1/(all_time/round_time))

# camera.release()
# VDO_Writer.release()
cv2.destroyAllWindows()
