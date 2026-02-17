from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivymd.app import MDApp
from kivymd.uix.toolbar import MDTopAppBar
from widgets.annonce_card import AnnonceCard
from widgets.navbar import Navbar

class RechercheScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical')
        
        # Toolbar
        self.toolbar = MDTopAppBar(
            title="Rechercher",
            elevation=4,
            md_bg_color=(0, 0.8, 0.8, 1),
            specific_text_color=(1, 1, 1, 1),
            left_action_items=[["arrow-left", lambda x: self.go_back()]]
        )
        layout.add_widget(self.toolbar)
        
        # Champ recherche
        self.search_input = MDTextField(
            hint_text='🔍 Mots-clés...',
            mode='rectangle',
            size_hint_y=None,
            height=50,
            padding=[15, 0]
        )
        layout.add_widget(self.search_input)
        
        # Bouton
        btn_search = MDRaisedButton(
            text='RECHERCHER',
            size_hint=(1, None),
            height=50,
            md_bg_color=(0, 0.8, 0.8, 1),
            on_release=self.rechercher
        )
        layout.add_widget(btn_search)
        
        # Résultats
        self.result_label = MDLabel(text='', size_hint_y=0.05)
        layout.add_widget(self.result_label)
        
        # Liste
        scroll = ScrollView()
        self.grid = GridLayout(cols=1, spacing=10, padding=15, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        scroll.add_widget(self.grid)
        layout.add_widget(scroll)
        
        # Navbar
        layout.add_widget(Navbar())
        
        self.add_widget(layout)
    
    def rechercher(self, *args):
        self.grid.clear_widgets()
        app = MDApp.get_running_app()
        
        mots = self.search_input.text
        annonces = app.db.rechercher_annonces(mots_cles=mots)
        
        self.result_label.text = f"{len(annonces)} résultat(s)"
        
        for a in annonces[:10]:
            card = AnnonceCard(
                annonce_id=a['id'],
                titre=a['titre'],
                prix=str(a['prix']) if a['prix'] else 'Prix non spécifié',
                image_url=a['image_urls'][0] if a.get('image_urls') else 'https://cdn-icons-png.flaticon.com/512/3132/3132693.png',
                ville=a['ville']
            )
            self.grid.add_widget(card)
    
    def go_back(self):
        MDApp.get_running_app().sm.current = 'home'