import dash
import keras
import pickle
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from keras.models import Sequential
from keras.layers import Dense,LSTM
from dash.dependencies import Input,Output
from app import app


layout = html.Div([
            html.Div([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H1(id='o_p')
                            ]),
                        ],style={'background-color':'#CCD7EA'}),
                    ],width={'size':4}),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H1('this is for graph')
                            ]),
                        ],style={'background-color':'#CCD7EA'}),
                    ]),
                ]),
            ]),
])


@app.callback(Output(component_id="o_p",component_property="children")
            ,Input(component_id="search_box",component_property="value"))

def model_load(value):
    value = value.upper()
    path_model = f'D:\\python_files\\machine_learning_models\\'
    model_ = 'apple_model'
    full_path = path_model + model_    
    saved_model = pickle.dumps(full_path)
    apple_model = pickle.loads(saved_model)
