import numpy as np
import pandas as pd
import plotly.graph_objs as go
from numba import jit
import plotly
from plotly.offline import init_notebook_mode
init_notebook_mode(connected=True)

# https://blog.datalore.io/how_to_plot_mandelbrot_set/


def get_plane_points(x, y_res=500, z_res=500, y_min=-10, y_max=10, z_min=-10, z_max=10):
    y = np.linspace(y_min, y_max, y_res)
    z = np.linspace(z_min, z_max, z_res)
    x, y, z = np.meshgrid(x, y, z)

    x, y, z = x.reshape(-1), y.reshape(-1) , z.reshape(-1)

    P = np.vstack((x, y, z)).T
    return P


def get_directions(P):
    v = np.array(P - 0)
    v = v/np.linalg.norm(v, axis=1)[:, np.newaxis]
    return v


@jit
def DistanceEstimator(positions, plane_loc, iterations, degree):
    m = positions.shape[0]

    x, y, z = np.zeros(m), np.zeros(m), np.zeros(m)
    x0, y0, z0 = positions[:, 0], positions[:, 1], positions[:, 2]

    dr = np.zeros(m) + 1
    r = np.zeros(m)

    theta = np.zeros(m)
    phi = np.zeros(m)
    zr = np.zeros(m)

    for _ in range(iterations):
        r = np.sqrt(x * x + y * y + z * z)

        dx = .01
        x_loc = plane_loc
        idx = (x < x_loc + dx) & (x > x_loc - dx)
        dr[idx] = np.power(r[idx], degree - 1) * degree * dr[idx] + 1.0

        theta[idx] = np.arctan2(np.sqrt(x[idx] * x[idx] + y[idx] * y[idx]), z[idx])
        phi[idx] = np.arctan2(y[idx], x[idx])

        zr[idx] = r[idx] ** degree
        theta[idx] = theta[idx] * degree
        phi[idx] = phi[idx] * degree

        x[idx] = zr[idx] * np.sin(theta[idx]) * np.cos(phi[idx]) + x0[idx]
        y[idx] = zr[idx] * np.sin(theta[idx]) * np.sin(phi[idx]) + y0[idx]
        z[idx] = zr[idx] * np.cos(theta[idx]) + z0[idx]

    return 0.5 * np.log(r) * r / dr


def trace(directions, plane_location, max_steps=50, iterations=50, degree=8):
    total_distance = np.zeros(directions.shape[0])
    keep_iterations = np.ones_like(total_distance)
    steps = np.zeros_like(total_distance)

    for _ in range(max_steps):
        positions = total_distance[:, np.newaxis] * directions
        distance = DistanceEstimator(positions, plane_location, iterations, degree)
        total_distance += distance * keep_iterations
        steps += keep_iterations

    # return 1 - (steps / max_steps) ** power
    return total_distance


def run():
    plane_location = 2
    plane_points = get_plane_points(x=plane_location)
    directions = get_directions(plane_points)
    distance = trace(directions, plane_location)

    return distance


# plotly_trace = go.Heatmap(z=np.array(plot_mandelbulb()))
#
# data = [plotly_trace]
#
# layout = go.Layout(
#     title='Mandelbrot Plot',
#     width=1250,
#     height=1250,
# )
#
# fig = go.Figure(data=data, layout=layout)
#
# plotly.offline.plot(fig, filename="MandelBulb.html")
