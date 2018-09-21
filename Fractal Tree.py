# from pysvg.builders import *
from math import pi as PI
from math import sin, cos
import random

root = 0

from plotly.graph_objs import *
import plotly.plotly as py
import plotly.tools as tls


# color the tree with a gradient from root_col to tip_col
# interpolate linearly to get color at a given position in the gradient
def get_col(root_col, tip_col, iterat):
    r = int((iterat * 1.0 / root) * (root_col[0] - tip_col[0])) + tip_col[0]
    g = int((iterat * 1.0 / root) * (root_col[1] - tip_col[1])) + tip_col[1]
    b = int((iterat * 1.0 / root) * (root_col[2] - tip_col[2])) + tip_col[2]
    return '#%02x%02x%02x' % (r, g, b)


# just testing commit.
def fractal_tree(lines, iterat, origin, t, r, theta, dtheta, root_col, tip_col, randomize=False):
    """
    draws branches
    iterat:     iteratation number, stop when iterat == 0
    origin:   x,y coordinates of the start of this branch
    t:        current trunk length
    r:        factor to contract the trunk each iteratation
    theta:    starting orientation
    dtheta:   angle of the branch
    """
    if iterat == 0:
        return lines
    # render the branch
    x0, y0 = origin

    # randomize the length
    randt = random.random() * t
    if randomize:
        x, y = x0 + randt * cos(theta), y0 - randt * sin(theta)
    else:
        x, y = x0 + cos(theta), y0 - sin(theta)
    # color the branch according to its position in the tree
    col = get_col(root_col, tip_col, iterat)
    # add to traces
    lines.append(Scatter(x=[x0, x], y=[y0, y], mode='lines', line=Line(color=col, width=1)))
    # recursive calls
    if randomize:
        fractal_tree(lines, iterat - 1, (x, y), t * r, r,
                     theta + (random.random()) * (iterscale / (iterat + 1)) * dtheta, dtheta, root_col, tip_col,
                     randomize)
        fractal_tree(lines, iterat - 1, (x, y), t * r, r,
                     theta - (random.random()) * (iterscale / (iterat + 1)) * dtheta, dtheta, root_col, tip_col,
                     randomize)
    else:
        fractal_tree(lines, iterat - 1, (x, y), t * r, r, theta + dtheta, dtheta, root_col, tip_col, randomize)
        fractal_tree(lines, iterat - 1, (x, y), t * r, r, theta - dtheta, dtheta, root_col, tip_col, randomize)


for i in range(30):
    # angle to radian factor
    ang2rad = PI / 180.0
    # experiment with number of iteratations (try 4 to 14)
    iterat = 12
    # experiment with trunk length (try 120)
    t = 120
    # experiment with factor to contract the trunk each iteratation (try 0.7)
    r = 0.7
    # starting orientation (initial 90 deg)
    theta = 90.0 * ang2rad
    # experiment with angle of the branch (try 18 deg)
    dtheta = 18.0 * ang2rad
    # experiment with gradient color choices
    root_col = (40, 40, 40)
    tip_col = (250, 250, 250)
    # experiment with factor to increase random angle variation as child branches get smaller
    iterscale = 6.0
    # center of bottom
    origin = (250, 500)
    root = iterat
    # make the tree
    lines = []
    fractal_tree(lines, iterat, origin, t, r, theta, dtheta, root_col, tip_col, True)

    # group the lines by similar color
    branches = {}
    for line in lines:
        color = line['line']['color']
        if color not in branches:
            branches[color] = line
        else:
            branches[color]['x'].extend(line['x'])
            branches[color]['y'].extend(line['y'])
            branches[color]['x'].append(None)
            branches[color]['y'].append(None)

    branch_data = [branches[c] for c in branches]

    layout = Layout(yaxis=YAxis(autorange='reversed'),
                    width=500, height=800, showlegend=False)
    fig = Figure(data=Data(branch_data), layout=layout)
    py.iplot(fig, filename='random fractal tree #{}'.format(i + 1))