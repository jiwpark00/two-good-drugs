import os

import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd

df = pd.read_csv('pain_result_small.csv')
df.drop('Unnamed: 0',axis=1,inplace=True)
df.drop_duplicates(keep = False, inplace=True)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

def generate_table(dataframe, max_rows=20):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


app.layout = html.Div([
    html.H2('Hello World'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL','BOS']],
        value='LA'
    ),
    html.Div(id='display-value')
])

@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])

def display_table(dropdown_value1,dropdown_value2):
    if dropdown_value1 is None:
        return 'Pick the values'

    #listing = 'hi'
    #print(type(df.GNDR_COD))
    #listing = generate_table(df[(df.AGE.isin(dropdown_value1)) & (df.GNDR_COD.isin(dropdown_value2))])
    listing_df = df[(df.AGE.isin(dropdown_value1))]
    if (dropdown_value2 is None) == False:
        listing_df = listing_df[df.GNDR_COD.isin(dropdown_value2)]
        listing = generate_table(listing_df)
        return listing
    
if __name__ == '__main__':
    app.run_server(debug=True)