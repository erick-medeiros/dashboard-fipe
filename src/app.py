from dash import Dash
import dash_bootstrap_components as dbc
from BrasilAPI import BrasilAPI
import layout

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

api = BrasilAPI(debug=True)

app.layout = layout.layout()

layout.callbacks(api)

if __name__ == "__main__":
    app.run_server(debug=False)
