import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(page_title="Dashboard Beans & Pods", layout="wide")

# Chargement des données
def load_data():
    fichier = 'beans_and_pods_v2.csv'  # <--- Nouveau fichier
    data = pd.read_csv(fichier)
    return data

# Chargement des données
data = load_data()
produits = ['Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino']

# Sidebar
st.sidebar.title("Beans & Pods")
menu = st.sidebar.selectbox("Navigation", [
    "Accueil", "Exploration", "Analyse & Corrélations",
    "Visualisations", "Analyse des Performances", "Rapport & Recommandations"
])

# ACCUEIL
if menu == "Accueil":
    st.markdown("""
    <div style='text-align: center;'>
    <h1>Tableau de Bord - Beans & Pods</h1>
    <p style='color:green;'>Analyse des ventes de café pour booster le marketing.</p>
    </div>
    """, unsafe_allow_html=True)
    st.image("https://cdn.pixabay.com/photo/2015/07/02/10/28/coffee-828527_1280.jpg", use_container_width=True)
    st.subheader("Aperçu des Données")
    st.dataframe(data.head())

# EXPLORATION
elif menu == "Exploration":
    st.header("Exploration des Données")
    st.dataframe(data.head(10))
    st.subheader("Statistiques descriptives")
    st.write(data.describe())

    st.subheader("Répartition des canaux de vente")
    fig1, ax1 = plt.subplots()
    data['Channel'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax1)
    ax1.set_ylabel('')
    st.pyplot(fig1)

    st.subheader("Répartition par région")
    fig2, ax2 = plt.subplots()
    sns.countplot(data=data, x='Region', ax=ax2)
    st.pyplot(fig2)

# CORRÉLATIONS
elif menu == "Analyse & Corrélations":
    st.header("Analyse & Corrélations")
    st.subheader("Matrice de Corrélation")
    corr = data[produits].corr()
    fig_corr, ax_corr = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax_corr)
    st.pyplot(fig_corr)

    st.subheader("Ventes moyennes par région")
    st.dataframe(data.groupby('Region')[produits].mean())

    st.subheader("Ventes moyennes par canal")
    st.dataframe(data.groupby('Channel')[produits].mean())

# VISUALISATIONS
elif menu == "Visualisations":
    st.header("Visualisations Interactives")

    st.subheader("Histogrammes des ventes")
    data[produits].hist(figsize=(14, 10), bins=20)
    st.pyplot(plt.gcf())

    st.subheader("Boxplot des ventes par région")
    produit = st.selectbox("Choisissez un produit :", produits)
    fig_box, ax_box = plt.subplots()
    sns.boxplot(data=data, x='Region', y=produit, ax=ax_box)
    st.pyplot(fig_box)

# ANALYSE DES PERFORMANCES
elif menu == "Analyse des Performances":
    st.header("Analyse des Performances de Vente")

    col1, col2 = st.columns(2)
    with col1:
        selected_region = st.selectbox("Filtrer par Région", ['Toutes'] + sorted(data['Region'].unique()))
    with col2:
        selected_channel = st.selectbox("Filtrer par Canal", ['Tous'] + sorted(data['Channel'].unique()))

    filtered_data = data.copy()
    if selected_region != 'Toutes':
        filtered_data = filtered_data[filtered_data['Region'] == selected_region]
    if selected_channel != 'Tous':
        filtered_data = filtered_data[filtered_data['Channel'] == selected_channel]

    st.subheader("Ventes Totales par Produit")
    ventes = filtered_data[produits].sum()
    fig_prod, ax_prod = plt.subplots()
    ventes.sort_values().plot.barh(ax=ax_prod, color=sns.color_palette("Set2", len(ventes)))
    ax_prod.set_xlabel("Total des Ventes")
    ax_prod.set_ylabel("Produits")
    st.pyplot(fig_prod)

# RAPPORT
elif menu == "Rapport & Recommandations":
    st.header("Rapport & Recommandations")
    st.markdown("""
    ### Tendances Observées
    - **Arabica**, **Espresso** et **Latte** sont très populaires.
    - Le canal **Online** génère plus de ventes globalement.
    - Des différences nettes existent entre les régions.

    ### Recommandations
    ✅ Renforcer la vente **en ligne** dans les régions performantes.  
    ✅ Mettre en avant **Latte et Espresso** dans les campagnes marketing.  
    ✅ Analyser la saisonnalité pour chaque type de café.

    ### Données à Collecter à l’Avenir
    - Données temporelles (mois, saison)
    - Données clients (âge, fidélité, satisfaction)
    - Coût de revient par produit
    """, unsafe_allow_html=True)

    st.success("Projet réalisé par MOR FAYE")
