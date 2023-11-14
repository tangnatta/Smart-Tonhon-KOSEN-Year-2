import glob
import sys
import numpy as np
from matplotlib.widgets import Button
import matplotlib.pyplot as plt
import matplotlib
import random
import time

matplotlib.use('TkAgg')

fig = plt.figure(facecolor='k')
win = fig.canvas.manager.window  # figure window
screen_res = win.wm_maxsize()  # used for window formatting later
dpi = 200.0  # figure resolution
fig.set_dpi(dpi)  # set figure resolution

# polar plot attributes and initial conditions
ax = fig.add_subplot(111, polar=True, facecolor='#006d70')
ax.set_position([-0.05, -0.05, 1.1, 1.05])
r_max = 400.0  # can change this based on range of sensor
ax.set_ylim([0.0, r_max])  # range of distances to show
ax.set_xlim([0.0, np.pi*2])  # limited by the servo span (0-180 deg)
ax.tick_params(axis='both', colors='w')
ax.grid(color='w', alpha=0.5)  # grid color
ax.set_rticks(np.linspace(0.0, r_max, 5))  # show 5 different distances
ax.set_thetagrids(np.linspace(0.0, 180.0, 10))  # show 10 angles
angles = np.arange(0, 361, 1)  # 0 - 180 degrees
theta = angles*(np.pi/180.0)  # to radians
dists = np.ones((len(angles),))  # dummy distances until real data comes in
pols, = ax.plot([], linestyle='', marker='o', markerfacecolor='w',
                markeredgecolor='#EFEFEF', markeredgewidth=1.0,
                markersize=10.0, alpha=0.9)  # dots for radar points
line1, = ax.plot([], color='w',
                 linewidth=4.0)  # sweeping arm plot

# figure presentation adjustments
fig.set_size_inches(0.8*(screen_res[0]/dpi), 1.5*(screen_res[1]/dpi))
plot_res = fig.get_window_extent().bounds  # window extent for centering
win.wm_geometry('+{0:1.0f}+{1:1.0f}'.
                format((screen_res[0]/2.0)-(plot_res[2]/2.0),
                       (screen_res[1]/2.0)-(plot_res[3]/2.0)))  # centering plot
fig.canvas.toolbar.pack_forget()  # remove toolbar for clean presentation
fig.canvas.set_window_title('Arduino Radar')

fig.canvas.draw()  # draw before loop
axbackground = fig.canvas.copy_from_bbox(
    ax.bbox)  # background to keep during loop

fig.show()

while True:
    # angle = random.randint(0, 180)  # random angle for testing

    # pols.set_data(theta, dists)
    # fig.canvas.restore_region(axbackground)
    # ax.draw_artist(pols)

    # line1.set_data(np.repeat((angle*(np.pi/180.0)), 2),
    #                np.linspace(0.0, r_max, 2))
    # ax.draw_artist(line1)

    fig.canvas.blit(ax.bbox)  # replot only data
    fig.canvas.flush_events()  # flush for next plot

    time.sleep(1)
