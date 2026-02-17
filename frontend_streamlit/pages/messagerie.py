"""
Page Messagerie - CHATBOT HYPER-INTELLIGENT - CORRIGÉ
"""
import streamlit as st
import sys
import random
import time
import re
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))
from database import get_user_conversations, get_messages_between, send_message, get_user, get_annonce_by_id

# ============================================
# BASE DE CONNAISSANCES DU CHATBOT
# ============================================

INTENTIONS = {
    "salutation": {
        "mots": ["bonjour", "Salama","Manahoana","salut", "coucou", "hello", "hi", "bjr", "bonsoir", "hey"],
        "reponses": [
            "👋 Bonjour ! Merci de votre intérêt pour mon annonce.",
            "😊 Salut ! Comment puis-je vous aider ?",
            "🌟 Bonjour, ravi de vous rencontrer !",
            "🙏 Bien le bonjour ! N'hésitez pas si vous avez des questions.",
            "👐 Hello ! Je suis là pour répondre à vos questions."
        ]
    },
    "disponibilite": {
        "mots": ["disponible", "vendu", "encore", "toujours", "libre", "acheter"],
        "reponses": [
            "✅ Oui, l'article est toujours disponible à la vente !",
            "📱 Toujours d'actualité, aucun acheteur pour l'instant.",
            "🔵 Oui, c'est encore disponible ! Intéressé(e) ?",
            "✔️ Disponible ! Vous voulez plus de photos ou d'infos ?",
            "🟢 Oui, toujours en stock ! N'hésitez pas à faire une offre."
        ]
    },
    "prix": {
        "mots": ["prix", "€", "ariary","euro", "cher", "coûte", "tarif", "combien", "valeur"],
        "reponses": [
            "💰 Le prix est de {prix}€. C'est déjà très compétitif pour la qualité !",
            "💶 Je le vends {prix}€. C'est un excellent rapport qualité-prix.",
            "🏷️ Prix actuel : {prix}€. Je reste ouvert aux propositions raisonnables.",
            "💵 {prix}€. Je pense que c'est un prix juste.",
            "🪙 L'article est à {prix}Ariary. Qu'en pensez-vous ?"
        ]
    },
    "negociation": {
        "mots": ["négociable", "offre", "proposition", "réduction", "moins", "baisser", "discuter", "rabais"],
        "reponses": [
            "🤝 Je peux faire un geste. Que pensez-vous de {prix2}€ ?",
            "💰 On peut discuter. Quelle est votre offre ?",
            "🔄 Je suis ouvert à la négociation. Proposez un prix !",
            "💸 Je peux baisser un peu. Est-ce que {prix2}€ vous conviendrait ?",
            "🤲 Faisons affaire ! Je peux descendre à {prix2}€."
        ]
    },
    "visite": {
        "mots": ["visite", "voir", "rendez-vous", "rencontrer", "montrer", "déplacement", "sur place"],
        "reponses": [
            "📅 Je suis disponible cette semaine en soirée ou le week-end. Vous êtes libre quand ?",
            "📍 On peut convenir d'un rendez-vous. Où êtes-vous situé(e) ?",
            "🏠 Je peux vous montrer l'article. Êtes-vous dispo ce week-end ?",
            "🗓️ Proposez-moi un créneau, je m'adapte !",
            "🤝 On peut se donner rendez-vous dans un lieu public près de chez moi."
        ]
    },
    "etat": {
        "mots": ["état", "etat", "fonctionne", "casse", "défaut", "usure", "rayure", "neuf", "occasion", "note"],
        "reponses": [
            "✨ L'article est en parfait état, très peu utilisé (occasion proche du neuf).",
            "🔧 Tout fonctionne parfaitement, aucun défaut signalé.",
            "🆕 Comme neuf, utilisé seulement quelques fois avec précaution.",
            "⭐ Excellent état général, bien entretenu et nettoyé régulièrement.",
            "📊 Je dirais 9/10, quelques micro-rayures invisibles à l'usage normal."
        ]
    },
    "photo": {
        "mots": ["photo", "image", "visuel", "photos", "images", "voir", "cliché"],
        "reponses": [
            "📸 Je peux vous envoyer plus de photos. Quels angles vous intéressent ?",
            "📱 Je vous envoie des photos supplémentaires tout à l'heure.",
            "🖼️ Y a-t-il des détails spécifiques que vous voulez voir ?",
            "📷 Je prendrai des photos sous tous les angles ce soir.",
            "📲 Je peux vous faire une vidéo si vous voulez !"
        ]
    },
    "livraison": {
        "mots": ["livraison", "envoi", "transport", "colis", "poste", "expédition", "frais", "port"],
        "reponses": [
            "🚚 La livraison est possible en fonction du lieu. Où êtes-vous situé(e) ?",
            "📦 Je peux envoyer par colissimo. Frais de port à votre charge (environ 10€).",
            "📍 On peut se donner rendez-vous dans un lieu public pour l'échange.",
            "🚗 Je peux vous livrer si vous n'êtes pas trop loin (dans un rayon de 30km).",
            "📬 Envoi sécurisé avec assurance possible."
        ]
    },
    "garantie": {
        "mots": ["garantie", "facture", "certificat", "original", "sav", "retour", "remboursement"],
        "reponses": [
            "🛡️ La garantie est encore valable jusqu'au 12/2025 (facture fournie).",
            "📄 J'ai la facture d'achat originale, je vous la donnerai.",
            "✅ Garantie constructeur incluse, encore 1 an.",
            "🔖 Sans garantie mais article testé et fonctionnel."
        ]
    },
    "paiement": {
        "mots": ["paiement", "payer", "espèces", "carte", "cb", "virement", "paypal", "liquide"],
        "reponses": [
            "💳 Paiement accepté : espèces, virement bancaire ou PayPal.",
            "💰 Espèces de préférence pour le remise en main propre.",
            "🏦 Virement bancaire possible, je vous envoie mon RIB par message.",
            "📱 PayPal aussi, envoi en 'paiement entre proches' sans frais."
        ]
    },
    "remerciement": {
        "mots": ["merci", "thanks", "thank", "remercie"],
        "reponses": [
            "🙏 Merci à vous ! N'hésitez pas si vous avez d'autres questions.",
            "😊 Avec plaisir ! Bonne journée.",
            "✨ Je vous en prie ! Tenez-moi au courant.",
            "🌟 Merci pour votre intérêt !"
        ]
    },
    "au_revoir": {
        "mots": ["au revoir", "bye", "ciao", "à plus", "adieu", "salut","veloma"],
        "reponses": [
            "👋 Au revoir ! Bonne continuation.",
            "🖐️ À bientôt peut-être !",
            "✨ Merci et bonne journée !",
            "🌟 Au plaisir d'échanger avec vous !"
        ]
    },
    "defaut": {
        "mots": [],
        "reponses": [
            "👍 Bien reçu ! Je prends note de votre message et vous réponds rapidement.",
            "📬 Message bien reçu ! Je regarde ça et reviens vers vous.",
            "⏳ Je prends connaissance de votre message et vous réponds dans la journée.",
            "💬 Merci pour votre message ! Je vais vérifier cela.",
            "🔄 Je me renseigne et reviens vers vous sous peu."
        ]
    }
}

