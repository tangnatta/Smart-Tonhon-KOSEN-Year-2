import numpy as np
import matplotlib.pyplot as plt
import time
import random
from PIL import Image
from polar2xy import polar2xy, xywh_mid2xywh, xxyy2xywh, theta2rad
from esp32_api import getDistance, getHeading, changeStepper, buzzer_mode, setBuzzer
import requests
import json
from math import floor

ai_url = "http://127.0.0.1:54321/results"
frame_size = [1600, 1200]

plt.style.use('ggplot')

angles = np.arange(0, 360, 1)  # 0 - 360 degrees
theta = angles*(np.pi/180.0)  # to radians
dists = np.zeros((len(angles),))  # dummy distances until real data comes in

fig = plt.figure(figsize=(5, 5), facecolor='k')
ax = fig.add_subplot(polar=True, facecolor='#0373bb')
# ax.set_position([-0.05, -0.05, 1.1, 1.05])
r_max = 400.0  # can change this based on range of sensor
ax.set_ylim([0.0, r_max])  # range of distances to show
ax.set_xlim([0.0, np.pi*2])  # limited by the servo span (0-180 deg)
ax.tick_params(axis='both', colors='w')
ax.grid(color='w', alpha=0.5)  # grid color
ax.set_rticks(np.linspace(0.0, r_max, 5))  # show 5 different distances
ax.set_thetagrids(np.linspace(0.0, 320.0, 9))  # show 10 angles

pols, = ax.plot([], linestyle='dashed', linewidth=1.0, marker='o', markerfacecolor='w',
                markeredgecolor='#eb5436', markeredgewidth=0.5,
                markersize=2.0, alpha=1.0)  # dots for radar points
line1, = ax.plot([], color='w',
                 linewidth=2.0)  # sweeping arm plot

fig.canvas.toolbar.pack_forget()  # remove toolbar for clean presentation
fig.canvas.manager.set_window_title('Arduino Radar')  # name of the window

ship = fig.add_axes([0, 0, 0, 0], polar=False, zorder=1)
ship.axis('off')

pirate = fig.add_axes([0, 0, 0, 0], polar=False, zorder=1)
pirate.axis('off')

axbackground = fig.canvas.copy_from_bbox(
    ax.bbox)  # background to keep during loop

figbackground = fig.canvas.copy_from_bbox(
    fig.bbox)  # background to keep during loop


# fig.canvas.draw()  # draw before loop

plt.show(block=False)

# ax.plot(angles, alice)

pirate_pic = Image.open('pirate.png')
ship_pic = Image.open('ship.png')

print(theta)
print("--------")
print(dists)

round_time = 0
ship_time = 0

while True:
    if ship_time > 10:
        fig.canvas.restore_region(figbackground)
        ship_time = 0
    else:
        fig.canvas.restore_region(axbackground)

    # angle = random.randint(0, 360)  # random angle for testing
    # distance = random.randint(0, 400)  # random distance for testing

    angle = getHeading()
    distance = getDistance()

    if (distance < 100):
        setBuzzer(buzzer_mode.FAST)
    elif (distance < 200):
        setBuzzer(buzzer_mode.NORMAL)
    elif (distance < 300):
        setBuzzer(buzzer_mode.SLOW)
    else:
        setBuzzer(buzzer_mode.STOP)

    pirate_angle, ship_angle = angle, angle

    pirate_w, pirate_h = 0, 0
    ship_w, ship_h = 0, 0

    response = requests.get(ai_url).content
    ai_object = json.loads(response)
    print(ai_object)
    # if len(ai_object) == 0:
    #     for i in range(0, 2):
    #         response = requests.get(ai_url).content
    #         ai_object = json.loads(response)
    #         print(i, ai_object)
    #         if len(ai_object) != 0:
    #             break

    ai_object.sort(key=lambda x: x["confidence"])
    # print(ai_object)

    for i in ai_object:
        xmin = i['xmin']
        ymin = i['ymin']
        xmax = i['xmax']
        ymax = i['ymax']
        confidence = i['confidence']
        classes = i['class']
        name = i['name']
        x, y, w, h = xxyy2xywh(xmin, ymin, xmax, ymax)
        shift_angle = angle + ((x-frame_size[0]/2)*30/(frame_size[0]/2))
        w, h = 0.08+(w/(frame_size[0]*4)), 0.08+(h/(frame_size[1]*4))
        dis = distance if distance <= 480 else 480
        if name == "pirate-ship":
            pirate_angle = shift_angle
            pirate_w, pirate_h = w, h
            pirate_x, pirate_y = polar2xy((dis/400)*0.37, pirate_angle)
            print(f"pirate x: {pirate_x}, y: {pirate_y}")
            pirate.set_position(xywh_mid2xywh(
                0.5+pirate_x, 0.5+pirate_y, pirate_w, pirate_h))
            pirate.imshow(pirate_pic)
            ship_time = 0

        elif name == "ship":
            ship_angle = shift_angle
            ship_w, ship_h = w, h
            ship_x, ship_y = polar2xy((dis/400)*0.37, ship_angle)
            print(f"ship x: {ship_x}, y: {ship_y}")
            ship.set_position(xywh_mid2xywh(
                0.5+ship_x, 0.5+ship_y, ship_w, ship_h))
            ship.imshow(ship_pic)
            ship_time = 0

    print("angle: ", angle)
    print("distance: ", distance)

    dists[floor(angle)] = distance  # update distance for current angle

    pols.set_data(theta, dists)  # plot the line of the radar

    line1.set_data(np.repeat((angle*(np.pi/180.0)), 2),
                   np.linspace(0.0, r_max, 2))  # plot detecting line

    fig.canvas.draw()

    fig.canvas.blit(ax.bbox)  # replot only data
    fig.canvas.flush_events()  # flush for next plot

    start = time.time()

    changeStepper(40)  # rotate to next detection angle

    print("time: ", time.time()-start)
    print("round time: ", round_time, "ship time: ", ship_time)
    round_time += 1
    ship_time += 1
    if round_time >= 100:
        round_time = 0
        dists = np.zeros((len(angles),))
        # time.sleep(1)

    # time.sleep(1)
