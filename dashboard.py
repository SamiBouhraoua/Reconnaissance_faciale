import streamlit as st
import sqlite3
import pandas as pd


def login():
    st.title("Connexion")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if username == "sami" and password == "sami":
            st.session_state["logged_in"] = True
        else:
            st.error("Identifiants incorrects")



def dashboard():
    st.title("Dashbord")

    connection = sqlite3.connect("database.db")
    db = pd.read_sql_query("SELECT * FROM detections", connection)

    # sidebar
    with st.sidebar:
        st.header("Filtres")
        noms = db["nom"].unique().tolist()
        nom_select = st.selectbox("Nom", ["Tous"] + noms)

    if nom_select != "Tous":
        db = db[db["nom"] == nom_select]


    st.subheader("Historique des détections")
    st.dataframe(db)


    st.subheader("Nombre de détections par personne")
    st.bar_chart(db["nom"].value_counts())


    st.subheader("Nombre de détections par jour")
    st.bar_chart(db["date"].str[:10].value_counts().sort_index())



# initialiser la clé de session (logged_in)
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
else:
    dashboard()