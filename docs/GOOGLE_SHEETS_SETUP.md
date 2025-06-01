# 🔧 Configuration Google Sheets pour Immo Eliza

Ce guide vous accompagne pour configurer l'intégration Google Sheets pour le système de feedback.

## 📋 Étapes de Configuration

### 1. Google Cloud Console - Création du Projet

1. **Accéder à Google Cloud Console**
   - Aller sur : https://console.cloud.google.com/
   - Se connecter avec votre compte Google

2. **Créer un nouveau projet**
   - Cliquer sur "Nouveau projet"
   - Nom du projet : `Immo-Eliza-Feedback`
   - Cliquer sur "Créer"

### 2. Activation des APIs

1. **Activer Google Sheets API**
   - Aller dans "APIs et Services" > "Bibliothèque"
   - Rechercher "Google Sheets API"
   - Cliquer sur "Activer"

2. **Activer Google Drive API**
   - Rechercher "Google Drive API"
   - Cliquer sur "Activer"

### 3. Création des Identifiants de Service

1. **Créer un compte de service**
   - Aller dans "APIs et Services" > "Identifiants"
   - Cliquer sur "Créer des identifiants" > "Compte de service"
   - Nom : `immo-eliza-feedback-service`
   - Description : `Service account for Immo Eliza feedback system`
   - Cliquer sur "Créer et continuer"

2. **Télécharger la clé JSON**
   - Dans la section "Comptes de service", cliquer sur le service créé
   - Aller dans l'onglet "Clés"
   - Cliquer sur "Ajouter une clé" > "Créer une clé"
   - Choisir "JSON"
   - **Sauvegarder le fichier comme `credentials.json` dans le dossier de votre projet**

### 4. Création de la Google Sheet

1. **Créer une nouvelle feuille**
   - Aller sur : https://sheets.google.com/
   - Créer une nouvelle feuille
   - Nommer la feuille : `Immo_Eliza_Feedbacks`

2. **Configurer les en-têtes** (ligne 1)
   ```
   timestamp | rating | comment | predicted_price | actual_price
   ```

3. **Partager avec le service account**
   - Copier l'email du service account depuis le fichier `credentials.json` 
     (champ "client_email")
   - Partager la Google Sheet avec cet email en mode "Éditeur"

### 5. Configuration Locale (Développement)

1. **Placer le fichier credentials.json**
   ```
   immo_eliza_deployement/
   ├── credentials.json  ← ICI
   ├── google_sheets_feedback.py
   └── feedback_form.py
   ```

2. **Tester la connexion**
   ```bash
   cd "g:\Mon Drive\BeCode\Bootcamp AI\Immo Eliza project\immo_eliza_deployement"
   python -c "from google_sheets_feedback import GoogleSheetsFeedback; gs = GoogleSheetsFeedback(); print('✅ Connexion OK' if gs.connect() else '❌ Erreur')"
   ```

### 6. Configuration Production (Streamlit Cloud)

1. **Configuration des secrets Streamlit**
   - Aller dans les paramètres de votre app Streamlit Cloud
   - Section "Secrets"
   - Ajouter le contenu complet du fichier `credentials.json` :

   ```toml
   [gcp_service_account]
   type = "service_account"
   project_id = "votre-projet-id"
   private_key_id = "votre-private-key-id"
   private_key = "-----BEGIN PRIVATE KEY-----\nVOTRE_CLE_PRIVEE\n-----END PRIVATE KEY-----\n"
   client_email = "votre-service-account@votre-projet.iam.gserviceaccount.com"
   client_id = "votre-client-id"
   auth_uri = "https://accounts.google.com/o/oauth2/auth"
   token_uri = "https://oauth2.googleapis.com/token"
   auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
   client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/votre-service-account%40votre-projet.iam.gserviceaccount.com"
   ```

### 7. Variables d'Environment

Ajouter dans les secrets Streamlit (ou variables d'environnement) :

```toml
GOOGLE_SHEET_NAME = "Immo_Eliza_Feedbacks"
```

## 🔒 Sécurité

- ⚠️ **IMPORTANT** : Ne jamais commiter le fichier `credentials.json` sur Git
- ✅ Le fichier est déjà dans `.gitignore`
- ✅ Les secrets Streamlit sont sécurisés automatiquement

## 🧪 Test de l'Installation

Une fois configuré, tester avec cette commande :

```python
from google_sheets_feedback import GoogleSheetsFeedback

# Test de connexion
gs = GoogleSheetsFeedback()
if gs.connect():
    print("✅ Configuration réussie !")
    
    # Test d'écriture
    test_data = {
        'timestamp': '2024-01-01T12:00:00',
        'rating': 5,
        'comment': 'Test de configuration',
        'predicted_price': 250000,
        'actual_price': None
    }
    
    if gs.save_feedback(test_data):
        print("✅ Sauvegarde test réussie !")
    else:
        print("❌ Erreur sauvegarde")
else:
    print("❌ Erreur de connexion")
```

## 🆘 Dépannage

### Erreur d'authentification
- Vérifier que les APIs sont activées
- Vérifier que le service account a accès à la Sheet
- Vérifier le format du fichier credentials.json

### Erreur de permission
- Vérifier que la Sheet est partagée avec le service account
- Vérifier que le nom de la Sheet est correct

### Mode Fallback
- Si Google Sheets ne fonctionne pas, le système utilisera automatiquement le CSV local
- Les données ne seront pas perdues !

---

✨ **Une fois configuré, votre système de feedback sera opérationnel avec Google Sheets !**
