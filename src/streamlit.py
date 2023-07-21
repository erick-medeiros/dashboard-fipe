import streamlit as st
from BrasilAPI import BrasilAPI
from data import get_data

api = BrasilAPI(debug=True)


def main():
    st.header("Dashboard FIPE")

    codeFipe = "0240265"

    data = get_data(api, codeFipe)

    df = data.pivot_table(values="valor", index="mes", columns="ano")

    st.line_chart(df)


if __name__ == "__main__":
    main()
