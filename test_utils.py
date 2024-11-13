import streamlit as st
import pandas as pd

from utils import order_data, category, slider_price

def test_order_data():
    # Données de test
    tbl = [[1, "test1"], [2, "test2"], [3, "test3"]]
    df = pd.DataFrame(tbl, columns=["id", "name"])
    # Test tri croissant
    result = order_data(df, "id", "croissant").reset_index(drop=True)
    expected_result = pd.DataFrame([[1, "test1"], [2, "test2"], [3, "test3"]], columns=["id", "name"]).reset_index(drop=True)
    pd.testing.assert_frame_equal(result, expected_result)
    # Test tri décroissant
    result = order_data(df, "id", "décroissant").reset_index(drop=True)
    expected_result = pd.DataFrame([[3, "test3"], [2, "test2"], [1, "test1"]], columns=["id", "name"]).reset_index(drop=True)
    pd.testing.assert_frame_equal(result, expected_result)

def test_category():
    # données de test
    tbl = pd.DataFrame({
        "id": [0, 1, 2],
        "classe": ["chat", "chien", "serpent"],
        "nom": ["Théo", "Noon", "Oz"],
        "race": ["Main Coon", "labrador", "python"]
    })
    col = ["classe", "nom", "race"]
    # test retour category
    result = category(tbl,col, ["chat", "chien", "serpent"]).reset_index(drop=True)
    expected_result = tbl[tbl[col].isin(["chat", "chien", "serpent"])].reset_index(drop=True)
    pd.testing.assert_frame_equal(result, expected_result)

    #test cat = None
    result = category(tbl,col, None).reset_index(drop=True)
    expected_result = tbl.reset_index(drop=True)
    pd.testing.assert_frame_equal(result, expected_result)

def test_slider_price():
    tbl = [[1, "car1", 2000], [2, "car2", 1500], [3, "car3", 5800]]
    df = pd.DataFrame(tbl, columns=["id", "name", "price"])
    result = slider_price(df, "price", [2000, 1500, 5800]).reset_index(drop=True)

