import dash
import dash_core_components as dcc
import dash_table as dt
import dash_html_components as html

from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate

import plotly.graph_objs as go

sample_data = {
    'series': {
        'data': [
            {'outcome': 'Pain', 'likelihood': 0},
            {'outcome': 'Nausea', 'likelihood': 0},
            {'outcome': 'Constipation', 'likelihood': 1},
            {'outcome': 'Depression', 'likelihood': 0.5},
            {'outcome': 'Insomnia', 'likelihood': 0}
        ],
        'style': {
            'backgroundColor': '#ffffff'
        }
    },
    'series2': {
        'data': [
            {'outcome': 'Pain', 'likelihood': 0},
            {'outcome': 'Nausea', 'likelihood': 0.5},
            {'outcome': 'Constipation', 'likelihood': 0},
            {'outcome': 'Depression', 'likelihood': 1},
            {'outcome': 'Insomnia', 'likelihood': 0}
        ],
        'style': {
            'backgroundColor': '#ffffff'
        }
    }
}

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Multi output example'),
    dcc.Dropdown(id='data-dropdown', options=[
        {'label': 'fake patient 1', 'value': 'series'},
        {'label': 'fake patient 2', 'value': 'series2'},
    ], value='series'),
    html.Div([
        dcc.Graph(id='graph'),
        dt.DataTable(id='data-table', columns=[
            {'name': 'Outcome', 'id': 'outcome'},
            {'name': 'Likelihood', 'id': 'likelihood'}
        ])
    ])
], id='container')


@app.callback([
    Output('graph', 'figure'),
    Output('data-table', 'data'),
    Output('data-table', 'columns'),
    Output('container', 'style')
], [Input('data-dropdown', 'value')])
def multi_output(value):
    if value is None:
        raise PreventUpdate

    selected = sample_data[value]
    data = selected['data']
    columns = [
        {'name': k.capitalize(), 'id': k}
        for k in data[0].keys()
    ]
    figure = go.Figure(
        data=[
            go.Bar(y=[y['likelihood']], text=y['outcome'], name=y['outcome'])
            for y in data
        ]
    )

    figure.update_layout(
    title=go.layout.Title(
        text="Plot Title",
        xref="paper",
        x=0
    ),
    xaxis=go.layout.XAxis(
        showticklabels=False,
        title=go.layout.xaxis.Title(
            text="Adverse Outcomes",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#7f7f7f",
            )
        )
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text="Likelihood (Based on Classifier)",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#7f7f7f"
            )
        )
    )
    )
    return figure, data, columns, selected['style']
    
if __name__ == '__main__':
    app.run_server(debug=True)