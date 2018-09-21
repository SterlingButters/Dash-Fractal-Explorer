import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, State, Input

import plotly.graph_objs as go
import numpy as np
from numba import jit
from textwrap import dedent as d
TODO: Fix aspect ratio

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

app = dash.Dash()
app.config['suppress_callback_exceptions'] = True

#######################################################################################################################

@jit
def mandelbrot(c, maxiter, threshold=2):
    z = c
    for n in range(maxiter):
        if abs(z) > threshold:
            return n
        z = z * z + c
    return 0


@jit
def mandelbrot_set(xmin, xmax, ymin, ymax, maxiter=250, width=1500, height=1500):
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    n3 = np.empty((width, height))
    for i in range(width):
        for j in range(height):
            n3[i, j] = mandelbrot(r1[i] + 1j*r2[j], maxiter)
    return r1, r2, n3

#######################################################################################################################


x, y, z = mandelbrot_set(-2.0, 0.5, -1.25, 1.25)
trace = go.Heatmap(x=x,
                   y=y,
                   z=z.T)

data = [trace]

layout = go.Layout(
    title='Mandelbrot Plot',
    width=1250,
    height=1250,
    )

fig = go.Figure(data=data, layout=layout)

################################################################################

app.layout = html.Div([
################################################################################
    # Title
    html.H2('Zoom Application',
                style={
                    'position': 'relative',
                    'top': '0px',
                    'left': '10px',
                    'font-family': 'Dosis',
                    'display': 'inline',
                    'font-size': '4.0rem',
                    'color': '#4D637F'
                }),
        html.H2('for',
                style={
                    'position': 'relative',
                    'top': '0px',
                    'left': '20px',
                    'font-family': 'Dosis',
                    'display': 'inline',
                    'font-size': '2.0rem',
                    'color': '#4D637F'
                }),
        html.H2('MandelBrot',
                style={
                    'position': 'relative',
                    'top': '0px',
                    'left': '27px',
                    'font-family': 'Dosis',
                    'display': 'inline',
                    'font-size': '4.0rem',
                    'color': '#4D637F'
                }),

    ################################################################################
    html.Br(),

    html.Div([

        dcc.Graph(
            id='graph',
            figure=fig
                ),

        dcc.Slider(
            id='iterations',
            min=0,
            max=500,
            marks={
                0: {'label':     '0'},
                50: {'label':    '50'},
                100: {'label':   '100'},
                150: {'label':   '150'},
                200: {'label':   '200'},
                250: {'label':   '250'},
                300: {'label':   '300'},
                350: {'label':   '350'},
                400: {'label':   '400'},
                450: {'label':   '450'},
                500: {'label':   '500'},
            },
            value=250,
        ),

        # html.Div([
        #     dcc.Markdown(d("""
        #         **Zoom and Relayout Data**
        #
        #         Click and drag on the graph to zoom or click on the zoom
        #         buttons in the graph's menu bar.
        #         Clicking on legend items will also fire
        #         this event.
        #     """)),
        #     html.Pre(id='relayout-data', style=styles['pre']),
        # ], className='three columns')
        #
        #     ])
    ])
])


@app.callback(
    # Output('relayout-data', 'children'),
    Output('graph', 'figure'),
    [Input('iterations', 'value'),
     Input('graph', 'relayoutData')])
def display_selected_data(iterations, relayoutData):
    xmin = relayoutData['xaxis.range[0]']
    xmax = relayoutData['xaxis.range[1]']
    ymin = relayoutData['yaxis.range[0]']
    ymax = relayoutData['yaxis.range[1]']

    x, y, z = mandelbrot_set(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, maxiter=iterations)
    trace = go.Heatmap(x=x,
                       y=y,
                       z=z.T)

    data = [trace]

    layout = go.Layout(
        title='Mandelbrot Plot',
        width=1250,
        height=1250,
    )

    fig = go.Figure(data=data, layout=layout)

    return fig
################################################################################


if __name__ == '__main__':
    app.run_server(debug=True)
