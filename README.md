
*English README (French is below)*

# Immo Eliza AI - Belgian Real Estate Price Prediction

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains the code and resources for **Immo Eliza AI**, a project focused on predicting real estate prices in Belgium. The primary goal is to provide an interactive web application where users can get price estimations for properties based on their features.

## 🎯 Project Objectives

*   Develop a Machine Learning model to predict housing prices in Belgium.
*   Build an interactive web application using Streamlit to serve the model's predictions.
*   Deploy the application using Streamlit Sharing.

## 🚀 Technologies Used

*   **Language:** Python 3.7.11 (due to PyCaret compatibility constraints)
*   **Data Preparation & Modeling:** Pandas, NumPy, Scikit-learn, PyCaret
*   **Web Application:** Streamlit
*   **Deployment:** Streamlit Sharing

## 📁 Project Structure

```
.
├── .devcontainer
│   └── devcontainer.json       # Configuration for VS Code Dev Containers (if used)
├── .gitignore                  # Files and folders to be ignored by Git
├── model
│   ├── model_features.txt      # List of features used by the model
│   └── pipeline_immo_eliza.pkl # Serialized preprocessing pipeline and model
├── notebooks
│   ├── preprocess_code.ipynb   # Notebook for data preprocessing
│   └── setup_train_pipeline.ipynb # Notebook for PyCaret pipeline setup and training
├── app.py                      # Main script for the Streamlit application
├── README.md                   # This file
└── requirements.txt            # Python dependencies for the project
```

## 🛠️ Installation and Usage

### 1. Prerequisites

*   Python 3.7.11
*   Git

### 2. Clone the Repository

```bash
git clone https://github.com/Linwe-e/immo_eliza_deployement.git
cd immo_eliza_deployement
```

### 3. Create a Virtual Environment and Install Dependencies

It is highly recommended to use a virtual environment.

```bash
python -m venv venv
# Activate the virtual environment
# On Windows:
# venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```
*(Note: The `.devcontainer` folder suggests a Dockerized environment configuration. If you are using VS Code with the "Dev Containers" extension, it might handle environment setup and dependency installation automatically when the project is opened in a container.)*

### 4. Explore the Notebooks

The following notebooks detail the data preparation and modeling steps:

*   `notebooks/preprocess_code.ipynb`: Contains code for data cleaning, transformation, and feature engineering.
*   `notebooks/setup_train_pipeline.ipynb`: Shows how the pipeline was configured, trained, and saved using PyCaret.

To run them, you will need Jupyter Notebook or Jupyter Lab:
```bash
pip install jupyterlab # or jupyter
jupyter lab # or jupyter notebook
```
Then, open the `.ipynb` files from the Jupyter interface.

### 5. Run the Streamlit Application Locally

The Streamlit application (`app.py`) provides an interactive interface for predictions.

```bash
streamlit run app.py
```

You can then access the application in your web browser, typically at `http://localhost:8501`.

## 📦 Model

The trained Machine Learning pipeline and associated features are located in the `model/` directory:

*   `pipeline_immo_eliza.pkl`: The complete saved pipeline (preprocessing + model).
*   `model_features.txt`: The list of columns (features) expected by the model to make a prediction.

## ☁️ Deployment

