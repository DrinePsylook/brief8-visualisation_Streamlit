import pytest
import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
#from car_data_analise import load_data,data_tri,catogor,filter_numeric_column,

@pytest.fixture
def load_data(nrows):           # Charger les données
    data = pd.read_csv("car_prices_clean.csv", nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

def data_tri(table,colonne,sort_order):    # Trier les données
    if colonne:
        
        if sort_order == 'Ascendant':
            data_sorted= pd.DataFrame(table).sort_values(by=colonne, ascending=True)
        else:c
    data_sorted = pd.DataFrame(table).sort_values(by=colonne, ascending=False)
    
    return data_sorted

def catogor(data,colonne,cat):    # Filtrage par modèle
    
    if cat:
        df2=data[data[colonne].isin(cat)]
    else:
        df2=data 
    return df2

def filter_numeric_column(data, column, min_value, max_value):  # Filtrage pour les colonnes numériques
    return data[data[column].between(min_value, max_value)]

def filter_boolean_column(data, column, selected_value):        # Filtrage pour les colonnes booléennes
    return data[data[column] == selected_value]

def filter_categorical_column(data, column, selected_values):   # Filtrage pour les colonnes catégorielles
    return data[data[column].isin(selected_values)]

def automatic_filtering(data):      # Filtrage automatique  
    filtered_data = data.copy() 
    
    for column in data.columns:      #fonction du type de chaque colonne
        column_type = data[column].dtype

        if np.issubdtype(column_type, np.number):
            st.write(f"Filtrer la colonne numérique : {column}")
            min_value = data[column].min()
            max_value = data[column].max()
            filter_range = st.slider(f"Plage de {column}:", min_value, max_value, (min_value, max_value))
            filtered_data = filter_numeric_column(filtered_data, column, filter_range[0], filter_range[1])

        elif np.issubdtype(column_type, np.bool_):
            st.write(f"Filtrer la colonne booléenne : {column}")
            selected_value = st.radio(f"Choisissez une valeur pour {column} :", ['True', 'False'])
            filtered_data = filter_boolean_column(filtered_data, column, selected_value == 'True')

        elif np.issubdtype(column_type, object) or np.issubdtype(column_type, np.category):
            st.write(f"Filtrer la colonne catégorielle : {column}")
            unique_values = data[column].unique()
            selected_values = st.multiselect(f"Valeurs de {column} :", unique_values, default=unique_values)
            filtered_data = filter_categorical_column(filtered_data, column, selected_values)

    return filtered_data
 
def download_excel(data):     # Fonction pour télécharger  
    excel_file = BytesIO()   # Créer un fichier Excel en mémoire avec BytesIO

    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:  # Créer un ExcelWriter et écrire les données dans un fichier Excel en mémoire
        data.to_excel(writer, index=False, sheet_name='Sheet1')
 #les données filtrées en Excel  
    st.download_button(     # Télécharger le fichier Excel via Streamlit
        label="Télécharger les données filtrées",
        data= excel_file,
        file_name="filtered_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    excel_file.seek(0) # Revenir au début du fichier Excel en mémoire

def group_data(data, group_by_col, agg_function):
    if group_by_col and agg_function:
                                   # Vérifier que la colonne de données pour l'agrégation est de type numérique
        numeric_columns = data.select_dtypes(include=np.number).columns.tolist()
    return data


def collect_user_input(data):
    group_column = st.selectbox("Sélectionner la colonne de regroupement", data.columns)  # Choisir une colonne de regroupement

    numeric_columns = data.select_dtypes(include=np.number).columns.tolist()# Sélectionner les colonnes d'agrégation numériques
    agg_columns = st.multiselect("Sélectionner les colonnes d'agrégation", numeric_columns)                                  
    agg_functions = {}   # Sélectionner les fonctions d'agrégation pour chaque colonne
    
    for col in agg_columns:
        functions = st.multiselect(f"Choisir les fonctions d'agrégation pour {col}", ['mean', 'sum', 'count', 'min', 'max'])
        agg_functions[col] = functions

    return group_column, agg_columns, agg_functions

def apply_groupby(data, group_column, agg_columns, agg_functions):
    # Regroupement par la colonne choisie
    grouped_data = data.groupby(group_column)
    
    # Appliquer les agrégations spécifiées
    

def display_and_download(aggregated_data):
   
    st.write("donner groupées et agrégées :")
    st.dataframe(aggregated_data)         # Télécharger les résultats agrégés en Excel
    if st.button("Télécharger les données agrégées"):
        download_excel(aggregated_data)

    agg_dict = {}
    for col in agg_columns:
        agg_dict[col] = agg_functions[col]
    
    aggregated_data = grouped_data.agg(agg_dict).reset_index()
    return aggregated_data

data_load_state = st.text('Loading data...')            # Charger les données
data = load_data(100)


data_load_state.text('Loading data...done!')



option = st.selectbox(      # Trier les données
    "what do you want to choose?",(data.columns)
  
)
st.write("You selected:", option)

sort_order = st.radio("Choisissez l'ordre de tri :", ('Ascendant', 'Descendant'))
data=data_tri(data,option,sort_order)


cat_model = data['model'].astype('category')                  # Filtrage par modèle


options = st.multiselect(
    "What are your favorite ",(cat_model)
    
)
st.write("You selected:", options)

data=catogor(data,'model',options)
st.dataframe(data)

# Filtrage des colonnes numériques
numeric_columns = data.select_dtypes(include=np.number).columns

if len(numeric_columns) > 0:
    st.write("You can filter the following numeric columns:", numeric_columns)
    
    
    numeric_column = st.selectbox("Choose a numeric column to filter:", numeric_columns)
    
    min_value = data[numeric_column].min()
    max_value = data[numeric_column].max()

    filter_range = st.slider(f"Select range for {numeric_column}:", min_value, max_value, (min_value, max_value))
    data = filter_numeric_column(data, numeric_column, filter_range[0], filter_range[1])

st.dataframe(data)

data_load_state = st.text('Chargement des données...')
data = load_data(100)  
data_load_state.text('Chargement des données... terminé!')

st.write("Voici les premières lignes des données :")   # Afficher les premières lignes des données
st.dataframe(data.head())
# Filtrage automatique basé sur le type de chaque colonne
filtered_data = automatic_filtering(data)

st.write("Voici les données filtrées :")  # Afficher les données filtrées
st.dataframe(filtered_data)
if st.button("telecharger le excel"):    # Ajouter un bouton pour télécharger le fichier Excel

  download_excel(filtered_data)

                                    # Charger les données
data = load_data(100)

                                    
st.title("Analyse des Données des Voitures")   # Titre de l'application

                                    # Sélection de la colonne pour le groupement
group_column = st.selectbox("Choisir une colonne pour le groupement", data.columns)

                                    # Sélection de la fonction d'agrégation
aggregation_function = st.selectbox("Choisir une fonction d'agrégation", 
                                   ['mean', 'sum', 'count', 'min', 'max'])

                                   # Appliquer le groupement et l'agrégation
if group_column and aggregation_function:
    aggregated_data = group_data(data, group_column, aggregation_function)
    st.write(f"Données groupées par {group_column} avec {aggregation_function} :")
    st.dataframe(aggregated_data)

                                   # Affichage des données brutes
st.write("Voici les données brutes:")
st.dataframe(data.head())

















