"""
Page Signalement - CORRIGÉE (bouton retour hors formulaire)
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from database import signaler_annonce, get_annonce_by_id

def afficher_signalement():
    """Affiche le formulaire de signalement"""
    
    # Vérification utilisateur connecté
    if not st.session_state.user:
        st.warning("🔒 Connectez-vous pour signaler une annonce")
        st.session_state.page = "connexion"
        st.experimental_rerun()
        return
    
    # Récupérer l'annonce signalée
    annonce_id = st.session_state.get('signal_annonce')
    if not annonce_id:
        st.error("❌ Aucune annonce sélectionnée pour signalement")
        if st.button("← Retour à l'accueil"):
            st.session_state.page = "accueil"
            st.experimental_rerun()
        return
    
    annonce = get_annonce_by_id(annonce_id)
    
    # BOUTON RETOUR - HORS FORMULAIRE !
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← Retour"):
            st.session_state.signal_annonce = None
            st.session_state.page = "accueil"
            st.experimental_rerun()
    
    st.markdown("# ⚠️ Signaler une annonce")
    st.markdown("Aidez-nous à maintenir une communauté sûre et fiable")
    st.markdown("---")
    
    # Aperçu de l'annonce
    if annonce:
        st.markdown("### 📋 Annonce concernée")
        col_img, col_info = st.columns([1, 3])
        with col_img:
            st.image(annonce.get('image', 'https://images.pexels.com/photos/356056/pexels-photo-356056.jpeg'), width=120)
        with col_info:
            st.markdown(f"**{annonce['titre']}**")
            st.markdown(f"📍 {annonce['ville']}, {annonce['pays']}")
            st.markdown(f"**{annonce['prix']} €**")
            st.markdown(f"👤 {annonce['vendeur']}")
    
    st.markdown("---")
    
    # FORMULAIRE DE SIGNALEMENT - SANS BOUTON RETOUR À L'INTÉRIEUR !
    with st.form("signalement_form"):
        st.markdown("### 📝 Motif du signalement")
        
        type_signalement = st.selectbox(
            "Type de problème *",
            [
                "🚫 Arnaque / Fraude",
                "🔞 Contenu inapproprié",
                "📧 Spam / Publicité abusive",
                "❌ Informations fausses",
                "📋 Annonce duplicata",
                "📞 Coordonnées incorrectes",
                "❓ Autre problème"
            ]
        )
        
        description = st.text_area(
            "Description détaillée *",
            height=150,
            placeholder="Décrivez le problème en détail..."
        )
        
        confidentialite = st.checkbox(
            "Je certifie que ce signalement est fait de bonne foi *"
        )
        
        # BOUTON SUBMIT - SEUL BOUTON DANS LE FORMULAIRE
        submit = st.form_submit_button("⚠️ Signaler")
        
        if submit:
            if not description:
                st.error("❌ Veuillez fournir une description")
            elif not confidentialite:
                st.error("❌ Veuillez accepter la certification")
            else:
                # Enregistrer le signalement
                signaler_annonce(
                    annonce_id, 
                    st.session_state.user['id'], 
                    f"{type_signalement}: {description}"
                )
                
                st.success("""
                ✅ **Signalement envoyé avec succès !**
                
                **Notre équipe examinera votre signalement sous 24h.**
                
                Merci de contribuer à la sécurité de notre communauté ! 🙏
                """)
                
                # Réinitialiser
                st.session_state.signal_annonce = None
                
                # BOUTON RETOUR APRÈS SUCCÈS - HORS FORMULAIRE
                col1, col2, col3 = st.columns([1, 2, 1])
                with col1:
                    if st.button("← Retour à l'accueil", key="btn_retour_success"):
                        st.session_state.page = "accueil"
                        st.experimental_rerun()