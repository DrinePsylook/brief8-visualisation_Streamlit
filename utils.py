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

def category(tbl, col, cat):
    if cat : 
        new_data = tbl[tbl[col].isin(cat)]
    else:
        new_data = tbl
    return new_data

def slider_price(tbl, col, values) :
    if values : 
        new_data = tbl[tbl[col].between(values[0], values[1])]
    else:
        new_data = tbl
    return new_data