"""
E-petites annonces - Application Mobile
VERSION FINALE ULTIME - 100% FONCTIONNELLE
Thème: Bleu turquoise, Blanc, Noir
"""

from kivy.config import Config

# Configuration de la fenêtre
Config.set('kivy', 'window_icon', 'assets/icon.png')
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', False)

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
import sys
from pathlib import Path

# Ajouter le chemin
sys.path.append(str(Path(__file__).parent))

# ============ IMPORTS DE TOUS LES ÉCRANS ============
from database.db_helper import DatabaseHelper
from screens.login_screen import LoginScreen
from screens.home_screen import HomeScreen
from screens.annonce_detail_screen import AnnonceDetailScreen
from screens.mes_annonces_screen import MesAnnoncesScreen
from screens.publier_screen import PublierScreen
from screens.recherche_screen import RechercheScreen
from screens.favoris_screen import FavorisScreen
from screens.carte_screen import CarteScreen
from screens.profil_screen import ProfilScreen
from screens.messages_screen import MessagesScreen
from screens.conversation_screen import ConversationScreen

class EpetitesAnnoncesApp(MDApp):
    """Application principale E-petites annonces - VERSION FINALE"""
    
    def build(self):
        # Configuration du thème
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.material_style = "M3"
        
        # Gestionnaire d'écrans
        self.sm = ScreenManager()
        
        # Initialisation de la base de données
        self.db = DatabaseHelper()
        
        # Utilisateur connecté (None par défaut)
        self.user = None
        
        # ============ AJOUT DE TOUS LES ÉCRANS ============
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(AnnonceDetailScreen(name='annonce_detail'))
        self.sm.add_widget(MesAnnoncesScreen(name='mes_annonces'))
        self.sm.add_widget(PublierScreen(name='publier'))
        self.sm.add_widget(RechercheScreen(name='recherche'))
        self.sm.add_widget(FavorisScreen(name='favoris'))
        self.sm.add_widget(CarteScreen(name='carte'))          # 🗺️ CARTE INTERACTIVE
        self.sm.add_widget(ProfilScreen(name='profil'))
        self.sm.add_widget(MessagesScreen(name='messages'))
        self.sm.add_widget(ConversationScreen(name='conversation'))
        
        print("✅ Application initialisée avec succès")
        print(f"📱 Écrans chargés: {len(self.sm.screens)}")
        
        return self.sm
    
    # ============ GESTION UTILISATEUR ============
    
    def login_user(self, username, password):
        """Connecter un utilisateur"""
        try:
            user = self.db.login(username, password)
            if user:
                self.user = user
                print(f"✅ Connexion réussie: {username}")
                
                # Rafraîchir l'accueil
                home_screen = self.sm.get_screen('home')
                home_screen.load_annonces()
                
                self.sm.current = 'home'
                return True
            else:
                print(f"❌ Échec connexion: {username}")
                return False
        except Exception as e:
            print(f"❌ Erreur connexion: {e}")
            return False
    
    def register_user(self, username, password, email=None, telephone=None, pays='France'):
        """Inscrire un nouvel utilisateur"""
        try:
            user = self.db.register(username, password, email, telephone, pays)
            if user:
                self.user = user
                print(f"✅ Inscription réussie: {username}")
                
                # Rafraîchir l'accueil
                home_screen = self.sm.get_screen('home')
                home_screen.load_annonces()
                
                self.sm.current = 'home'
                return True
            else:
                print(f"❌ Échec inscription: {username}")
                return False
        except Exception as e:
            print(f"❌ Erreur inscription: {e}")
            return False
    
    def logout_user(self):
        """Déconnexion complète"""
        if self.user:
            print(f"👋 Déconnexion: {self.user['username']}")
        self.user = None
        self.sm.current = 'login'
        
        # Nettoyer les écrans si nécessaire
        for screen_name in ['home', 'profil', 'favoris', 'mes_annonces']:
            try:
                screen = self.sm.get_screen(screen_name)
                if hasattr(screen, 'clear_data'):
                    screen.clear_data()
            except:
                pass
    
    # ============ UTILITAIRES ============
    
    def get_current_user(self):
        """Récupérer l'utilisateur connecté"""
        return self.user
    
    def is_authenticated(self):
        """Vérifier si un utilisateur est connecté"""
        return self.user is not None
    
    # ============ FERMETURE ============
    
    def on_stop(self):
        """Fermer la connexion BDD à la sortie"""
        try:
            if hasattr(self, 'db'):
                self.db.fermer_connexion()
                print("✅ Base de données fermée")
        except Exception as e:
            print(f"❌ Erreur fermeture BDD: {e}")
        
        print("👋 Application terminée")


if __name__ == '__main__':
    try:
        print("🚀 Démarrage de E-petites annonces...")
        EpetitesAnnoncesApp().run()
    except Exception as e:
        print(f"❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()