import numpy as np
import plotly.graph_objs as go
from plotly import offline
import pandas as pd
import math
import random

offline.init_notebook_mode(connected=True)

x_res = 50
y_res = 50
z_res = 50
n = 8

# drawing area (xa < xb & ya < yb)
xa = -1.5
xb = 1.5
ya = -1.5
yb = 1.5
za = -1.5
zb = 1.5

maxIt = 100  # max number of iterations allowed
pi2 = math.pi * 2.0
# random rotation angles to convert 2d plane to 3d plane
xy = random.random() * pi2
xz = random.random() * pi2
yz = random.random() * pi2

sxy = math.sin(xy)
cxy = math.cos(xy)
sxz = math.sin(xz)
cxz = math.cos(xz)
syz = math.sin(yz)
cyz = math.cos(yz)

xs = []
ys = []
zs = []

origx = (xa + xb) / 2.0
origy = (ya + yb) / 2.0
origz = (za + zb) / 2.0
for kz in range(z_res):

    c = kz * (zb - za) / (z_res - 1) + za
    for ky in range(y_res):

        b = ky * (yb - ya) / (y_res - 1) + ya
        for kx in range(x_res):

            a = kx * (xb - xa) / (x_res - 1) + xa
            x = a
            y = b
            z = c

            # 3d rotation around center of the plane
            x = x - origx
            y = y - origy

            x0 = x * cxy - y * sxy
            y = x * sxy + y * cxy
            x = x0

            # xy-plane rotation
            x0 = x * cxz - z * sxz
            z = x * sxz + z * cxz
            x = x0

            # xz-plane rotation
            y0 = y * cyz - z * syz
            z = y * syz + z * cyz
            y = y0

            # yz-plane rotation
            x = x + origx
            y = y + origy
            z = z + origz

            cx = x
            cy = y
            cz = z
            for i in range(maxIt):
                r = math.sqrt(x * x + y * y + z * z)
                t = math.atan2(math.hypot(x, y), z)
                p = math.atan2(y, x)
                rn = r ** n
                x = rn * math.sin(t * n) * math.cos(p * n) + cx
                y = rn * math.sin(t * n) * math.sin(p * n) + cy
                z = rn * math.cos(t * n) + cz
                if x * x + y * y + z * z > 4.0:
                    break

                else:
                    xs.append(x)
                    ys.append(y)
                    zs.append(z)

print(pd.DataFrame({'x': xs, 'y': ys, 'z': zs}))

xs = np.array(xs)
ys = np.array(ys)
zs = np.array(zs)

plot = go.Scatter3d(x=xs,
                    y=ys,
                    z=zs,
                    mode='markers',
                    marker=dict(size=1,
                                line=dict(
                                    color='rgb(204, 204, 204)',
                                    width=1
                                ),
                                color=np.sqrt(xs**2 + ys**2 + zs**2),
                                colorscale='Viridis',
                                ),
                    opacity=.7,
                    )

data = [plot]

layout = go.Layout(
    xaxis=go.layout.XAxis(
        title='x'
    ),
    yaxis=go.layout.YAxis(
        title='y'
    )
)
fig = go.Figure(data=data, layout=layout)
offline.plot(fig, filename='cubes.html', auto_open=True)
