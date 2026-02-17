from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import MDList, TwoLineAvatarListItem, ImageLeftWidget
from kivy.uix.scrollview import ScrollView
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kivymd.uix.toolbar import MDTopAppBar
from widgets.navbar import Navbar

class ConversationItem(TwoLineAvatarListItem):
    def __init__(self, autre_user_id, **kwargs):
        super().__init__(**kwargs)
        self.autre_user_id = autre_user_id

class MessagesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical')
        
        self.toolbar = MDTopAppBar(
            title="💬 Messages",
            elevation=4,
            md_bg_color=(0, 0.8, 0.8, 1),
            specific_text_color=(1, 1, 1, 1),
            left_action_items=[["arrow-left", lambda x: self.go_back()]]
        )
        layout.add_widget(self.toolbar)
        
        scroll = ScrollView()
        self.conversations_list = MDList()
        scroll.add_widget(self.conversations_list)
        layout.add_widget(scroll)
        
        self.empty_label = MDLabel(
            text="💭 Aucune conversation",
            halign='center',
            theme_text_color='Secondary'
        )
        layout.add_widget(self.empty_label)
        
        layout.add_widget(Navbar())
        self.add_widget(layout)
    
    def on_enter(self):
        self.load_conversations()
    
    def load_conversations(self):
        self.conversations_list.clear_widgets()
        app = MDApp.get_running_app()
        
        if not app.user:
            self.go_back()
            return
        
        try:
            conversations = app.db.get_conversations(app.user['id'])
            
            if conversations and len(conversations) > 0:
                self.empty_label.opacity = 0
                
                for conv in conversations:
                    # Gérer les différentes longueurs de retour
                    if len(conv) >= 5:
                        autre_id = conv[0]
                        username = conv[1]
                        avatar_url = conv[2]
                        dernier_message = conv[3] if conv[3] else "Nouvelle conversation"
                        
                        item = ConversationItem(
                            text=username,
                            secondary_text=dernier_message[:50] + '...' if dernier_message and len(dernier_message) > 50 else dernier_message,
                            autre_user_id=autre_id
                        )
                        
                        avatar = ImageLeftWidget(
                            source=avatar_url or 'https://i.pravatar.cc/150?u=' + str(autre_id)
                        )
                        item.add_widget(avatar)
                        item.bind(on_release=self.open_conversation)
                        self.conversations_list.add_widget(item)
            else:
                self.empty_label.opacity = 1
        except Exception as e:
            print(f"Erreur chargement conversations: {e}")
            self.empty_label.opacity = 1
    
    def open_conversation(self, item):
        app = MDApp.get_running_app()
        conv_screen = app.sm.get_screen('conversation')
        conv_screen.set_conversation(
            app.user['id'],
            item.autre_user_id,
            item.text
        )
        app.sm.current = 'conversation'
    
    def go_back(self):
        MDApp.get_running_app().sm.current = 'home'