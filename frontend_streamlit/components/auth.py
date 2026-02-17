"""
Gestion de l'authentification
"""
import streamlit as st
from database import authenticate_user, create_user, get_user

def check_authentication():
    """Vérifie si l'utilisateur est authentifié"""
    return st.session_state.user is not None

def login_user(email, password):
    """Authentifie un utilisateur"""
    user = authenticate_user(email, password)
    if user:
        st.session_state.user = user
        return True
    return False

def register_user(username, email, password, ville=None, pays=None, telephone=None):
    """Inscrit un nouvel utilisateur"""
    user_id = create_user(username, email, password, ville, pays, telephone)
    if user_id:
        user = get_user(user_id)
        st.session_state.user = user
        return True
    return False

def logout_user():
    """Déconnecte l'utilisateur"""
    st.session_state.user = None