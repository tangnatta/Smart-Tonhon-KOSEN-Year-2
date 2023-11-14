import numpy as np


def theta2rad(theta):
    return theta/180.0*np.pi


def polar2xy(r, theta):
    x = r * np.cos(theta2rad(theta))
    y = r * np.sin(theta2rad(theta))
    return x, y


def xy2polar(x, y):
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    return r, theta


def xxyy2xywh(x1, y1, x2, y2):
    x = (x1 + x2) / 2
    y = (y1 + y2) / 2
    w = x2 - x1
    h = y2 - y1
    return x, y, w, h


def xywh_mid2xywh(x, y, w, h):
    x = x - w/2
    y = y - h/2
    w = w
    h = h
    return x, y, w, h
