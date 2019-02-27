import numpy as np
import pandas as pd
import plotly.graph_objs as go
from numba import jit
import plotly
from plotly.offline import init_notebook_mode, plot
init_notebook_mode(connected=True)

# https://blog.datalore.io/how_to_plot_mandelbrot_set/


def get_boundaries(center, span, zoom):
    return center - span/2.**zoom, center + span/2.**zoom


def get_plane_points(Q, center, span, zoom, width, height, eps=1e-4):
    x_min, x_max = get_boundaries(center[0], span[0], zoom)
    y_min, y_max = get_boundaries(center[1], span[1], zoom)
    a, b, c = Q
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    x, y = np.meshgrid(x, y)
    x, y = x.reshape(-1), y.reshape(-1)
    if np.abs(c) > eps:
        z = -(a*x + b*y)/c
        P = np.vstack((x, y, z)).T
    elif np.abs(a) > eps:
        z = -(c*x + b*y)/a
        P = np.vstack((z, y, x)).T
    elif np.abs(b) > eps:
        z = -(a*x + c*y)/b
        P = np.vstack((x, z, y)).T
    return P


@jit
def DistanceEstimator(positions, iterations, degree=8, bailout=1000):
    m = positions.shape[0]
    x, y, z = np.zeros(m), np.zeros(m), np.zeros(m)
    x0, y0, z0 = positions[:, 0], positions[:, 1], positions[:, 2]
    dr = np.zeros(m) + 1
    r = np.zeros(m)
    theta = np.zeros(m)
    phi = np.zeros(m)
    zr = np.zeros(m)
    for _ in range(iterations):
        r = np.sqrt(x*x + y*y + z*z)
        idx1 = r < bailout
        dr[idx1] = np.power(r[idx1], degree - 1) * degree * dr[idx1] + 1.0

        theta[idx1] = np.arctan2(np.sqrt(x[idx1]*x[idx1] + y[idx1]*y[idx1]), z[idx1])
        phi[idx1] = np.arctan2(y[idx1], x[idx1])

        zr[idx1] = r[idx1] ** degree
        theta[idx1] = theta[idx1] * degree
        phi[idx1] = phi[idx1] * degree

        x[idx1] = zr[idx1] * np.sin(theta[idx1]) * np.cos(phi[idx1]) + x0[idx1]
        y[idx1] = zr[idx1] * np.sin(theta[idx1]) * np.sin(phi[idx1]) + y0[idx1]
        z[idx1] = zr[idx1] * np.cos(theta[idx1]) + z0[idx1]

    return 0.5 * np.log(r) * r / dr


def trace(start, directions, max_steps, min_distance, iterations, degree, bailout):
    total_distance = np.zeros(directions.shape[0])
    keep_iterations = np.ones_like(total_distance)
    steps = np.zeros_like(total_distance)
    for _ in range(max_steps):
        positions = start[np.newaxis, :] + total_distance[:, np.newaxis] * directions
        distance = DistanceEstimator(positions, iterations, degree, bailout)
        keep_iterations[distance < min_distance] = 0
        total_distance += distance * keep_iterations
        steps += keep_iterations

    return total_distance[total_distance < 3] * -directions[total_distance < 3][:, 0],\
           total_distance[total_distance < 3] * -directions[total_distance < 3][:, 1],\
           total_distance[total_distance < 3] * -directions[total_distance < 3][:, 2]


def get_directions(P, Q):
    v = np.array(P - Q)
    v = v/np.linalg.norm(v, axis=1)[:, np.newaxis]
    return v


def plot_mandelbulb(degree=8, observer_position=np.array([3, 0, 0]), max_steps=32, iterations=32, bailout=32000,
                    min_distance=5e-3, zoom=0, width=200, height=200, span=[1.5, 1.5], center=[0, 0],
                    ):

    plane_points = get_plane_points(observer_position, center=center, span=span, zoom=zoom, width=width, height=height)
    directions = get_directions(plane_points, observer_position)
    image = trace(observer_position, directions, max_steps, min_distance, iterations, degree, bailout)
    Xs = observer_position[0] - image[0]
    Ys = observer_position[1] - image[1]
    Zs = observer_position[2] - image[2]
    return Xs, Ys, Zs


xs = []
ys = []
zs = []

for angle in [[3, 0, 0], [0, 3, 0], [0, 0, 3], [-3, 0, 0], [0, -3, 0], [0, 0, -3]]:
    xs_, ys_, zs_ = plot_mandelbulb(degree=9, observer_position=np.array(angle))
    xs.extend(xs_)
    ys.extend(ys_)
    zs.extend(zs_)

xs = np.array(xs)
ys = np.array(ys)
zs = np.array(zs)

bulb = go.Scatter3d(x=xs,
                    y=ys,
                    z=zs,
                    mode='markers',
                    marker=dict(size=1,
                                color=np.sqrt(xs ** 2 + ys ** 2 + zs ** 2),
                                colorscale='Viridis',
                                # size=np.e ** np.sqrt(xs ** 2 + ys ** 2 + zs ** 2),
                                # line=dict(
                                #     color='rgb(204, 204, 204)',
                                #     width=1
                                # ),
                                ),
                    opacity=.7,
                    )

data = [bulb]

layout = go.Layout(
    xaxis=go.layout.XAxis(
        title='x'
    ),
    yaxis=go.layout.YAxis(
        title='y'
    )
)

fig = go.Figure(data=data, layout=layout)
plot(fig, filename='test.html', auto_open=True)
