import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd

app = dash.Dash(__name__)

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

server = app.server

df = pd.read_csv('pain_result.csv')
df.drop('Unnamed: 0',axis=1,inplace=True)
df.drop_duplicates(keep = False, inplace=True)

def generate_table(dataframe, max_rows=20):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

app.layout = html.Div(children=[
    html.H4(children='FAERS Drug Data 2012-2019'),
    dcc.Dropdown(id='dropdown1', options=[
        {'label': i, 'value': i} for i in df.AGE.unique()
    ], multi=True, placeholder='Filter by age...'),
    dcc.Dropdown(id='dropdown2', options=[
        {'label': i, 'value': i} for i in df.GNDR_COD.unique()
    ], multi=True, placeholder='Filter by gender...'),
    html.Div(id='table-container1')
])

@app.callback(
    dash.dependencies.Output('table-container1', 'children'),
    [dash.dependencies.Input('dropdown1', 'value'),
    dash.dependencies.Input('dropdown2', 'value')])
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