# Projet de Surveillance Faciale

Ce projet utilise **OpenCV**, **face_recognition**, **SQLite** et **Streamlit** pour détecter des visages, enregistrer les identités dans une base de donnee SQLite et afficher un tableau de bord en temps réel. Une alarme est déclenchée si un visage inconnu est détecté.


## Fonctionnalités

- Reconnaissance faciale avec `face_recognition`
- Enregistrement des détections dans une base SQLite
- Déclenchement d'une **alarme sonore** en cas de visage inconnu
- Tableau de bord interactif via **Streamlit**
- Filtrage par nom, visualisation par jour et par personne


## Étapes d'Installation

1. Installe les dépendances nécessaires :

`pip install opencv-python face_recognition numpy pygame streamlit pandas`

---------

2. Placez `SignaturesAll.npy` dans ce dossier.

---------

3. Lancez la détection :

`python Reconnaissance_faciale.py`

---------

4. Lancez le tableau de bord :

`streamlit run dashboard.py`