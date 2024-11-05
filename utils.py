import streamlit as st
import pandas as pd
import numpy as np
import io

DATA_CSV = ('car_prices_clean.csv')
buffer = io.BytesIO()

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
    if values and len(values) == 2: 
        new_data = tbl[tbl[col].between(values[0], values[1])]
    else:
        new_data = tbl
    return new_data

def advanced_filter(data, option):
    for col_name, col_type in data.dtypes.items() :
        if col_name == option:
            cat_data = data[col_name].astype('category').unique()
            if col_type == 'object':
                select_data_col = st.sidebar.multiselect(f"Choisissez un filtre avancé pour {col_name} : ", 
                                                        cat_data,
                                                        default = None,
                                                        placeholder = "Quel truc")
                return select_data_col
            elif col_type == 'int64' or col_type == 'float64' :
                min_nb = int(min(data[col_name]))
                max_nb = int(max(data[col_name]))
                values_data_col = st.sidebar.slider(f"Selectionnez une tranche pour {col_name} :", min_nb, max_nb, (min_nb, max_nb))
                return values_data_col
            
def convert_xlsx(data):
    buffer = io.BytesIO()
    writer = pd.ExcelWriter(buffer, engine="xlsxwriter")
    data.to_excel(writer, index=False, sheet_name="sheet1")
    writer.close()
    data_bytes = buffer.getvalue() 
    return data_bytes
 