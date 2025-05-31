#!/usr/bin/env python3
"""
Script pour convertir le modèle PyCaret en format joblib
Ce script charge le modèle PyCaret et le sauvegarde en format joblib pour réduire la taille
"""

import joblib
import os
import sys
from pycaret.regression import load_model

def convert_pycaret_to_joblib():
    """Convertit le modèle PyCaret en format joblib"""
    
    # Chemins des fichiers
    pycaret_model_path = 'model/pipeline_immo_eliza'
    joblib_model_path = 'model/pipeline_immo_eliza.joblib'
    
    try:
        print("🔄 Chargement du modèle PyCaret...")
        # Charger le modèle PyCaret
        pycaret_model = load_model(pycaret_model_path)
        print("✅ Modèle PyCaret chargé avec succès !")
        
        print("💾 Sauvegarde en format joblib...")
        # Sauvegarder avec joblib
        joblib.dump(pycaret_model, joblib_model_path, compress=3)
        print("✅ Modèle sauvegardé en format joblib !")
        
        # Afficher les tailles des fichiers
        pkl_size = os.path.getsize('model/pipeline_immo_eliza.pkl') / (1024 * 1024)  # MB
        joblib_size = os.path.getsize(joblib_model_path) / (1024 * 1024)  # MB
        
        print(f"\n📊 Comparaison des tailles :")
        print(f"   📄 PyCaret (.pkl): {pkl_size:.2f} MB")
        print(f"   📦 Joblib (.joblib): {joblib_size:.2f} MB")
        print(f"   💾 Réduction: {((pkl_size - joblib_size) / pkl_size * 100):.1f}%")
        
        print(f"\n🎉 Conversion terminée ! Le fichier joblib est prêt : {joblib_model_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la conversion : {e}")
        return False

if __name__ == "__main__":
    print("🚀 Conversion PyCaret vers Joblib")
    print("=" * 40)
    
    # Vérifier que le modèle PyCaret existe
    if not os.path.exists('model/pipeline_immo_eliza.pkl'):
        print("❌ Erreur : Le fichier 'model/pipeline_immo_eliza.pkl' n'existe pas!")
        print("   Assurez-vous que le modèle PyCaret est présent dans le dossier model/")
        sys.exit(1)
    
    # Effectuer la conversion
    success = convert_pycaret_to_joblib()
    
    if success:
        print("\n✅ Conversion réussie !")
        print("Vous pouvez maintenant pousser le fichier .joblib vers GitHub")
        print("Il sera automatiquement utilisé par l'application Streamlit")
    else:
        print("\n❌ La conversion a échoué")
        sys.exit(1)
