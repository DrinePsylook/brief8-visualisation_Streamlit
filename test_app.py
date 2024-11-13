import streamlit as st
import pandas as pd
import numpy as np

from streamlit.testing.v1 import AppTest
from app import data, category_model

at = AppTest.from_file("app.py").run()
#df_test = pd.read_csv('car_prices_clean.csv')


def test_title():
    assert at.title[0].value == "Data : vente de voitures"

def test_selectbox():
    opt = data.columns.tolist()
    assert at.selectbox[0].options == opt

def test_radio():
    orderby = ["croissant", "décroissant"]
    assert at.radio[0].options == orderby

def test_multiselect():
    cat = data['model'].astype('category').unique()
    assert set(at.multiselect[0].options) == set(cat)

def test_slider():
    col_name = 'year'
    min_nb = int(min(data[col_name])) 
    max_nb = int(max(data[col_name])) 
    slider_range = at.slider[0].value 
    assert slider_range == (min_nb, max_nb)

def test_slider_price():
    min_price = int(min(data['sellingprice']))
    max_price = int(max(data['sellingprice']))
    assert at.slider[1].value == tuple([min_price, max_price])

def test_button():
    assert at.button[0].label=="Somme"
