import streamlit as st
import pandas as pd
import numpy as np


def load_data(nrows):
    data = pd.read_csv("car_prices_clean.csv", nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

def data_tri(table,colonne,sort_order):
    if colonne:
        
        if sort_order == 'Ascendant':
            data_sorted= pd.DataFrame(table).sort_values(by=colonne, ascending=True)
        else:
            data_sorted = pd.DataFrame(table).sort_values(by=colonne, ascending=False)
    
    return data_sorted

def catogor(data,colonne,cat):
    
    if cat:
        df2=data[data[colonne].isin(cat)]
    else:
        df2=data 
    return df2


data_load_state = st.text('Loading data...')
data = load_data(100)

data_load_state.text('Loading data...done!')



option = st.selectbox(
    "what do you want to choose?",(data.columns)
  
)
st.write("You selected:", option)

sort_order = st.radio("Choisissez l'ordre de tri :", ('Ascendant', 'Descendant'))
data=data_tri(data,option,sort_order)
st.dataframe(data)

cat_model = data['model'].astype('category')


options = st.multiselect(
    "What are your favorite ",(cat_model)
    
)
st.write("You selected:", options)

data=catogor(data,'model',options)
st.dataframe(data)
