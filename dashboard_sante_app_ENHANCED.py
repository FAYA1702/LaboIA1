import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard Santé", layout="wide")

def load_data():
    fichier = 'health_sales_data.csv'
    data = pd.read_csv(fichier)
    return data

data = load_data()

# Menu latéral
st.sidebar.title("Dashboard Santé")
menu = st.sidebar.selectbox("Navigation", ["Accueil", "Exploration", "Analyse & Corrélations", "Visualisations", "Analyse des Performances", "Rapport & Recommandations"])

# Accueil
if menu == "Accueil":
    st.markdown("""
    <div style='text-align: center;'>
    <h1>Tableau de Bord - Produits Santé</h1>
    <p style='color:blue;'>Analyse des ventes et données clients pour optimiser les stratégies commerciales.</p>
    </div>
    """, unsafe_allow_html=True)
    st.image("https://cdn.pixabay.com/photo/2020/10/29/16/27/health-5695515_1280.jpg", use_container_width=True)
    st.subheader("Aperçu des Données")
    st.dataframe(data.head())

# Exploration
elif menu == "Exploration":
    st.header("Exploration des Données")
    st.subheader("Aperçu des premières lignes")
    st.dataframe(data.head(10))
    st.subheader("Aperçu des dernières lignes")
    st.dataframe(data.tail(10))

    st.subheader("Statistiques descriptives")
    st.write(data.describe())

    st.subheader("Répartition des canaux de vente")
    fig1, ax1 = plt.subplots()
    data['Channel'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, ax=ax1)
    ax1.set_ylabel('')
    st.pyplot(fig1)

    st.subheader("Répartition par région")
    fig2, ax2 = plt.subplots()
    sns.countplot(data=data, x='Region', ax=ax2)
    st.pyplot(fig2)

# Corrélations
elif menu == "Analyse & Corrélations":
    st.header("Analyse & Corrélations")
    st.subheader("Matrice de Corrélation")
    corr = data.select_dtypes(include=['float64', 'int64']).corr()
    fig_corr, ax_corr = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax_corr)
    st.pyplot(fig_corr)

    st.subheader("Ventes moyennes par région")
    region_moy = data.groupby('Region')[['Product_A', 'Product_B', 'Product_C', 'Product_D', 'Customer_Age', 'Purchase_Amount']].mean()
    st.dataframe(region_moy)

    st.subheader("Ventes moyennes par canal")
    canal_moy = data.groupby('Channel')[['Product_A', 'Product_B', 'Product_C', 'Product_D', 'Customer_Age', 'Purchase_Amount']].mean()
    st.dataframe(canal_moy)

# Visualisations
elif menu == "Visualisations":
    st.header("Visualisations Interactives")

    st.subheader("Histogrammes des ventes par produit")
    data[['Product_A', 'Product_B', 'Product_C', 'Product_D']].hist(figsize=(12, 8), bins=20)
    st.pyplot(plt.gcf())

    st.subheader("Boxplot des ventes par région")
    produit = st.selectbox("Choisissez un produit :", ['Product_A', 'Product_B', 'Product_C', 'Product_D'])
    fig_box, ax_box = plt.subplots()
    sns.boxplot(data=data, x='Region', y=produit, ax=ax_box)
    st.pyplot(fig_box)

    st.subheader("Pairplot des produits")
    fig_pair = sns.pairplot(data, vars=['Product_A', 'Product_B', 'Product_C', 'Product_D'], hue='Region')
    st.pyplot(fig_pair)

# Analyse des Performances avec Filtres
elif menu == "Analyse des Performances":
    st.markdown("<h2 style='text-align:center; color:white;'>Analyse des Performances de Vente</h2>", unsafe_allow_html=True)
    st.write("")

    # Création de 2 colonnes côte à côte (largeur fixe pour uniformité)
    col1, col2 = st.columns([1, 1])

    with col1:
        selected_region = st.selectbox("Filtrer par Région", ['Toutes'] + sorted(data['Region'].unique()))

    with col2:
        selected_channel = st.selectbox("Filtrer par Canal", ['Tous'] + sorted(data['Channel'].unique()))

    filtered_data = data.copy()

    if selected_region != 'Toutes':
        filtered_data = filtered_data[filtered_data['Region'] == selected_region]

    if selected_channel != 'Tous':
        filtered_data = filtered_data[filtered_data['Channel'] == selected_channel]

    st.subheader("Répartition des Ventes")
    col3, col4 = st.columns(2)

    with col3:
        ventes = filtered_data[['Product_A', 'Product_B', 'Product_C', 'Product_D']].sum()
        fig_prod, ax_prod = plt.subplots()
        ventes.sort_values().plot.barh(ax=ax_prod, color=sns.color_palette("viridis", len(ventes)))
        ax_prod.set_xlabel("Total des Ventes")
        ax_prod.set_ylabel("Produits")
        ax_prod.set_title("Ventes Totales par Produit")
        st.pyplot(fig_prod)

    # Ventes par région
    with col4:
        region_sales = filtered_data.groupby('Region')[['Product_A', 'Product_B', 'Product_C', 'Product_D']].sum().sum(axis=1)

        if not region_sales.empty and region_sales.sum() > 0:
            fig_reg, ax_reg = plt.subplots()
            region_sales.sort_values().plot.barh(ax=ax_reg, color=sns.color_palette("muted", len(region_sales)))
            ax_reg.set_xlabel("Total des Ventes")
            ax_reg.set_ylabel("Région")
            ax_reg.set_title("Ventes par Région")
            st.pyplot(fig_reg)
        else:
            st.warning("Aucune donnée disponible pour les filtres sélectionnés.")

# Rapport
elif menu == "Rapport & Recommandations":
    st.header("Rapport & Recommandations")

    st.subheader("Tendances Observées")
    st.markdown("""
    - Le canal **Online** enregistre une forte croissance.
    - **Product_B** et **Product_D** sont les plus populaires.
    - Les jeunes clients (<30 ans) achètent plus fréquemment.
    """)

    st.subheader("Recommandations")
    st.markdown("""
    ✅ Renforcer les campagnes **en ligne**.<br>
    ✅ Cibler les jeunes avec des offres spécifiques.<br>
    ✅ Optimiser les stocks des produits les plus performants.<br>
    ✅ Analyser les périodes saisonnières.
    """, unsafe_allow_html=True)

    st.subheader("Données à Collecter à l'Avenir")
    st.markdown("""
    - Données de satisfaction client
    - Historique d'achat par client
    - Prix moyen par produit
    """)

    st.success("Projet réalisé par MOR FAYE")