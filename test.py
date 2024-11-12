# app.py
#import pandas as pd

#def sort_data(df, column_name):
    #"""Trie les données selon la colonne spécifiée."""
    #return df.sort_values(by=column_name)

from source import reverse_str
def test_should_reverse_string():
    assert reverse_str('abc') == 'cba'