This application is deployed using Streamlit Sharing and is accessible at:
**[https://immoeliza-ai.streamlit.app/](https://immoeliza-ai.streamlit.app/)**

## 🤝 Contribution

Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.

Please feel free to:
1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file (to be created if you wish to formally add one) for more details.

---

*Version Française du README*

# Immo Eliza AI - Prédiction des Prix Immobiliers en Belgique

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Ce dépôt contient le code et les ressources pour **Immo Eliza AI**, un projet axé sur la prédiction des prix de l'immobilier en Belgique. L'objectif principal est de fournir une application web interactive où les utilisateurs peuvent obtenir des estimations de prix pour des biens immobiliers en fonction de leurs caractéristiques.

## 🎯 Objectifs du Projet

*   Développer un modèle de Machine Learning pour prédire les prix des logements en Belgique.
*   Construire une application web interactive avec Streamlit pour servir les prédictions du modèle.
*   Déployer l'application en utilisant Streamlit Sharing.

## 🚀 Technologies Utilisées

*   **Langage :** Python 3.7.11 (en raison des contraintes de compatibilité avec PyCaret)
*   **Préparation des données & Modélisation :** Pandas, NumPy, Scikit-learn, PyCaret
*   **Application Web :** Streamlit
*   **Déploiement :** Streamlit Sharing

## 📁 Structure du Projet

```
.
├── .devcontainer
│   └── devcontainer.json       # Configuration pour les conteneurs de développement VS Code (si utilisé)
├── .gitignore                  # Fichiers et dossiers à ignorer par Git
├── model
│   ├── model_features.txt      # Liste des features (caractéristiques) utilisées par le modèle
│   └── pipeline_immo_eliza.pkl # Pipeline de preprocessing et modèle sérialisé
├── notebooks
│   ├── preprocess_code.ipynb   # Notebook pour le preprocessing des données
│   └── setup_train_pipeline.ipynb # Notebook pour la configuration et l'entraînement du pipeline avec PyCaret
├── app.py                      # Script principal de l'application Streamlit
├── README.md                   # Ce fichier
└── requirements.txt            # Dépendances Python du projet
```

## 🛠️ Installation et Utilisation

### 1. Prérequis

*   Python 3.7.11
*   Git

### 2. Cloner le Dépôt

```bash
git clone https://github.com/Linwe-e/immo_eliza_deployement.git
cd immo_eliza_deployement
```

### 3. Créer un Environnement Virtuel et Installer les Dépendances

Il est fortement recommandé d'utiliser un environnement virtuel.

```bash
python -m venv venv
# Activer l'environnement virtuel
# Sur Windows :
# venv\Scripts\activate
# Sur macOS/Linux :
# source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```
*(Note : Le dossier `.devcontainer` suggère une configuration d'environnement Docker. Si vous utilisez VS Code avec l'extension "Dev Containers", celle-ci pourrait gérer automatiquement la configuration de l'environnement et l'installation des dépendances à l'ouverture du projet dans un conteneur.)*

### 4. Explorer les Notebooks

Les notebooks suivants détaillent les étapes de préparation des données et de modélisation :

*   `notebooks/preprocess_code.ipynb` : Contient le code de nettoyage, de transformation et d'ingénierie des caractéristiques.
*   `notebooks/setup_train_pipeline.ipynb` : Montre comment le pipeline a été configuré, entraîné et sauvegardé en utilisant PyCaret.

Pour les exécuter, vous aurez besoin de Jupyter Notebook ou Jupyter Lab :
```bash
pip install jupyterlab # ou jupyter
jupyter lab # ou jupyter notebook
```
Ouvrez ensuite les fichiers `.ipynb` depuis l'interface Jupyter.

### 5. Lancer l'Application Streamlit Localement

L'application Streamlit (`app.py`) fournit une interface interactive pour les prédictions.

```bash
streamlit run app.py
```

Vous pourrez ensuite accéder à l'application dans votre navigateur web, généralement à l'adresse `http://localhost:8501`.

## 📦 Modèle

Le pipeline de Machine Learning entraîné et les caractéristiques associées se trouvent dans le dossier `model/` :

*   `pipeline_immo_eliza.pkl` : Le pipeline complet sauvegardé (preprocessing + modèle).
*   `model_features.txt` : La liste des colonnes (caractéristiques) attendues par le modèle pour faire une prédiction.

## ☁️ Déploiement

Cette application est déployée en utilisant Streamlit Sharing et est accessible à l'adresse :
**[https://immoeliza-ai.streamlit.app/](https://immoeliza-ai.streamlit.app/)**

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour les modifications majeures, veuillez d'abord ouvrir une "issue" pour discuter de ce que vous souhaitez modifier.

N'hésitez pas à :
1.  Forker le projet
2.  Créer votre branche de fonctionnalité (`git checkout -b feature/SuperFonctionnalite`)
3.  Commiter vos changements (`git commit -m 'Ajout de SuperFonctionnalite'`)
4.  Pousser vers la branche (`git push origin feature/SuperFonctionnalite`)
5.  Ouvrir une Pull Request

## 📜 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` (à créer si vous souhaitez ajouter formellement une licence) pour plus de détails.

---