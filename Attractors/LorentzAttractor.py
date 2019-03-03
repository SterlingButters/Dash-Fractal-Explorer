import numpy as np
import time
import plotly.graph_objs as go
import plotly.tools as tls
from plotly.offline import init_notebook_mode, plot
from scipy.spatial.distance import cdist

init_notebook_mode(True)


# stream_id = tls.get_credentials_file()['stream_ids']
# token = stream_id[-1]
# stream_id = dict(token=token)
# cone = go.Cone(stream=stream_id)


def lorenz(x, y, z, s=10, r=20, b=2.667):
    x_dot = s * (y - x)
    y_dot = r * x - y - x * z
    z_dot = x * y - b * z
    return x_dot, y_dot, z_dot


dt = 0.01
stepCnt = 1000

# Need one more for the initial values
xs = np.empty((stepCnt + 1,))
ys = np.empty((stepCnt + 1,))
zs = np.empty((stepCnt + 1,))

# Setting initial values
xs[0], ys[0], zs[0] = (0., 1., 1.05)

# Stepping through "time".
for i in range(stepCnt):
    # Derivatives of the X, Y, Z state
    x_dot, y_dot, z_dot = lorenz(xs[i], ys[i], zs[i])
    xs[i + 1] = xs[i] + (x_dot * dt)
    ys[i + 1] = ys[i] + (y_dot * dt)
    zs[i + 1] = zs[i] + (z_dot * dt)

attractor = go.Scatter3d(x=xs,
                         y=ys,
                         z=zs,
                         mode='lines',
                         opacity=0.6,
                         line=dict(color='#00FFFF')
                         )

frames = []
for k in range(stepCnt - 1):
    print(k)
    v = np.array([xs[k + 1], ys[k + 1], zs[k + 1]]) - np.array([xs[k], ys[k], zs[k]])
    v = v / np.linalg.norm(v)

    # frame_data = go.Cone(x=[xs[k]],
    #                      y=[ys[k]],
    #                      z=[zs[k]],
    #                      u=[v[0]],
    #                      v=[v[1]],
    #                      w=[v[2]],
    #                      sizeref=3
    #                      )

    frame_data = go.Scatter3d(x=[xs[k]],
                              y=[ys[k]],
                              z=[zs[k]],
                              mode='markers')

    frame = dict(data=[frame_data])
    frames.append(frame)

layout = go.Layout(title='Curve',
                   updatemenus=[{'type': 'buttons',
                                 'buttons': [{'label': 'Play',
                                              'method': 'animate',
                                              'args': [None, {'frame':
                                                                  {'duration': 1000, 'redraw': False},
                                                              'transition':
                                                                  {'duration': 1000,
                                                                   'easing': 'quadratic-in-out'}
                                                              }]
                                              }]}]
                   )

data = [attractor, attractor]

fig = go.Figure(data=data, layout=layout, frames=frames)

plot(fig, auto_open=True)

# s = py.Stream(stream_id=token)
# s.open()
# sleep_time = .001
# i = 0
# while i < stepCnt - 1:
#     v = np.array([xs[i + 1], ys[i + 1], zs[i + 1]]) - np.array([xs[i], ys[i], zs[i]])
#     v = v / np.linalg.norm(v)
#
#     s.write(go.Cone(x=[xs[i]],
#                     y=[ys[i]],
#                     z=[zs[i]],
#                     u=[v[0]],
#                     v=[v[1]],
#                     w=[v[2]])
#             )
#     time.sleep(sleep_time)
#     i += 1
