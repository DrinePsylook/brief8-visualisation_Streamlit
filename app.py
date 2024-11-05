import streamlit as st
import pandas as pd
import numpy as np
from utils import load_data, filter_data, category, slider_price

#état du téléchargement s'il est trop long
data_load_state = st.text('Loading data...')

# appel de la fonction load_data, affichage des données limitées aux 100 premières entrées
data = load_data(100)

# choix des colonnes à affficher avec un selectbox :
option = st.selectbox("Choisissez votre colonne", (data.columns), placeholder="Selectionnez votre filtre...",)
# filtre croissant, décroissant avec des boutons radio
ordre = st.radio("Quel ordre ?", key="visibility", options = ["croissant", "décroissant"])

#data_load_state.text('Loading data...done!')

# appel de la fonction filter_data pour l'affichage des données triées par colonne avec le selectbox
data = filter_data(data, option, ordre)

# transformation de la colonne model d'Object à Category
category_model = data['model'].astype('category')

# choix de plusieurs modèles en fonction des choix de l'utilisateur via le multiselect
select_category = st.multiselect(
    "Choisissez les marques des voitures :",
    category_model,
    default = None,
    placeholder = "Marques de voiture"
)
#st.write(select_category)

# appel de la fonction category pour l'affichage des données liées au model de voiture
data = category(data, 'model', select_category)

# prix de vente minimum et maximum dans la liste
min_price = min(data['sellingprice'])
max_price = max(data['sellingprice'])

# affichage du slider
values = st.slider("Selectionnez une tranche de prix", int(min_price), int(max_price), (20000, 30000))

data = slider_price(data, 'sellingprice', values)



st.dataframe(data=data, on_select="rerun", selection_mode="multi-row")
