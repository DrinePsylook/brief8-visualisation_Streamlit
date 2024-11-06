import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

# Charger les données
def load_data(nrows):
    data = pd.read_csv("car_prices_clean.csv", nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data
# Trier les données
def data_tri(table,colonne,sort_order):
    if colonne:
        
        if sort_order == 'Ascendant':
            data_sorted= pd.DataFrame(table).sort_values(by=colonne, ascending=True)
        else:
            data_sorted = pd.DataFrame(table).sort_values(by=colonne, ascending=False)
    
    return data_sorted
# Filtrage par modèle
def catogor(data,colonne,cat):
    
    if cat:
        df2=data[data[colonne].isin(cat)]
    else:
        df2=data 
    return df2
# Filtrage pour les colonnes numériques
def filter_numeric_column(data, column, min_value, max_value):
    return data[data[column].between(min_value, max_value)]
# Filtrage pour les colonnes booléennes
def filter_boolean_column(data, column, selected_value):
    return data[data[column] == selected_value]
# Filtrage pour les colonnes catégorielles
def filter_categorical_column(data, column, selected_values):
    return data[data[column].isin(selected_values)]
# Filtrage automatique  
def automatic_filtering(data):
    filtered_data = data.copy() 
     #fonction du type de chaque colonne
    for column in data.columns:
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
 # Fonction pour télécharger  
def download_excel(data):
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
















