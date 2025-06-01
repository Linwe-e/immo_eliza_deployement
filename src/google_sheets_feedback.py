#!/usr/bin/env python3
"""
Module pour gérer les feedbacks via Google Sheets
Integration sécurisée pour le projet Immo Eliza
"""

import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
from datetime import datetime
import json
import os

class GoogleSheetsFeedback:
    """Gestionnaire des feedbacks via Google Sheets avec sécurité renforcée"""
    
    def __init__(self):
        """Initialise la connexion Google Sheets"""
        self.gc = None
        self.sheet = None
        self.sheet_name = "Immo_Eliza_Feedbacks"
        self.connected = False
        self.setup_connection()
    
    def setup_connection(self):
        """Configure la connexion avec Google Sheets de manière sécurisée"""
        try:
            # En production (Streamlit Cloud), utilise les secrets
            if hasattr(st, 'secrets') and 'gcp_service_account' in st.secrets:
                credentials_info = st.secrets["gcp_service_account"]
                credentials = Credentials.from_service_account_info(
                    credentials_info,
                    scopes=[
                        'https://www.googleapis.com/auth/spreadsheets',
                        'https://www.googleapis.com/auth/drive'
                    ]
                )
                self.gc = gspread.authorize(credentials)
                
            # En développement local, utilise un fichier JSON depuis un dossier sécurisé
            else:
                # Priorité 1 : Dossier sécurisé de l'utilisateur
                secure_path = os.path.expanduser('~/.credentials/immo_eliza_credentials.json')
                
                # Priorité 2 : Dossier du projet (fallback temporaire)
                project_path = 'credentials.json'
                
                if os.path.exists(secure_path):
                    # Utilise le fichier sécurisé
                    self.gc = gspread.service_account(filename=secure_path)
                elif os.path.exists(project_path):
                    # Fallback temporaire (à éviter en production)
                    self.gc = gspread.service_account(filename=project_path)
                else:
                    # Aucune configuration trouvée
                    return False
                
            # Essaie d'ouvrir la feuille de calcul
            try:
                self.sheet = self.gc.open(self.sheet_name).sheet1
                self.connected = True
                return True
            except gspread.SpreadsheetNotFound:
                # Feuille non trouvée, on utilisera le fallback
                return False
                
        except Exception as e:
            # Erreur de connexion, on utilisera le fallback
            return False
    
    def connect(self):
        """Test la connexion à Google Sheets"""
        return self.connected
    
    def save_feedback(self, feedback_data):
        """Sauvegarde un feedback dans Google Sheets"""
        if not self.connected or not self.sheet:
            return False
        
        try:
            row_data = [
                feedback_data['timestamp'],
                feedback_data['rating'],
                feedback_data['comment'],
                feedback_data['predicted_price'],
                feedback_data['actual_price'] or ""
            ]
            
            self.sheet.append_row(row_data)
            return True
            
        except Exception as e:
            return False
    
    def get_feedback_stats(self):
        """Récupère des statistiques sur les feedbacks"""
        if not self.connected or not self.sheet:
            return None
            
        try:
            all_values = self.sheet.get_all_values()
            if len(all_values) <= 1:  # Seulement les en-têtes
                return {"total": 0, "average_rating": 0}
            
            # Calcule des stats simples
            ratings = []
            for row in all_values[1:]:  # Skip headers
                if len(row) >= 2 and row[1]:  # Rating column
                    try:
                        ratings.append(float(row[1]))
                    except:
                        continue
            
            if ratings:
                return {
                    "total": len(ratings),
                    "average_rating": round(sum(ratings) / len(ratings), 2)
                }
            else:
                return {"total": 0, "average_rating": 0}
                
        except Exception as e:
            return None
