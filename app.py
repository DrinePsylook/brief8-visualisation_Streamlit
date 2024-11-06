import streamlit as st
import pandas as pd
import numpy as np
from utils import load_data, filter_data, category, slider_price, advanced_filter, col_numeric, convert_xlsx, agg_sum,agg_mean, agg_min, agg_max

st.set_page_config(page_title="Visualisation avec Streamlit",
    page_icon="🧊",
    layout="wide")

st.sidebar.title("Filtres")

st.title("Tableau : prix des voitures")

#état du téléchargement s'il est trop long
data_load_state = st.text('Loading data...')

# appel de la fonction load_data, affichage des données limitées aux 100 premières entrées
data = load_data(100)

# choix des colonnes à affficher avec un selectbox :
option = st.sidebar.selectbox("Choisissez votre colonne", (data.columns), placeholder="Selectionnez votre filtre...",)
# filtre croissant, décroissant avec des boutons radio
ordre = st.sidebar.radio("Quel ordre ?", key="visibility", options = ["croissant", "décroissant"])

data_load_state.text('Loading data...done!')


if option :
    # appel de la fonction filter_data pour l'affichage des données triées par colonne avec le selectbox
    data = filter_data(data, option, ordre)
    #appel de la fonction de filtre avancé
    filterPlus = advanced_filter(data, option)
    #print(filterPlus)
    if filterPlus:
        if isinstance(filterPlus, list) :
            data = category(data, option, filterPlus)
        elif isinstance(filterPlus, tuple) and len(filterPlus) == 2 :
            data = slider_price(data, option, filterPlus)


# transformation de la colonne model d'Object à Category
category_model = data['model'].astype('category').unique()

# choix de plusieurs modèles en fonction des choix de l'utilisateur via le multiselect
select_category = st.sidebar.multiselect(
    "Choisissez les marques des voitures :",
    category_model,
    default = None,
    placeholder = "Marques de voiture"
)
#st.write(select_category)

# appel de la fonction category pour l'affichage des données liées au model de voiture
data = category(data, 'model', select_category)

# prix de vente minimum et maximum dans la liste
if not data.empty :
    min_price = int(min(data['sellingprice']))
    max_price = int(max(data['sellingprice']))

    if min_price == max_price:
        st.sidebar.write(f"Le prix de vente est fixe : {min_price}")
        values = (min_price, max_price)  # Utilisation de la valeur unique pour le filtre
    else:
        # affichage du slider
        values = st.sidebar.slider("Selectionnez une tranche de prix :", min_price, max_price, (min_price, max_price))

    data = slider_price(data, 'sellingprice', values)

st.sidebar.divider()


col_num = col_numeric(data)

select_col_agg = st.sidebar.multiselect(
    "Choisissez les colonnes à aggréger :",
    col_num,
    default = None,
    placeholder = "Les colonnes à aggréger"
)

if st.sidebar.button("Somme"):
    data_sum = agg_sum(data, option, select_col_agg)
    data_sum

if st.sidebar.button("Moyenne"):
    data_mean = agg_mean(data, option, select_col_agg)
    data_mean

if st.sidebar.button("Minimum"):
    data_min = agg_min(data, option, select_col_agg)
    data_min

if st.sidebar.button("Maximum"):
    data_max = agg_max(data, option, select_col_agg)
    data_max

if st.sidebar.button("Reset"):
    data = load_data(100)


st.dataframe(data=data, use_container_width= True, on_select="rerun")

#conversion du data filtré
xlsx_file = convert_xlsx(data)

#bouton permettant le téléchargement au format excel
st.download_button("Download xlsx", 
          data=xlsx_file,
          file_name=f"car_prices-{option}.xlsx",
          mime="application/vnd.ms-excel")
