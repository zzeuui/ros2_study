import numpy as np

n = 3
to_degree = 180/np.pi
to_radian = np.pi/180

gap_theta = 2*np.pi / n #2pi radian = 360 degree
theta = [gap_theta*n for n in range(n)]

r = 3
x = [r*np.cos(th) for th in theta]
y = [r*np.sin(th) for th in theta]

def calc_position(n, r):
    gap_theta = 2*np.pi /n
    theta = [gap_theta*n for n in range(n)]

    x = [r*np.cos(th) for th in theta]
    y = [r*np.sin(th) for th in theta]

    return x, y, theta


