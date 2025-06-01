#!/usr/bin/env python3
"""
Script de nettoyage final pour Immo Eliza
Supprime les fichiers temporaires et optimise le projet
"""

import os
import shutil
import glob

BASE_DIR = "."  # Définir le répertoire de base

def clean_project():
    """Nettoie les fichiers temporaires du projet"""
    print("🧹 Nettoyage du projet Immo Eliza...")
    
    # Fichiers et dossiers à nettoyer
    patterns_to_clean = [
        "**/__pycache__",
        "**/*.pyc", 
        "**/*.pyo",
        "**/*.log",
        "**/logs/app_main.log", 
        "**/logs/notebook_specific.log", 
        "**/test_*.py",
        "**/debug_*.py"
    ]
    
    cleaned_count = 0
    
    for pattern in patterns_to_clean:
        for item in glob.glob(pattern, recursive=True):
            try:
                if os.path.isfile(item):
                    os.remove(item)
                    print(f"  ✅ Supprimé: {item}")
                    cleaned_count += 1
                elif os.path.isdir(item):
                    shutil.rmtree(item)
                    print(f"  ✅ Supprimé dossier: {item}")
                    cleaned_count += 1
            except Exception as e:
                print(f"  ⚠️  Impossible de supprimer {item}: {e}")
    
    print(f"\n🎉 Nettoyage terminé ! {cleaned_count} éléments supprimés.")
    
    # Afficher les fichiers restants
    print("\n📁 Structure finale du projet:")
    # Walk from BASE_DIR for consistent root
    for root, dirs, files in os.walk(BASE_DIR):
        # Ignorer les dossiers cachés
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        level = root.replace(BASE_DIR, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            if not file.startswith('.'):
                print(f"{subindent}{file}")

if __name__ == "__main__":
    clean_project()
