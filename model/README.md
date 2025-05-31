# Dossier Model

Ce dossier contient les modèles d'apprentissage automatique pour l'application Immo Eliza.

## Fichiers requis (à placer manuellement) :

### Pour le fonctionnement de l'application :
- `pipeline_immo_eliza.pkl` : Pipeline PyCaret entraîné pour les prédictions immobilières
- `model_features.txt` : Liste des caractéristiques utilisées par le modèle

### Instructions :
1. Placez le fichier `pipeline_immo_eliza.pkl` dans ce dossier après entraînement
2. Le fichier `model_features.txt` contient la documentation des features

**Note :** Les fichiers .pkl sont ignorés par git car ils sont volumineux et peuvent contenir des données sensibles. Utilisez un système de stockage adapté (Git LFS, cloud, etc.) pour versionner les modèles.
