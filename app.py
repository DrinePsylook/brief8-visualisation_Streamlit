import streamlit as st
import pandas as pd
import numpy as np

DATA_CSV = ('car_prices_clean.csv')


def load_data(nrows) :
    data = pd.read_csv(DATA_CSV, nrows=nrows)
    lowercase= lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

def filter_data(data, col, order):
    asc = None
    if order == "croissant":
        asc = True
    else:
        asc = False
    if col:
        tbl_filter = pd.DataFrame(data).sort_values(by=col, ascending=asc)
    return tbl_filter


data_load_state = st.text('Loading data...')

data = load_data(100)
option = st.selectbox("Choisissez votre colonne", (data.columns), placeholder="Selectionnez votre filtre...",)
ordre = st.radio("Quel ordre ?", key="visibility", options = ["croissant", "décroissant"])

data_load_state.text('Loading data...done!')
data = filter_data(data, option, ordre)

category_model = data['model'].astype('category')

st.dataframe(data=data, on_select="rerun", selection_mode="multi-row")
