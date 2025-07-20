import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(layout="wide", page_title="Data Visualizer")

st.title("📊 Visualisation Avancée de Données")
st.markdown("Importez un fichier `.csv`, `.xlsx`, ou `.xls` pour explorer vos données automatiquement.")

uploaded_file = st.file_uploader("📂 Déposez un fichier ici", type=["csv", "xlsx", "xls"])

# ✅ Utiliser fichier par défaut si aucun fichier n'est importé
if uploaded_file is None:
    default_path = "Superstore.csv"
    if os.path.exists(default_path):
        df = pd.read_csv(default_path, encoding="latin1")
        st.info("✅ Aucun fichier importé. Le fichier par défaut a été utilisé.")
    else:
        st.warning("⚠️ Aucun fichier importé et le fichier par défaut est introuvable.")
        st.stop()
else:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file, encoding="latin1")
        else:
            df = pd.read_excel(uploaded_file)

    except Exception as e:
        st.error(f"❌ Erreur de lecture du fichier : {e}")
        st.stop()

# ✅ Affichage de l’aperçu
st.success("✅ Fichier chargé avec succès !")
st.write("Aperçu du fichier :", df.head())

# ➕ Préparation des colonnes
st.sidebar.header("⚙️ Paramètres d’analyse")
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
date_columns = df.select_dtypes(include=['datetime64[ns]']).columns.tolist()

# 🔁 Conversion automatique des colonnes date
for col in df.columns:
    if "date" in col.lower() or "jour" in col.lower():
        try:
            df[col] = pd.to_datetime(df[col])
            date_columns.append(col)
        except:
            pass

# ➕ Sélection des types de graphiques
chart_types = st.sidebar.multiselect("📈 Choisir des types de graphiques", [
    "Histogramme", "Barres", "Scatter", "Boxplot", "Camembert", "Lignes"
])

# Sélection dynamique des axes
x_axis = st.sidebar.selectbox("🧭 Axe X", df.columns)
y_axis = st.sidebar.selectbox("🧮 Axe Y", numeric_columns, index=0 if numeric_columns else None)
color = st.sidebar.selectbox("🎨 Couleur (optionnelle)", [None] + categorical_columns)

st.subheader("📊 Graphiques")

# 🔍 Création des graphiques
for chart_type in chart_types:
    if chart_type == "Histogramme":
        fig = px.histogram(df, x=x_axis, color=color)
    elif chart_type == "Barres":
        fig = px.bar(df, x=x_axis, y=y_axis, color=color)
    elif chart_type == "Scatter":
        fig = px.scatter(df, x=x_axis, y=y_axis, color=color)
    elif chart_type == "Boxplot":
        fig = px.box(df, x=x_axis, y=y_axis, color=color)
    elif chart_type == "Camembert":
        fig = px.pie(df, names=x_axis)
    elif chart_type == "Lignes":
        fig = px.line(df, x=x_axis, y=y_axis, color=color)
    else:
        continue
    st.plotly_chart(fig, use_container_width=True)

# ➕ Statistiques
st.subheader("📋 Statistiques descriptives")
st.write(df.describe(include='all'))

# 📅 Analyse temporelle
if date_columns:
    st.subheader("📅 Analyse temporelle")
    date_col = st.selectbox("Choisir une colonne date", date_columns)
    try:
        df['mois'] = df[date_col].dt.to_period("M").astype(str)
        df_mois = df.groupby("mois").size().reset_index(name="nombre")
        fig_mois = px.bar(df_mois, x="mois", y="nombre", title="Nombre d'entrées par mois")
        st.plotly_chart(fig_mois, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Erreur dans l’analyse temporelle : {e}")
