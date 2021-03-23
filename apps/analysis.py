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
                        ],style={'background-color':'#CCD7EA'})
                    ]),
                    dbc.Row([

                    ])
                ])
            ])
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

@app.callback(Output(component_id='recommendations',component_property='children'),
            [Input(component_id='search_box',component_property='value')])
def recom(value):
    d = Data(value)
    df = d.gat_recommendation()
    df = df.filter(["Firm","To Grade"])
    df = df.head(5)
    return dbc.Table.from_dataframe(df,style={'font-family':'nudista-web",Helvetica,Arial,sans-serif','color':'black'})
