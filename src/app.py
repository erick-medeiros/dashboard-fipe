from dash import Dash, html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
import utils
from BrasilAPI import BrasilAPI
import pandas as pd
import datetime

codeFipeDefault = "0240265"

isLoading = False

year_current = datetime.date.today().year

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

api = BrasilAPI(debug=True)


def get_data(codeFipe) -> pd.DataFrame:
    data = {"ano": [], "mes": [], "valor": []}

    codeTables = []

    tabelas = api.get_fipe_tabelas()

    if tabelas is not None:
        for i in tabelas:
            codeTables.append(i["codigo"])

    response_data = api.get_multiple_fipe_preco(codeFipe, codeTables)

    if response_data is not None:
        for value_per_month in response_data:
            for value_by_model_year in value_per_month:
                model_year = int(value_by_model_year["anoModelo"])

                if model_year > year_current:
                    continue

                reference_month = utils.br_date(value_by_model_year["mesReferencia"])
                value = utils.brl_to_float(value_by_model_year["valor"])

                data["ano"].append(model_year)
                data["mes"].append(reference_month)
                data["valor"].append(value)

    df = pd.DataFrame(data)
    df.sort_values(by="mes", inplace=True)
    df.sort_values(by="ano")
    return df


def get_fig(codeFipe):
    data = get_data(codeFipe)
    return px.line(data, x="mes", y="valor", color="ano")


@callback(
    Output("output-graph", "children"),
    Input("submit-val", "n_clicks"),
    State("input-on-submit", "value"),
)
def update_output(children, value):
    if value is None:
        return html.Div()
    else:
        return html.Div([dcc.Graph(id="line-graph", figure=get_fig(value))])


app.layout = dbc.Container(
    [
        dbc.Row(
            [
                html.H1("Hello World"),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(id="output-graph", children=[]),
                ),
                html.Div(
                    [
                        html.Div(dcc.Input(id="input-on-submit", type="text")),
                        html.Button("Submit", id="submit-val", n_clicks=0),
                    ]
                ),
            ],
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
