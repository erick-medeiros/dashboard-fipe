import utils
from BrasilAPI import BrasilAPI
import pandas as pd
import datetime

year_current = datetime.date.today().year

def get_data(api: BrasilAPI, codeFipe: str) -> pd.DataFrame:
    data = {"ano": [], "mes": [], "valor": []}

    codeTables = []

    tabelas = api.get_fipe_tabelas()

    if tabelas is not None:
        for i in tabelas:
            codeTables.append(i["codigo"])
        # codeTables.append(tabelas[0]["codigo"])
        # codeTables.append(tabelas[1]["codigo"])
        # codeTables.append(tabelas[2]["codigo"])

    response_data = api.get_multiple_fipe_preco(codeFipe, codeTables)

    if response_data is not None:
        for value_per_month in response_data:
            if value_per_month is None:
                    continue
            for value_by_model_year in value_per_month:
                if value_by_model_year is None:
                    continue

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
