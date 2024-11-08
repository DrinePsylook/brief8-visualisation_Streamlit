import streamlit as st
import pandas as pd
import numpy as np
import io
from datetime import datetime, date

DATA_CSV = ('car_prices_clean.csv')
buffer = io.BytesIO()

def load_data(nrows) :
    data = pd.read_csv(DATA_CSV, nrows=nrows)
    lowercase= lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

def order_data(data, col, order):
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

def convert_date(data):
    for col_name, col_type in data.dtypes.items() :
        if col_name == 'saledate':
            data['salemonth'] = pd.DataFrame(data['saledate'])
            # récupération du mois de vente
            data['salemonth'] = pd.to_datetime(data['salemonth'], errors='coerce').dt.month
            data['salemonth'] = data['salemonth'].apply(lambda x: datetime(1900, x, 1).strftime('%B'))
            month = data['salemonth'].unique()
            values_col_month = st.sidebar.multiselect(f"Choisissez un filtre avancé pour {col_name} : ", month,
                                        default = None,
                                        placeholder = f"Quel {col_name} ?")
            return values_col_month

def advanced_filter(data, option):
    for col_name, col_type in data.dtypes.items() :
        if col_name == option:
            cat_data = data[col_name].astype('category').unique()
            if col_type == 'object':
                select_data_col = st.sidebar.multiselect(f"Choisissez un filtre avancé pour {col_name} : ", 
                                                        cat_data,
                                                        default = None,
                                                        placeholder = f"Quel {col_name} ?")
                return select_data_col
            elif col_type == 'int64' or col_type == 'float64' :
                min_nb = int(min(data[col_name]))
                max_nb = int(max(data[col_name]))
                # print(f"nb min-max : {type(min_nb)} et {type(max_nb)}")

                values_data_col = st.sidebar.slider(f"Selectionnez une tranche pour {col_name} :", min_nb, max_nb, (min_nb, max_nb))
                return values_data_col
            
def col_numeric(data):
    col_num=[]
    for col_name, col_type in data.dtypes.items() :
        if col_type == 'int64' or col_type == 'float64' :
            col_num.append(col_name)
    return col_num

def col_string(data):
    col_str = []
    for col_name, col_type in data.dtypes.items() :
        if col_type == 'object':
            col_str.append(col_name)
    return col_str
        
 
def agg_sum(data, col1, col2):
    sum_data = data.groupby(col1)[col2].sum()
    return sum_data

def agg_mean(data, col1, col2):
    mean_data = data.groupby(col1)[col2].mean()
    return mean_data

def agg_min(data, col1, col2):
    min_data = data.groupby(col1)[col2].min()
    return min_data

def agg_max(data, col1, col2):
    max_data = data.groupby(col1)[col2].max()
    return max_data

def agg_all(data, col1, col2_list):
    all_data = {}
    for col2 in col2_list:
        grouped_data = data.groupby(col1).agg({ col2:['sum', 'mean', 'min','max'] })
        grouped_data.columns = ['_'.join(col) for col in grouped_data.columns.values]
        all_data[col2] = grouped_data.reset_index()
    return all_data

def concat_data(data, col1, col2):
    data_concatened = data.groupby([col1], as_index = False).agg({col2: [", ".join, 'unique']})
    # print(data_concatened[col2].unique)
    new_col2 = data_concatened[col2].unique.apply(lambda x: str(x).replace("['", "").replace("']", ""))
    # print("new_col2 = ", new_col2)
    new_data = [data_concatened[col1], new_col2]
    return new_data

def concat_count(data, col1, col2):
    total = data.groupby([col1], as_index = False).agg({col2: [', '.join, 'unique', 'count']})
    # total.columns = [col1, f"{col2}_joined", f"{col2}_unique", f"{col2}_count"]
    # new_col2 = total[col2].unique.apply(lambda x: str(x).replace("['", "").replace("']", ""))
    # print("new_col = ", total[col2].count)
    # new_data = total[[col1, f"{col2}_joined", new_col2, f"{col2}_count"]]
    return total

def convert_xlsx(data):
    buffer = io.BytesIO()
    writer = pd.ExcelWriter(buffer, engine="xlsxwriter")
    data.to_excel(writer, index=False, sheet_name="sheet1")
    writer.close()
    data_bytes = buffer.getvalue() 
    return data_bytes