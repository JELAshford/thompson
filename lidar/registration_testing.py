# Make a gui to show the resistration process. 
# First, just see how well it works
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

from pycpd import AffineRegistration, RigidRegistration, DeformableRegistration
from functools import partial
import numpy as np
import json


def visualize(iteration, error, X, Y, ax):
    plt.cla()
    ax.scatter(X[:, 0],  X[:, 1], color='red', label='Target')
    ax.scatter(Y[:, 0],  Y[:, 1], color='blue', label='Source')
    plt.text(0.87, 0.92, 'Iteration: {:d}\nQ: {:06.4f}'.format(
        iteration, error), horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize='x-large')
    ax.legend(loc='upper left', fontsize='x-large')
    plt.draw()
    plt.pause(0.001)


BUFFER_SAVE_PATH = "/Users/jamesashford/Data Store/ThompsonData/lidar_scans"
with open(f'{BUFFER_SAVE_PATH}/angle1.json') as set1:
    xs, ys = json.load(set1)
    X = np.array([[x, y] for (x, y) in zip(xs, ys)])
with open(f'{BUFFER_SAVE_PATH}/angle2.json') as set2:
    xs, ys = json.load(set2)
    Y = np.array([[x, y] for (x, y) in zip(xs, ys)])

fig = plt.figure()
fig.add_axes([0, 0, 1, 1])
callback = partial(visualize, ax=fig.axes[0])

reg = AffineRegistration(**{'X': X, 'Y': Y})
# reg.register(callback)
reg.register()
params = reg.get_registration_parameters()
print(params)
# IT WORKS!

# Use these parameters to transform the target set
Yprime = np.dot(Y, params[0]) + params[1]
plt.scatter(X[:, 0], X[:, 1], c="red")
plt.scatter(Y[:, 0], Y[:, 1], c="cyan")
plt.scatter(Yprime[:, 0], Yprime[:, 1], c="blue")
plt.show()

#TODO; Merge the sets by nearest neighbours
#TODO; Store the params in a way that meaningfully describes the movement