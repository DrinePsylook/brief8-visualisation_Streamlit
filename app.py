import streamlit as st
import pandas as pd
import numpy as np
from utils import load_data, order_data, category, slider_price, advanced_filter, col_numeric, convert_xlsx, agg_sum,agg_mean, agg_min, agg_max, agg_all, col_string, concat_data, concat_count, load_model

st.set_page_config(page_title="Visualisation avec Streamlit",
    page_icon="🧊",
    layout="wide")

st.sidebar.title("Filtres")

st.title("Data : vente de voitures")

#état du téléchargement s'il est trop long
data_load_state = st.text('Loading data...')

# appel de la fonction load_data, affichage des données limitées aux 100 premières entrées
data = load_data(1000)


# choix des colonnes à affficher avec un selectbox :
option = st.sidebar.selectbox("Choisissez votre colonne", 
                              (data.columns), 
                              placeholder="Selectionnez votre filtre...",)
# filtre croissant, décroissant avec des boutons radio
ordre = st.sidebar.radio("Quel ordre ?", 
                         key="visibility", 
                         options = ["croissant", "décroissant"])

#data_load_state.text('Loading data...done!')


if option :
    # appel de la fonction filter_data pour l'affichage des données triées par colonne avec le selectbox
    data = order_data(data, option, ordre)
    #appel de la fonction de filtre avancé
    filterPlus = advanced_filter(data, option)
    # print(filterPlus)
    if filterPlus:
        if isinstance(filterPlus, list) :
            data = category(data, option, filterPlus)
        elif isinstance(filterPlus, tuple) and len(filterPlus) == 2 :
            data = slider_price(data, option, filterPlus)
        else:
            data = category(data, 'salemonth', filterPlus)


# transformation de la colonne model d'Object à Category
category_model = data['model'].astype('category').unique()

# choix de plusieurs modèles en fonction des choix de l'utilisateur via le multiselect
select_category = st.sidebar.multiselect(
    "Choisissez les marques des voitures :",
    category_model,
    default = None,
    placeholder = "Marques de voiture"
)

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
    "Choisissez les colonnes numériques à agréger :",
    col_num,
    default = None,
    placeholder = "Les colonnes numériques à agréger"
)


col1, col2 = st.sidebar.columns(2)
with col1:
    button_sum = st.button("Somme")
    button_min = st.button("Minimum")
    button_all = st.button("All agg")
    
with col2:
    button_mean = st.button("Moyenne")
    button_max = st.button("Maximum")


col_str = col_string(data)

select_col_txt = st.sidebar.selectbox(
    "Choisissez les colonnes textuelles à agréger :",
    col_str,
    placeholder = "Les colonnes textuelles  à agréger"
)

col1a, col2a = st.sidebar.columns(2)

with col1a:
    button_concat = st.button("Jointure")
    button_reset = st.button("Reset")

with col2a:
    button_concat_count = st.button("Count")

#appel de la fonction sum
if button_sum:
    data_sum = agg_sum(data, option, select_col_agg)
    st.write(data_sum)

#appel de la fonction mean
if button_mean:
    data_mean = agg_mean(data, option, select_col_agg)
    st.write(data_mean)

#appel de la fonction min
if button_min:
    data_min = agg_min(data, option, select_col_agg)
    st.write(data_min)

#appel de la fonction max
if button_max:
    data_max = agg_max(data, option, select_col_agg)
    st.write(data_max)

#appel de toutes les fonctions agrégation numériques
if button_all:
    data_all_agg = agg_all(data, option, select_col_agg)
    for all_aggregated_data, df in data_all_agg.items():
        st.write(df)

#appel de la fonction agg textuelle
if button_concat:
    data_concat = concat_data(data, option, select_col_txt)
    st.dataframe(data=data_concat, use_container_width= True, on_select="rerun")

#appel de la fonction agg textuelle count
if button_concat_count:
    data_count = concat_count(data, option, select_col_txt)
    st.dataframe(data=data_count, use_container_width= True, on_select="rerun")

#création du bouton reset
if button_reset:
    data = load_data(100)

with st.form("my form"):
    model, data_params, pipeline = load_model()
    car_maker = st.selectbox(
        "Constructeur de voiture",
        data_params["constructeur"],
        index=None,
        placeholder="Choisir un constructeur de voiture"
    )
    car_model = st.selectbox(
        "Modèle de voiture",
        data_params["modèle"],
        index=None,
        placeholder="Choisir un modèle de voiture"
    )
    car_type = st.selectbox(
        "Type de voiture",
        data_params["type"],
        index=None,
        placeholder="Choisir un type de voiture"
    )
    odometer_min, odometer_max = data_params['compteur kilométrique']
    car_odometer = st.slider("Choisir les km", odometer_min, odometer_max, 1)

    condition_min, condition_max = data_params['condition']
    car_condition = st.slider("Choisir l'état de la voiture", condition_min, condition_max, 1)

    year_min, year_max = data_params['année']
    car_year = st.slider("Choisir l'année de construction", year_min+1990, year_max+1990, 1)

    submitted = st.form_submit_button("Envoyer")
    if submitted:
        car_year -= 1990
        st.write([car_year, car_maker, car_model, car_type, car_condition, car_odometer])
        data = [car_year, car_maker, car_model, car_type, car_condition, car_odometer]
        df = pd.DataFrame(columns=['année', 'constructeur', 'modèle', 'type', 'condition', 'compteur kilométrique'], index=[0])
        df.loc[0]=data
        processed_data = pipeline.transform(df)
        preds = model.predict(processed_data)
        st.write(preds)

st.write("Outside the form")

st.dataframe(data=data, use_container_width= True, on_select="rerun")

if isinstance(data, pd.DataFrame): 
    #conversion du data filtré
    xlsx_file = convert_xlsx(data)

    #bouton permettant le téléchargement au format excel
    st.download_button("Download xlsx", 
            data=xlsx_file,
            file_name=f"car_prices-{option}.xlsx",
            mime="application/vnd.ms-excel")
else:
    st.warning("The data is not a DataFrame. Cannot export to Excel.")