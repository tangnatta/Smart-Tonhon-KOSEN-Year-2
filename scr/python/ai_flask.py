from datetime import datetime
from flask import Flask, render_template, Response, request
import cv2
import logging
from ai_func import *
from multiprocessing.pool import ThreadPool
from multiprocessing import cpu_count
import requests
import torch

ip = '192.168.137.99'

# logging.basicConfig(filename="ai_flask" +
#                     str(datetime.now().strftime("%d-%m-%Y_%H.%M.%S"))+".log")

# logger = logging.getLogger()

app = Flask(__name__)

URL_CAM1 = "http://"+ip+"/capture"

# URL_CAM1 = "http://127.0.0.1:12345/frame1"

pool = ThreadPool(processes=cpu_count())

model = torch.hub.load(
    'ultralytics/yolov5',
    'custom',
    path="mb-best-project-m.onnx"
)

model.conf = 0.65  # NMS confidence threshold/--
model.iou = 0.45  # NMS IoU threshold
# model.agnostic = False  # NMS class-agnostic
# model.multi_label = False  # NMS multiple labels per box
# (optional list) filter by class, i.e. = [0, 15, 16] for COCO persons, cats and dogs
# model.classes = [0]
model.max_det = 1000  # maximum number of detections per image
# model.amp = False  # Automatic Mixed Precision (AMP) inference


@app.route('/results')
def results():
    frame = pool.apply_async(get_img_from_url, args=(URL_CAM1,))

    frame = frame.get()

    # frame = pool.apply_async(cv2.resize, args=(
    #     frame, (round(frame.shape[1]*0.8), round(frame.shape[0]*0.8)), cv2.INTER_AREA))

    results = pool.apply_async(
        run, args=(model, frame[:, :, ::-1]))

    results = results.get()

    # frame = pool.apply_async(draw_every_box, args=(
    #     frame, results.pandas().xyxy[0]))

    # frame = frame.get()
    return Response(response=results.pandas().xyxy[0].to_json(orient="records"), mimetype='application/json')


def results_frame():
    frame = pool.apply_async(get_img_from_url, args=(URL_CAM1,))

    frame = frame.get()

    results = pool.apply_async(
        run, args=(model, frame[:, :, ::-1]))

    results = results.get()

    frame = pool.apply_async(draw_every_box, args=(
        frame, results.pandas().xyxy[0]))

    frame = frame.get()
    ret, buffer = cv2.imencode(
        '.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 100])
    frame = buffer.tobytes()
    return (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


def results_stream():
    while True:
        yield results_frame()


@app.route('/stream')
def stream():
    return Response(response=results_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/image')
def image():
    return Response(response=results_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    requests.get(URL_CAM1.split('capture')[0]+'control?var=framesize&val=10')
    app.run(host='0.0.0.0', port=54321, debug=False)
