from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.toolbar import MDTopAppBar
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty
from datetime import datetime
import random

class MessageBubble(MDBoxLayout):
    """Bulle de message - CORRIGÉ sans elevation"""
    def __init__(self, text, is_me, timestamp=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 80
        self.padding = [10, 5]
        
        if timestamp is None:
            timestamp = datetime.now().strftime('%H:%M')
        
        # Espace à gauche si c'est mon message
        if is_me:
            self.add_widget(MDBoxLayout(size_hint_x=0.15))
        
        # Bulle de message - SANS elevation
        bubble = MDBoxLayout(
            orientation='vertical',
            size_hint_x=0.7,
            padding=[15, 10],
            md_bg_color=(0, 0.8, 0.8, 0.15) if is_me else (0.95, 0.95, 0.95, 1)
        )
        
        # Texte
        msg_label = MDLabel(
            text=text,
            size_hint_y=0.7,
            text_size=(bubble.width - 30, None),
            theme_text_color='Custom' if is_me else 'Primary',
            text_color=(0, 0.6, 0.6, 1) if is_me else (0, 0, 0, 1)
        )
        bubble.add_widget(msg_label)
        
        # Timestamp
        time_label = MDLabel(
            text=timestamp,
            font_style='Caption',
            size_hint_y=0.3,
            halign='right',
            theme_text_color='Secondary'
        )
        bubble.add_widget(time_label)
        
        self.add_widget(bubble)
        
        # Espace à droite si c'est son message
        if not is_me:
            self.add_widget(MDBoxLayout(size_hint_x=0.15))

class ConversationScreen(Screen):
    """Écran de conversation avec AUTO-RÉPONSE - CORRIGÉ"""
    
    autre_user_id = NumericProperty(0)
    autre_username = StringProperty('')
    annonce_id = NumericProperty(0)
    
    AUTO_REPLIES = [
        "Merci pour votre message ! Je reviens vers vous rapidement.",
        "Bonjour, l'annonce est toujours disponible oui !",
        "Je vous recontacterai dans la journée 😊",
        "D'accord, quand seriez-vous disponible pour une visite ?",
        "Super ! On peut s'organiser quand vous voulez.",
        "Je suis disponible ce week-end, et vous ?",
        "Parfait ! N'hésitez pas si vous avez d'autres questions.",
        "Le prix est négociable, on peut en discuter.",
        "Je peux vous envoyer plus de photos si besoin.",
        "Oui, c'est toujours d'actualité 👍",
    ]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_user_id = 0
        self.typing_indicator = None
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical')
        
        # Toolbar
        self.toolbar = MDTopAppBar(
            title="Conversation",
            elevation=4,
            md_bg_color=(0, 0.8, 0.8, 1),
            specific_text_color=(1, 1, 1, 1),
            left_action_items=[["arrow-left", lambda x: self.go_back()]]
        )
        layout.add_widget(self.toolbar)
        
        # Zone des messages
        self.scroll = ScrollView()
        self.messages_layout = MDBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=10,
            spacing=5
        )
        self.messages_layout.bind(minimum_height=self.messages_layout.setter('height'))
        self.scroll.add_widget(self.messages_layout)
        layout.add_widget(self.scroll)
        
        # Zone de saisie
        input_layout = MDBoxLayout(
            size_hint_y=0.1,
            padding=[10, 5, 10, 5],
            spacing=10,
            md_bg_color=(0.98, 0.98, 0.98, 1)
        )
        
        self.message_input = MDTextField(
            hint_text='Écrivez votre message...',
            mode='fill',
            size_hint_x=0.8,
            multiline=False
        )
        input_layout.add_widget(self.message_input)
        
        self.btn_send = MDIconButton(
            icon='send',
            theme_text_color='Custom',
            text_color=(0, 0.8, 0.8, 1),
            size_hint_x=0.1,
            on_release=self.send_message
        )
        input_layout.add_widget(self.btn_send)
        
        layout.add_widget(input_layout)
        self.add_widget(layout)
    
    def on_enter(self):
        """Quand on arrive sur l'écran"""
        self.load_messages()
    
    def set_conversation(self, current_user_id, autre_user_id, autre_username, annonce_id=0):
        """Configurer la conversation"""
        self.current_user_id = current_user_id
        self.autre_user_id = autre_user_id
        self.autre_username = autre_username
        self.annonce_id = annonce_id
        
        self.toolbar.title = f"💬 {autre_username}"
        self.load_messages()
    
    def load_messages(self):
        """Charger les messages"""
        app = MDApp.get_running_app()
        messages = app.db.get_messages(self.current_user_id, self.autre_user_id)
        
        self.messages_layout.clear_widgets()
        
        for msg in messages:
            expediteur_id = msg[1]
            contenu = msg[4]
            date_envoi = msg[5]
            
            try:
                dt = datetime.strptime(date_envoi, '%Y-%m-%d %H:%M:%S')
                timestamp = dt.strftime('%H:%M')
            except:
                timestamp = datetime.now().strftime('%H:%M')
            
            is_me = expediteur_id == self.current_user_id
            bubble = MessageBubble(contenu, is_me, timestamp)
            self.messages_layout.add_widget(bubble)
        
        Clock.schedule_once(self.scroll_to_bottom, 0.1)
    
    def send_message(self, *args):
        """Envoyer un message"""
        text = self.message_input.text.strip()
        
        if text:
            app = MDApp.get_running_app()
            timestamp = datetime.now().strftime('%H:%M')
            
            # Sauvegarder
            app.db.envoyer_message(
                self.current_user_id,
                self.autre_user_id,
                self.annonce_id,
                text
            )
            
            # Afficher
            bubble = MessageBubble(text, True, timestamp)
            self.messages_layout.add_widget(bubble)
            self.message_input.text = ''
            
            Clock.schedule_once(self.scroll_to_bottom, 0.1)
            
            # Auto-réponse
            self.simulate_typing()
    
    def simulate_typing(self):
        """Simuler quelqu'un qui tape"""
        # Indicateur "écrit..."
        self.typing_indicator = MDBoxLayout(
            size_hint_y=None,
            height=40,
            padding=[15, 5]
        )
        
        typing_label = MDLabel(
            text=f"{self.autre_username} écrit...",
            font_style='Caption',
            theme_text_color='Secondary'
        )
        self.typing_indicator.add_widget(typing_label)
        self.messages_layout.add_widget(self.typing_indicator)
        
        Clock.schedule_once(self.scroll_to_bottom, 0.1)
        
        # Réponse après délai
        delay = random.uniform(1.5, 3.0)
        Clock.schedule_once(self.send_auto_reply, delay)
    
    def send_auto_reply(self, dt):
        """Envoyer une réponse automatique"""
        # Retirer l'indicateur
        if self.typing_indicator and self.typing_indicator in self.messages_layout.children:
            self.messages_layout.remove_widget(self.typing_indicator)
        
        # Choisir réponse
        reply = random.choice(self.AUTO_REPLIES)
        timestamp = datetime.now().strftime('%H:%M')
        
        # Sauvegarder
        app = MDApp.get_running_app()
        app.db.envoyer_message(
            self.autre_user_id,
            self.current_user_id,
            self.annonce_id,
            reply
        )
        
        # Afficher
        bubble = MessageBubble(reply, False, timestamp)
        self.messages_layout.add_widget(bubble)
        
        Clock.schedule_once(self.scroll_to_bottom, 0.1)
    
    def scroll_to_bottom(self, dt):
        """Défiler vers le bas"""
        self.scroll.scroll_y = 0
    
    def go_back(self):
        """Retour aux messages"""
        MDApp.get_running_app().sm.current = 'messages'