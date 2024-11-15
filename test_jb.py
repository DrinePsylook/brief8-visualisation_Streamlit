import streamlit as st
import pandas as pd

from streamlit.testing.v1 import AppTest

### TEST SI TITRE AFFICHÉ ###

def test_title() :
    at = AppTest.from_file("app.py").run()
    assert at.title[0].value == "Data : vente de voitures"

### TEST ORDER DATA ###
from utils import order_data

def test_order_data():
    data = {"A": [3, 1, 2], "B": ["a", "b", "c"]}
    df = pd.DataFrame(data)
    
    result_1 = order_data(df, col="A", order="croissant")
    expected = pd.DataFrame({"A": [1, 2, 3], "B": ["b", "c", "a"]}).reset_index(drop=True)
    pd.testing.assert_frame_equal(result_1.reset_index(drop=True), expected)
    
    result_2 = order_data(df, col="A", order="decroissant")
    expected = pd.DataFrame({"A": [3, 2, 1], 'B': ["a", "c", "b"]}).reset_index(drop=True)
    pd.testing.assert_frame_equal(result_2.reset_index(drop=True), expected)

    ### TEST CATEGORY ###
from utils import category 

def test_category():
    # Données de test
    data = {"Type": ["A", "B", "C", "A", "B", "C"], "Value": [10, 20, 30, 40, 50, 60]}
    df = pd.DataFrame(data)

    # 1 seule cat
    result = category(df, col="Type", cat=["A"])
    expected = pd.DataFrame({"Type": ["A", "A"], "Value": [10, 40]}).reset_index(drop=True)
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)

    # plusieurs cat
    result = category(df, col="Type", cat=["A", "B"])
    expected = pd.DataFrame({"Type": ["A", "B", "A", "B"], "Value": [10, 20, 40, 50]}).reset_index(drop=True)
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)
    # cat = None
    result = category(df, col="Type", cat=None)
    expected = df.reset_index(drop=True)
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)

    ### TEST SLIDER PRICE ###
from utils import slider_price 

def test_slider_price():
    # Données de test
    data = {"Price": [100, 200, 300, 400, 500], "Item": ["A", "B", "C", "D", "E"]}
    df = pd.DataFrame(data)

    # Test avec une plage de valeurs
    result = slider_price(df, col="Price", values=[200, 400])
    expected = pd.DataFrame({"Price": [200, 300, 400], "Item": ["B", "C", "D"]}).reset_index(drop=True)
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)

    # Test avec une seule valeur 
    result = slider_price(df, col="Price", values=[300])
    expected = df.reset_index(drop=True)  

    result = slider_price(df, col="Price", values=[100, 200, 300, 400, 500])
    #print(result)
    min_value =int(min(df["Price"]))
    max_value =int(max(df["Price"]))
    expected = df[df["Price"].between(min_value, max_value)]
    #print(expected)
    pd.testing.assert_frame_equal(result, expected)
   