import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
import base64
import numpy as np
from sklearn.externals import joblib

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server=app.server

df = pd.read_csv('df_prediction_list_nausea.csv')

data=df.to_dict("records")

column_numbers = [4,5,8,9]

image_filename = 'red-pill-blue-pill.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app.layout = html.Div([

    html.H1(children='INTER:ACTION?'),

    html.Img(src='data:image/png;base64,{}'.format(encoded_image),
        style={'height': '150px', 'width': '300px'}),

    html.H4("Predicting likely adverse outcomes for drug2drug interactions" ),

    html.H5("Please pick the relevant patient information: drugs, age, weight"),

    dcc.Dropdown(
    id="drop-down",

    options=[
        {"label": i, "value": i} for i in sorted(df['First Drug'].unique())],
    value='ANDROGEL',style={'font-size':'20px','height': '30px', 'width': '300px'}
),

    dcc.Dropdown(
    id="drop-down2",
    value='VICODIN',style={'font-size':'20px','height': '30px', 'width': '300px'}
),

    dcc.Dropdown(
    id="drop-down3",

    options=[
        {"label": i, "value": i} for i in sorted(df['AGE'].unique())],
    value=70,style={'font-size':'20px','height': '30px', 'width': '300px'}
),

    dcc.Dropdown(
    id="drop-down4",

    options=[
        {"label": i, "value": i} for i in sorted(df['WT'].unique())],
    value=57,style={'font-size':'20px','height': '30px', 'width': '300px'}
),

    dcc.Dropdown(
    id="drop-down5",

    options=[
        {"label": i, "value": i} for i in sorted(df['Gender'].unique())],
    value='F',style={'font-size':'20px','height': '30px', 'width': '300px'}
),

    dash_table.DataTable(

    id='table-filtering',
    columns=[{"name": i, "id": i} for i in df.columns[column_numbers]],

    style_as_list_view=False,

    style_cell={'fontSize':20},

    style_data_conditional=[

    {
            'if': {
                'column_id': 'Nausea_Risk',
                'filter_query': '{Nausea_Risk} eq "Medium_Risk"'
            },
            'backgroundColor': '#FF9F0A',
            'color': 'white',
        },
        {
            'if': {
                'column_id': 'Nausea_Risk',
                'filter_query': '{Nausea_Risk} eq "High_Risk"'
            },
            'backgroundColor': '#FF375F',
            'color': 'white',
            },
             {
            'if': {
                'column_id': 'Nausea_Risk',
                'filter_query': '{Nausea_Risk} eq "No_Risk"'
            },
            'backgroundColor': '#3D9970',
            'color': 'white',
            }]

)


    ])

@app.callback(Output('drop-down2', 'options'),
    [Input('drop-down', "value")])

def set_cities_options(selected_country):
    return [{"label": i, "value": i} for i in sorted(df[df['First Drug'] == selected_country]['Second Drug'].unique())]

@app.callback(
    dash.dependencies.Output('drop-down2', 'value'),
    [dash.dependencies.Input('drop-down2', 'options')])
def set_cities_value(available_options):
    return available_options[0]['value']

@app.callback(Output('drop-down3', 'options'),
    [Input('drop-down', "value"),
    Input('drop-down2',"value")])

def set_cities_options(selected_country1,selected_country2):
    return [{"label": i, "value": i} for i in sorted(df[(df['First Drug'] == selected_country1) & 
        (df['Second Drug'] == selected_country2)]['AGE'].unique())]

@app.callback(
    dash.dependencies.Output('drop-down3', 'value'),
    [dash.dependencies.Input('drop-down3', 'options')])
def set_cities_value(available_options):
    return available_options[0]['value']

@app.callback(Output('drop-down4', 'options'),
    [Input('drop-down', "value"),
    Input('drop-down2',"value"),
    Input('drop-down3',"value")])

def set_cities_options(selected_country1, selected_country2, selected_country3):
    return [{"label": i, "value": i} for i in sorted(df[(df['First Drug'] == selected_country1) & 
        (df['Second Drug'] == selected_country2) & (df['AGE'] == selected_country3)]['WT'].unique())]

@app.callback(
    dash.dependencies.Output('drop-down4', 'value'),
    [dash.dependencies.Input('drop-down4', 'options')])
def set_cities_value(available_options):
    return available_options[0]['value']

@app.callback(Output('drop-down5', 'options'),
    [Input('drop-down', "value"),
    Input('drop-down2',"value"),
    Input('drop-down3',"value"),
    Input('drop-down4', "value")])

def set_cities_options(selected_country1,selected_country2,selected_country3,selected_country4):
    return [{"label": i, "value": i} for i in sorted(df[(df['First Drug'] == selected_country1) & 
        (df['Second Drug'] == selected_country2) & (df['AGE'] == selected_country3) &
        (df['WT'] == selected_country4)]['Gender'].unique())]

@app.callback(
    dash.dependencies.Output('drop-down5', 'value'),
    [dash.dependencies.Input('drop-down5', 'options')])
def set_cities_value(available_options):
    return available_options[0]['value']

@app.callback(
    Output('table-filtering', "data"),
    [Input('drop-down', "value"),
    Input('drop-down2', "value"),
    Input('drop-down3', "value"),
    Input('drop-down4', "value"),
    Input('drop-down5', "value")])

def update_table(value1, value2, value3, value4, value5):
    filename = 'DecisionTree_Pain_model.pkl' # or .sav
    with open(filename, 'wb') as outfile:
        joblib.dump(classifier_DM, outfile) # key for saving

    # random_data = [[50, 70,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,
    #      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  1,  0,  0,
    #      0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    #      0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0]]

    # print(loaded_model.predict_proba(random_data)[0])

    df_f=df
    dff=df_f.loc[(df_f["First Drug"]==value1) & (df_f["Second Drug"]==value2) & 
    (df_f["AGE"]==value3) & (df_f["WT"]==value4) & 
    (df_f["Gender"]==value5)]
    return dff.to_dict("records")

 
if __name__ == '__main__':
    app.run_server(debug=True)