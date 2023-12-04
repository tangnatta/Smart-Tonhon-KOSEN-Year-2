import cv2
import numpy as np
import random
import urllib.request


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


def crop_img(img, x_center, y_center, w, h):
    x_center = round(x_center)
    y_center = round(y_center)
    w /= 2
    w = round(w)
    h /= 2
    h = round(h)
    return img[x_center-w:x_center+w, y_center-h:y_center+h, :]
