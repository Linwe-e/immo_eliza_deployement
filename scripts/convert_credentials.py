#!/usr/bin/env python3
"""
Script pour convertir les credentials JSON vers le format TOML pour Streamlit
"""

import json
import os

def convert_json_to_toml():
    """Convertit le fichier credentials.json au format TOML pour Streamlit"""
    
    # Chemin vers le fichier credentials
    cred_path = os.path.expanduser('~/.credentials/immo_eliza_credentials.json')
    
    print("🔄 Conversion des credentials pour Streamlit Cloud")
    print("=" * 50)
    
    if not os.path.exists(cred_path):
        print(f"❌ Fichier non trouvé : {cred_path}")
        return
    
    try:
        # Lire le fichier JSON
        with open(cred_path, 'r') as f:
            credentials = json.load(f)
        
        print("✅ Fichier JSON lu avec succès")
        print("\n📋 COPIE CE CONTENU DANS LES SECRETS STREAMLIT :")
        print("=" * 60)
        print()
          # Générer le format TOML
        print("[gcp_service_account]")
        for key, value in credentials.items():
            if isinstance(value, str):
                # Échapper les guillemets et antislashs dans les valeurs
                escaped_value = value.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
                print(f'{key} = "{escaped_value}"')
            elif isinstance(value, (int, bool)):
                print(f'{key} = {str(value).lower()}')
            else:
                # Pour tout autre type, convertir en string et échapper
                escaped_value = str(value).replace('\\', '\\\\').replace('"', '\\"')
                print(f'{key} = "{escaped_value}"')
        
        print()
        print("=" * 60)
        print("✅ Conversion terminée !")
        print()
        print("📝 Instructions :")
        print("1. Va sur https://share.streamlit.io/")
        print("2. Trouve ton app 'immoeliza-ai'") 
        print("3. Clique sur les 3 points → Settings → Secrets")
        print("4. Colle le contenu ci-dessus")
        print("5. Sauvegarde et redémarre l'app")
        
    except Exception as e:
        print(f"❌ Erreur lors de la conversion : {e}")

if __name__ == "__main__":
    convert_json_to_toml()