def detecter_intention_avancee(message, annonce=None):
    """Détection avancée de l'intention avec score"""
    msg = message.lower()
    
    scores = {}
    for intention, data in INTENTIONS.items():
        score = 0
        for mot in data["mots"]:
            if mot in msg:
                score += 1
                if re.search(r'\b' + mot + r'\b', msg):
                    score += 1
        if score > 0:
            scores[intention] = score
    
    if scores:
        return max(scores, key=scores.get)
    return "defaut"

def generer_reponse_avancee(intention, annonce=None, message=""):
    """Génère une réponse humaine et contextuelle"""
    
    reponses = INTENTIONS[intention]["reponses"]
    reponse = random.choice(reponses)
    
    if annonce:
        prix = annonce.get('prix', 0)
        if '{prix}' in reponse:
            reponse = reponse.replace('{prix}', str(prix))
        if '{prix2}' in reponse:
            prix_negocie = int(prix * random.uniform(0.8, 0.95))
            reponse = reponse.replace('{prix2}', str(prix_negocie))
    
    emoticones = ["😊", "👍", "✨", "🙂", "👌", "🤝", "💪", "🎯"]
    if random.random() > 0.7:
        reponse += " " + random.choice(emoticones)
    
    return reponse

def envoyer_reponse_chatbot_intelligent(expediteur_id, destinataire_id, annonce_id, message):
    """Envoie une réponse hyper-intelligente"""
    
    annonce = get_annonce_by_id(annonce_id) if annonce_id else None
    intention = detecter_intention_avancee(message, annonce)
    
    if intention in ["prix", "negociation"]:
        delay = random.uniform(1.5, 3.0)
    elif intention in ["garantie", "etat"]:
        delay = random.uniform(1.0, 2.0)
    else:
        delay = random.uniform(0.8, 1.8)
    
    time.sleep(delay)
    
    reponse = generer_reponse_avancee(intention, annonce, message)
    send_message(destinataire_id, expediteur_id, annonce_id, reponse)
    
    return reponse

