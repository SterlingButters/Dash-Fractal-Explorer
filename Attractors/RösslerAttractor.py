## The numerical method used is first order forward Euler method.

#############################################
from scipy import *
import numpy as np
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, plot

init_notebook_mode(True)


# We define a function which is going to be the recursive function.
def num_rossler(x, y, z, h, a=0.15, b=0.2, c=6.0):
    x_dot = x + h * (-y - z)
    y_dot = y + h * (x + a * y)
    z_dot = z + h * (b + z * (x - c))
    return x_dot, y_dot, z_dot


# Them the time interval and the step size
h = 0.0001
t_ini = 0
t_fin = 96 * pi
numsteps = int((t_fin - t_ini) / h)

# using this parameters we build the time.
t = linspace(t_ini, t_fin, numsteps)
# And the vectors for the solutions
x = zeros(numsteps)
y = zeros(numsteps)
z = zeros(numsteps)

# We set the initial conditions
x[0] = 0
y[0] = 0
z[0] = 0

# This is the main loop where we use the recursive system to obtain the solution
for k in range(x.size - 1):
    # We use the previous point to generate the new point using the recursion
    [x[k + 1], y[k + 1], z[k + 1]] = num_rossler(x[k], y[k], z[k], t[k + 1] - t[k])

# Now that we have the solution in vectors t,x,y,z is time to plot them.

# We create a figure and 4 axes on it. 3 of the axes are going to be 2D and the fourth one is a 3D plot.

attractor = go.Scatter3d(x=x,
                         y=y,
                         z=z,
                         mode='lines',
                         opacity=0.6,
                         # color='#00FFFF'
                         )

data = [attractor]

fig = go.Figure(data=data)

plot(fig, auto_open=True)

