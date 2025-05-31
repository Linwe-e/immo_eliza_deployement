from datetime import datetime
import streamlit as st
import pandas as pd
import os

def save_feedback_to_session(rating, comment, predicted_price, actual_price=None):
    """Sauvegarde le feedback dans session state"""
    
    try:
        # Validation des données
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            return False
        if predicted_price is None or predicted_price <= 0:
            return False
        
    except Exception as e:
        st.error(f"Erreur technique : {str(e)}")
        return False
       
    # Initialiser la liste si elle n'existe pas
    if 'all_feedback' not in st.session_state:
        st.session_state.all_feedback = []
    
    # Créer l'entrée de feedback
    feedback_entry = {
        'timestamp': datetime.now().isoformat(),
        'rating': rating,
        'comment': comment if comment else "",
        'predicted_price': predicted_price,
        'actual_price': actual_price if actual_price and actual_price > 0 else None
    }
    
    # Ajouter à la liste
    st.session_state.all_feedback.append(feedback_entry)
    
    return True

def save_feedback_to_file(rating, comment, predicted_price, actual_price=None):
    """Sauvegarde le feedback dans un fichier CSV"""
    
    try:
        # Créer le dossier s'il n'existe pas
        os.makedirs("data", exist_ok=True)
        
        feedback_entry = {
            'timestamp': datetime.now().isoformat(),
            'rating': rating,
            'comment': comment if comment else "",
            'predicted_price': predicted_price,
            'actual_price': actual_price if actual_price and actual_price > 0 else None
        }
        
        # Fichier CSV
        csv_file = "data/feedbacks.csv"
        
        # Si le fichier existe, l'ajouter, sinon le créer
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            df = pd.concat([df, pd.DataFrame([feedback_entry])], ignore_index=True)
        else:
            df = pd.DataFrame([feedback_entry])
        
        df.to_csv(csv_file, index=False)
        return True
        
    except Exception as e:
        st.error(f"Erreur lors de la sauvegarde fichier : {str(e)}")
        return False

def display_feedback_section(predicted_price):
    """Affiche la section feedback avec st.form"""
    
    # Vérifier que predicted_price est valide
    if not isinstance(predicted_price, (int, float)):
        return  # Ne pas afficher le feedback si pas de prédiction valide
    
    # Initialiser l'état si nécessaire
    if 'feedback_submitted' not in st.session_state:
        st.session_state.feedback_submitted = False
    
    st.markdown("---")
    st.markdown("### 💬 Votre avis nous intéresse !")
    
    # Vérifier si feedback déjà soumis
    if st.session_state.feedback_submitted:
        st.success("✅ Merci pour votre retour ! 🙏 Cela nous aide énormément !")
        if st.button("📝 Donner un autre avis"):
            st.session_state.feedback_submitted = False
            st.rerun()
        return
    
    with st.expander("📝 Partager votre retour", expanded=False):
        with st.form(key="feedback_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Cette prédiction vous semble-t-elle réaliste ?**")
                rating = st.select_slider(
                    "Évaluation",
                    options=[1, 2, 3, 4, 5],
                    value=3,
                    format_func=lambda x: "⭐" * x
                )
            
            with col2:
                actual_price = st.number_input(
                    "Prix réel (si vous le connaissez) 💰",
                    min_value=0,
                    value=0,
                    help="Laissez à 0 si vous ne connaissez pas le prix réel"
                )
            
            comment = st.text_area(
                "Commentaires (optionnel) 💭",
                placeholder="Partagez votre expérience, suggestions d'amélioration...",
                max_chars=500,
                help="Maximum 500 caractères"
            )
            
            submitted = st.form_submit_button("🚀 Envoyer", type="primary", use_container_width=True)
            
            if submitted:
                # Validation avant sauvegarde
                if actual_price < 0:
                    st.error("❌ Le prix ne peut pas être négatif")
                    return
                    
                if comment and len(comment) > 500:
                    st.error("❌ Le commentaire ne peut pas dépasser 500 caractères")
                    return
                
                actual_price_to_save = actual_price if actual_price > 0 else None
                
                # Sauvegarder dans session ET dans fichier CSV
                success_session = save_feedback_to_session(rating, comment, predicted_price, actual_price_to_save)
                success_file = save_feedback_to_file(rating, comment, predicted_price, actual_price_to_save)
                
                if success_session and success_file:
                    st.session_state.feedback_submitted = True
                    st.success("✅ Feedback sauvegardé avec succès !")
                    st.rerun()
                else:
                    st.error("❌ Erreur lors de la sauvegarde")

def export_feedback_to_csv():
    """Exporte les feedbacks en CSV"""
    if 'all_feedback' in st.session_state and st.session_state.all_feedback:
        df = pd.DataFrame(st.session_state.all_feedback)
        return df.to_csv(index=False)
    return None

def get_feedback_stats():
    """Retourne des statistiques sur les feedbacks"""
    if 'all_feedback' not in st.session_state or not st.session_state.all_feedback:
        return None
    
    df = pd.DataFrame(st.session_state.all_feedback)
    return {
        'total_feedback': len(df),
        'average_rating': df['rating'].mean(),
        'price_accuracy': df[df['actual_price'].notna()]['actual_price'].count()
    }

def display_feedback_admin():
    """Section admin pour gérer les feedbacks"""
    if 'all_feedback' in st.session_state and st.session_state.all_feedback:
        st.markdown("### 📊 Administration des feedbacks")
        
        # Afficher les stats
        stats = get_feedback_stats()
        if stats:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total feedbacks", stats['total_feedback'])
            with col2:
                st.metric("Note moyenne", f"{stats['average_rating']:.1f}/5")
            with col3:
                st.metric("Prix réels fournis", stats['price_accuracy'])
        
        # Bouton de téléchargement
        csv_data = export_feedback_to_csv()
        if csv_data:
            st.download_button(
                label="📥 Télécharger les feedbacks (CSV)",
                data=csv_data,
                file_name=f"feedbacks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )