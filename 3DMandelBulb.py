import numpy as np
import pandas as pd
import plotly.graph_objs as go
from numba import jit
import plotly
from plotly.offline import init_notebook_mode
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


def trace(start, directions, max_steps, min_distance, iterations, degree, bailout, power):
    total_distance = np.zeros(directions.shape[0])
    keep_iterations = np.ones_like(total_distance)
    steps = np.zeros_like(total_distance)
    for _ in range(max_steps):
        positions = start[np.newaxis, :] + total_distance[:, np.newaxis] * directions
        distance = DistanceEstimator(positions, iterations, degree, bailout)
        keep_iterations[distance < min_distance] = 0
        total_distance += distance * keep_iterations
        steps += keep_iterations
    return 1 - (steps/max_steps)**power


def get_directions(P, Q):
    v = np.array(P - Q)
    v = v/np.linalg.norm(v, axis=1)[:, np.newaxis]
    return v


def plot_mandelbulb(degree=8, observer_position=np.array([1., 1., 3.]), max_steps=32, iterations=32, bailout=32000, min_distance=5e-3, zoom=0, power=0.2, width=500, height=500, x_size=500, y_size=500, span=[1.2, 1.2], center=[0, 0]):
    plane_points = get_plane_points(observer_position, center=center, span=span, zoom=zoom, width=width, height=height)
    directions = get_directions(plane_points, observer_position)
    image = trace(observer_position, directions, max_steps, min_distance, iterations, degree, bailout, power)
    image = image.reshape(width, height)
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #     print(pd.DataFrame(image))
    # p = ggplot() \
    #     + geom_image(image) + ggsize(x_size, y_size) \
    #     + theme(legend_position='none', axis_ticks='blank', axis_line='blank', axis_title='blank', axis_text='blank')
    return image


np.array(plot_mandelbulb())

plotly_trace = go.Heatmap(z=np.array(plot_mandelbulb()))

data = [plotly_trace]

layout = go.Layout(
    title='Mandelbrot Plot',
    width=1250,
    height=1250,
)

fig = go.Figure(data=data, layout=layout)

plotly.offline.plot(fig, filename="MandelBulb.html")