# ============================================
# FONCTION PRINCIPALE - CORRIGÉE
# ============================================

def afficher_messagerie():
    """Page de messagerie avec chatbot intelligent"""
    
    if not st.session_state.user:
        st.warning("🔒 Connectez-vous pour accéder à la messagerie")
        st.session_state.page = "connexion"
        st.experimental_rerun()
        return
    
    st.title("💬 ChatBot - Messagerie Intelligente")
    st.markdown("*Un assistant intelligent répond automatiquement à vos messages*")
    
    # 🔴 CORRECTION ICI - Utiliser la bonne fonction !
    if st.session_state.get('selected_interlocuteur'):
        afficher_conversation()  # ← J'ai renommé en afficher_conversation()
    else:
        afficher_liste_conversations()

def afficher_liste_conversations():
    """Affiche la liste des conversations"""
    st.markdown("### 📩 Vos conversations")
    
    conversations = get_user_conversations(st.session_state.user['id'])
    
    if conversations:
        for conv in conversations:
            with st.container():
                st.markdown(f"""
                <div style="
                    background: white;
                    border-radius: 12px;
                    padding: 15px;
                    margin: 10px 0;
                    border-left: 5px solid #06D6A0;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                ">
                    <div style="display: flex; align-items: center; gap: 15px;">
                        <div style="
                            background: #06D6A0;
                            width: 50px;
                            height: 50px;
                            border-radius: 50%;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            color: white;
                            font-size: 20px;
                        ">
                            👤
                        </div>
                        <div style="flex: 1;">
                            <strong style="font-size: 16px;">{conv['interlocuteur']}</strong>
                            <p style="margin: 5px 0 0 0; color: #666; font-size: 14px;">
                                {conv['dernier_message'][:50] + '...' if conv['dernier_message'] else 'Aucun message'}
                            </p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Ouvrir", key=f"open_conv_{conv['interlocuteur_id']}"):
                    st.session_state.selected_interlocuteur = conv['interlocuteur_id']
                    st.experimental_rerun()
                st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.info("""
        💭 **Aucune conversation pour le moment**
        
        Parcourez les annonces et cliquez sur "Contacter" pour démarrer une conversation !
        Le chatbot vous répondra automatiquement.
        """)

def afficher_conversation():  # ← Renommé pour correspondre à l'appel
    """Affiche une conversation avec chatbot hyper-intelligent"""
    
    interlocuteur = get_user(st.session_state.selected_interlocuteur)
    if not interlocuteur:
        st.error("❌ Utilisateur non trouvé")
        st.session_state.selected_interlocuteur = None
        st.experimental_rerun()
        return
    
    if st.button("← Retour à la liste"):
        st.session_state.selected_interlocuteur = None
        st.experimental_rerun()
    
    st.markdown("---")
    
    # En-tête premium
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #06D6A0 0%, #118AB2 100%);
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        color: white;
        display: flex;
        align-items: center;
        gap: 20px;
    ">
        <div style="
            background: rgba(255,255,255,0.2);
            width: 80px;
            height: 80px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 40px;
            backdrop-filter: blur(10px);
        ">
            👤
        </div>
        <div style="flex: 1;">
            <h2 style="margin: 0; color: white;">{interlocuteur['username']}</h2>
            <p style="margin: 5px 0 0 0; color: rgba(255,255,255,0.9); display: flex; align-items: center; gap: 5px;">
                <span style="background: #00C851; width: 10px; height: 10px; border-radius: 50%; display: inline-block;"></span>
                En ligne (IA avancée activée)
            </p>
        </div>
        <div style="
            background: rgba(255,255,255,0.2);
            padding: 8px 16px;
            border-radius: 25px;
            font-size: 14px;
            backdrop-filter: blur(10px);
        ">
            🤖 Réponses intelligentes
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Messages
    messages = get_messages_between(st.session_state.user['id'], st.session_state.selected_interlocuteur)
    
    for msg in messages:
        msg_date = msg.get('created_at', '')
        heure = msg_date[11:16] if msg_date and len(msg_date) >= 16 else datetime.now().strftime('%H:%M')
        
        if msg['expediteur_id'] == st.session_state.user['id']:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #06D6A0 0%, #05b386 100%);
                color: white;
                padding: 12px 18px;
                border-radius: 20px 20px 4px 20px;
                margin: 10px 0 10px auto;
                max-width: 70%;
                box-shadow: 0 4px 12px rgba(6, 214, 160, 0.3);
            ">
                {msg['contenu']}
                <div style="font-size: 11px; text-align: right; margin-top: 5px; opacity: 0.8;">
                    {heure}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="
                background: white;
                color: #333;
                padding: 12px 18px;
                border-radius: 20px 20px 20px 4px;
                margin: 10px auto 10px 0;
                max-width: 70%;
                box-shadow: 0 4px 12px rgba(0,0,0,0.05);
                border-left: 4px solid #06D6A0;
            ">
                <div style="display: flex; align-items: center; gap: 5px; margin-bottom: 5px;">
                    <span style="background: #06D6A0; color: white; padding: 2px 10px; border-radius: 15px; font-size: 11px;">
                        🤖 IA
                    </span>
                    <span style="font-size: 11px; color: #666;">
                        {interlocuteur['username']} (auto)
                    </span>
                </div>
                {msg['contenu']}
                <div style="font-size: 11px; text-align: right; margin-top: 5px; color: #999;">
                    {heure} · Réponse instantanée
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Zone de saisie
    with st.form("send_message_form", clear_on_submit=True):
        st.markdown("""
        <div style="background: #f8f9fa; padding: 15px; border-radius: 15px; margin-bottom: 10px;">
            <span style="color: #06D6A0; font-weight: bold;">💭 Posez votre question</span>
            <span style="color: #666; margin-left: 10px; font-size: 13px;">
                (prix, disponibilité, état, livraison...)
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        new_message = st.text_area(
            "", 
            placeholder="Ex: Bonjour, est-ce toujours disponible ?",
            height=100
        )
        
        send_clicked = st.form_submit_button("📤 Envoyer le message")
        
        if send_clicked and new_message.strip():
            send_message(
                st.session_state.user['id'],
                st.session_state.selected_interlocuteur,
                None,
                new_message.strip()
            )
            
            with st.spinner("🤖 L'assistant intelligent réfléchit..."):
                time.sleep(random.uniform(0.8, 1.8))
            
            envoyer_reponse_chatbot_intelligent(
                st.session_state.user['id'],
                st.session_state.selected_interlocuteur,
                None,
                new_message.strip()
            )
            
            st.success("✅ Réponse instantanée générée !")
            time.sleep(0.3)
            st.experimental_rerun()