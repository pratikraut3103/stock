import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import yfinance as yf
from dash.dependencies import Output,Input
from app import app

layout = html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Card([
                            dbc.CardBody([
                                dbc.Row([
                                    html.H3("Recommendations")
                                ]),
                                dbc.Row([
                                    html.Div([],id = "recommendations")
                                ])

                            ])
                        ],style={'background-color':'#CCD7EA',"width":"100%"})
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Card([
                            dbc.CardBody([
                                dbc.Row([
                                    html.H3("Instutional Holder")
                                ]),
                                dbc.Row([
                                    html.Div([],id = "Holders")
                                ])

                            ])
                        ],style={'background-color':'#CCD7EA'})
                    ]),

                    html.Br(),
                    dbc.Row([
                        dbc.Card([
                            dbc.CardBody([
                                dbc.Row([
                                    html.H3(" Download Historic Data"),
                                    html.Br(),
                                    dcc.DatePickerRange(
                                        start_date_placeholder_text="Start Period",
                                        end_date_placeholder_text="End Period",
                                        calendar_orientation='horizontal',
                                    )
                                ]),
                                dbc.Row([
                                    dbc.Button
                                ]),
                            ])
                        ],style={'background-color':'#CCD7EA'})
                    ])
                ],width={"size":3}),

                html.Br(),

                dbc.Col([
                    dbc.Row([
                        dbc.Card([
                            dbc.CardBody([
                                dbc.Row([
                                    html.Div([
                                        dcc.RadioItems(
                                            id='book_select',
                                            options=[
                                                {'label': 'Call', 'value': 'ce'},
                                                {'label': 'Puts', 'value': 'pe'},
                                            ],
                                            value='ce',
                                            labelStyle={'display': 'inline-block',"margin-right": "10px"}
                                        ),
                                        dbc.Toast(
                                            "Call selected",
                                            id="call_toast",
                                            header="Call Values",
                                            is_open=False,
                                            dismissable=True,
                                            icon="danger",
                                            # top: 66 positions the toast below the navbar
                                            style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                                        ),
                                        dbc.Toast(
                                            "Put selected",
                                            id="put_toast",
                                            header="Put Values",
                                            is_open=False,
                                            dismissable=True,
                                            icon="danger",
                                            # top: 66 positions the toast below the navbar
                                            style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                                        )
                                    ]),
                                ]),
                                dbc.Row([
                                    html.Div([],id = "book"),
                                ])

                            ])
                        ],style={'background-color':'#CCD7EA'})
                    ])
                ],width={"size":9}),
            ],no_gutters=False)
])

class Data:
    def __init__(self,ticker):
        self.Ticker = yf.Ticker(ticker)
    def gat_recommendation(self):
        recommend = self.Ticker.recommendations
        return recommend
    def gat_institionalHolder(self):
        inst = self.Ticker.institutional_holders
        return inst
    def gat_option(self):
        opt = self.Ticker.option_chain('2021-03-26')
        return opt



@app.callback(Output(component_id='recommendations',component_property='children'),
            [Input(component_id='search_box',component_property='value')])
def recom(value):
    d = Data(value)
    df = d.gat_recommendation()
    df = df.filter(["Firm","To Grade"])
    df = df.head(5)
    return dbc.Table.from_dataframe(df,style={'font-family':'nudista-web",Helvetica,Arial,sans-serif','color':'black'})

@app.callback(Output(component_id='Holders',component_property='children'),
            [Input(component_id='search_box',component_property='value')])
def recom(value):
    d = Data(value)
    df = d.gat_institionalHolder()
    df = df.filter(["Holder","Shares"])
    df = df.head(5)
    return dbc.Table.from_dataframe(df,style={'font-family':'nudista-web",Helvetica,Arial,sans-serif','color':'black'})

@app.callback(Output(component_id='book',component_property='children'),
            [Input(component_id='search_box',component_property='value'),
             Input(component_id="book_select",component_property='value')])
def recom(value,book_value):
    d = Data(value)
    df = d.gat_option()
    df = pd.DataFrame(df)
    if book_value == "ce" :
        df = df[0].tolist()[0]
        df = df.drop(columns=["openInterest",	"impliedVolatility","inTheMoney"	,"contractSize"	,"currency"])
        df.fillna(value=0,inplace=True)
        df = df[df['volume'] != 0]
    elif book_value == "pe" :
        df = df[0].tolist()[1]
        df = df.drop(columns=["openInterest",	"impliedVolatility","inTheMoney"	,"contractSize"	,"currency"])
        df.fillna(value=0,inplace=True)
        df = df[df['volume'] != 0]
    return dbc.Table.from_dataframe(df,style={'font-family':'nudista-web",Helvetica,Arial,sans-serif','color':'black',"font-size":"15px"})

@app.callback(
    Output("call_toast", "is_open"),
    [Input("book_select", "value")],
)
def open_toast(n):
    if n=="ce":
        return True
    return False

@app.callback(
    Output("put_toast", "is_open"),
    [Input("book_select", "value")],
)
def open_toast(n):
    if n=="pe":
        return True
    return False
