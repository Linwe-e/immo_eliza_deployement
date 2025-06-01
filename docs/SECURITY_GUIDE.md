# 🔒 Guide de Sécurité - Credentials Google Sheets

## ✅ **Bonnes Pratiques Adoptées**

### 1. **Stockage Sécurisé Local**

**Dossier recommandé :**
```
C:\Users\[TonNom]\.credentials\immo_eliza_credentials.json
```

**Avantages :**
- ✅ Hors du projet (pas de risque de commit accidentel)
- ✅ Accessible uniquement à ton compte Windows
- ✅ Invisible pour les autres utilisateurs du PC
- ✅ Inaccessible aux outils externes (y compris moi ! 😊)

### 2. **Configuration des Permissions Windows**

```powershell
# Créer le dossier sécurisé
New-Item -ItemType Directory -Path "$env:USERPROFILE\.credentials" -Force

# Restreindre l'accès (optionnel pour plus de sécurité)
icacls "$env:USERPROFILE\.credentials" /inheritance:r /grant:r "$env:USERNAME:(OI)(CI)F"
```

### 3. **Protection Multi-Niveaux**

1. **Niveau 1** : `.gitignore` protège `credentials.json` du projet
2. **Niveau 2** : Stockage hors projet dans `~/.credentials/`
3. **Niveau 3** : Permissions Windows restrictives
4. **Niveau 4** : Secrets Streamlit pour la production

## 📋 **Instructions de Placement**

### Étape 1 : Créer le dossier sécurisé
```powershell
New-Item -ItemType Directory -Path "$env:USERPROFILE\.credentials" -Force
```

### Étape 2 : Placer le fichier JSON téléchargé
1. Télécharge le fichier JSON depuis Google Cloud Console
2. **Renomme-le** en `immo_eliza_credentials.json`
3. **Place-le** dans `C:\Users\[TonNom]\.credentials\`

### Étape 3 : Vérifier le placement
```powershell
Test-Path "$env:USERPROFILE\.credentials\immo_eliza_credentials.json"
```
Cette commande doit retourner `True`

## 🛡️ **Pourquoi c'est Sécurisé**

### Ce que PEUT voir l'Assistant IA :
- ✅ La structure de ton projet
- ✅ Les fichiers non-sensibles
- ✅ Le code de ton app

### Ce que NE PEUT PAS voir l'Assistant IA :
- ❌ Le contenu de `~/.credentials/`
- ❌ Tes clés privées Google
- ❌ Tes secrets Streamlit
- ❌ Tes données personnelles

## 🔧 **Comment ça Marche**

Notre code modifié cherche dans cet ordre :

1. **Production** : Secrets Streamlit (sécurisés par Streamlit)
2. **Développement** : `~/.credentials/immo_eliza_credentials.json` ✅ SÉCURISÉ
3. **Fallback** : `credentials.json` (projet) ⚠️ TEMPORAIRE UNIQUEMENT

## 🚨 **Règles de Sécurité**

### ✅ À FAIRE :
- Utiliser le dossier `~/.credentials/`
- Configurer les secrets Streamlit pour la production
- Garder les credentials hors du projet
- Supprimer tout credentials.json du projet après configuration

### ❌ NE JAMAIS FAIRE :
- Commiter credentials.json sur Git
- Partager le fichier JSON par email/chat
- Laisser des credentials dans le dossier de projet
- Publier des credentials dans le code

## 🎯 **Prochaines Étapes**

1. **Créer le dossier sécurisé** (commande ci-dessus)
2. **Télécharger et placer le JSON** depuis Google Cloud Console
3. **Tester la connexion** avec notre script
4. **Configurer les secrets Streamlit** pour la production

---

**✨ Avec cette configuration, tes credentials sont protégés au maximum !**
