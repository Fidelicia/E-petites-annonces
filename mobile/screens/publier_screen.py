from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivy.uix.image import AsyncImage
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from widgets.navbar import Navbar

class PublierScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image_urls = []
        self.categories = []
        self.sous_categories = []
        self.categorie_id = None
        self.menu_categorie = None
        self.menu_sous_categorie = None
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical')
        
        # Toolbar
        self.toolbar = MDTopAppBar(
            title="Publier une annonce",
            elevation=4,
            md_bg_color=(0, 0.8, 0.8, 1),
            specific_text_color=(1, 1, 1, 1),
            left_action_items=[["arrow-left", lambda x: self.go_back()]]
        )
        layout.add_widget(self.toolbar)
        
        # ScrollView
        scroll = ScrollView()
        form = MDBoxLayout(
            orientation='vertical',
            padding=20,
            spacing=15,
            size_hint_y=None
        )
        form.bind(minimum_height=form.setter('height'))
        
        # ===== ZONE IMAGES =====
        self.image_container = GridLayout(cols=3, spacing=5, size_hint_y=None, height=100)
        form.add_widget(self.image_container)
        
        btn_photo = MDRaisedButton(
            text='➕ AJOUTER PHOTO',
            size_hint=(1, None),
            height=40,
            md_bg_color=(0, 0.8, 0.8, 0.8),
            on_release=self.add_image
        )
        form.add_widget(btn_photo)
        
        # ===== TITRE =====
        self.titre_input = MDTextField(
            hint_text='Titre de l\'annonce *',
            mode='rectangle',
            size_hint_y=None,
            height=50
        )
        form.add_widget(self.titre_input)
        
        # ===== CATÉGORIE - SOLUTION SIMPLE ! =====
        self.categorie_input = MDTextField(
            hint_text='Catégorie *',
            mode='rectangle',
            size_hint_y=None,
            height=50,
            readonly=False,  # ← On peut écrire mais on va utiliser le bouton
            on_touch_down=self.open_categories_menu  # ← Changement important !
        )
        form.add_widget(self.categorie_input)
        
        # ===== SOUS-CATÉGORIE =====
        self.sous_categorie_input = MDTextField(
            hint_text='Sous-catégorie *',
            mode='rectangle',
            size_hint_y=None,
            height=50,
            readonly=False,
            on_touch_down=self.open_sous_categories_menu,
            disabled=True
        )
        form.add_widget(self.sous_categorie_input)
        
        # ===== PRIX =====
        self.prix_input = MDTextField(
            hint_text='Prix (€)',
            mode='rectangle',
            size_hint_y=None,
            height=50
        )
        form.add_widget(self.prix_input)
        
        # ===== DESCRIPTION =====
        self.description_input = MDTextField(
            hint_text='Description détaillée *',
            mode='rectangle',
            size_hint_y=None,
            height=120,
            multiline=True
        )
        form.add_widget(self.description_input)
        
        # ===== VILLE =====
        self.ville_input = MDTextField(
            hint_text='Ville *',
            mode='rectangle',
            size_hint_y=None,
            height=50
        )
        form.add_widget(self.ville_input)
        
        # ===== BOUTON PUBLIER =====
        btn_publier = MDRaisedButton(
            text='✅ PUBLIER L\'ANNONCE',
            size_hint=(1, None),
            height=50,
            md_bg_color=(0, 0.8, 0.8, 1),
            font_size=16,
            on_release=self.publier_annonce
        )
        form.add_widget(btn_publier)
        
        scroll.add_widget(form)
        layout.add_widget(scroll)
        layout.add_widget(Navbar())
        
        self.add_widget(layout)
    
    def on_enter(self):
        """Charger les catégories"""
        app = MDApp.get_running_app()
        self.categories = app.db.get_categories()
        # Pré-remplir pour test
        self.titre_input.text = f"Test {__import__('datetime').datetime.now().strftime('%H:%M:%S')}"
        self.ville_input.text = "Paris"
    
    def open_categories_menu(self, instance, touch):
        """Ouvrir le menu des catégories au clic"""
        if not self.categories:
            return
        
        if instance.collide_point(*touch.pos):
            items = []
            for cat_id, cat_nom in self.categories:
                items.append({
                    "text": cat_nom,
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=cat_id, y=cat_nom: self.select_categorie(x, y)
                })
            
            self.menu_categorie = MDDropdownMenu(
                caller=instance,
                items=items,
                width_mult=4,
                position="bottom"
            )
            self.menu_categorie.open()
            return True
    
    def select_categorie(self, cat_id, cat_nom):
        """Sélectionner une catégorie"""
        self.categorie_id = cat_id
        self.categorie_input.text = cat_nom
        self.sous_categorie_input.text = ''
        self.sous_categorie_input.disabled = False
        
        # Charger les sous-catégories
        app = MDApp.get_running_app()
        self.sous_categories = app.db.get_sous_categories(cat_id)
        
        if self.menu_categorie:
            self.menu_categorie.dismiss()
    
    def open_sous_categories_menu(self, instance, touch):
        """Ouvrir le menu des sous-catégories"""
        if not self.sous_categories:
            return
        
        if instance.collide_point(*touch.pos):
            items = []
            for sc_id, sc_nom in self.sous_categories:
                items.append({
                    "text": sc_nom,
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=sc_nom: self.select_sous_categorie(x)
                })
            
            self.menu_sous_categorie = MDDropdownMenu(
                caller=instance,
                items=items,
                width_mult=4,
                position="bottom"
            )
            self.menu_sous_categorie.open()
            return True
    
    def select_sous_categorie(self, sc_nom):
        """Sélectionner une sous-catégorie"""
        self.sous_categorie_input.text = sc_nom
        if self.menu_sous_categorie:
            self.menu_sous_categorie.dismiss()
    
    def add_image(self, *args):
        """Ajouter une image"""
        if len(self.image_urls) < 3:
            import random
            url = f"https://picsum.photos/400/300?random={random.randint(1,10000)}"
            self.image_urls.append(url)
            self.refresh_images()
    
    def refresh_images(self):
        """Rafraîchir l'affichage des images"""
        self.image_container.clear_widgets()
        for url in self.image_urls:
            img = AsyncImage(
                source=url,
                size_hint=(1, 1),
                allow_stretch=True,
                keep_ratio=True
            )
            self.image_container.add_widget(img)
    
    def publier_annonce(self, *args):
        """Publier l'annonce"""
        app = MDApp.get_running_app()
        
        if not app.user:
            self.show_dialog("Erreur", "Vous devez être connecté")
            return
        
        # Validation
        if not self.titre_input.text:
            self.show_dialog("Erreur", "Titre requis")
            return
        if not self.categorie_input.text:
            self.show_dialog("Erreur", "Catégorie requise")
            return
        if not self.sous_categorie_input.text:
            self.show_dialog("Erreur", "Sous-catégorie requise")
            return
        if not self.description_input.text:
            self.show_dialog("Erreur", "Description requise")
            return
        if not self.ville_input.text:
            self.show_dialog("Erreur", "Ville requise")
            return
        
        # Prix
        try:
            prix = float(self.prix_input.text) if self.prix_input.text else None
        except:
            prix = None
        
        # Images par défaut
        if not self.image_urls:
            import random
            self.image_urls = [f"https://picsum.photos/400/300?random={random.randint(1,10000)}"]
        
        # Créer l'annonce
        annonce_id = app.db.creer_annonce(
            titre=self.titre_input.text,
            description=self.description_input.text,
            prix=prix,
            categorie=self.categorie_input.text,
            sous_categorie=self.sous_categorie_input.text,
            utilisateur_id=app.user['id'],
            image_urls=self.image_urls,
            ville=self.ville_input.text,
            pays=app.user.get('pays', 'France')
        )
        
        if annonce_id:
            self.show_dialog("Succès", "✅ Annonce publiée !")
            # FORCER le rafraîchissement de l'accueil
            home_screen = app.sm.get_screen('home')
            home_screen.load_annonces()
            self.clear_form()
            self.go_back()
        else:
            self.show_dialog("Erreur", "❌ Échec de la publication")
    
    def show_dialog(self, title, text):
        """Afficher une boîte de dialogue"""
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
    
    def clear_form(self):
        """Nettoyer le formulaire"""
        self.titre_input.text = ''
        self.categorie_input.text = ''
        self.sous_categorie_input.text = ''
        self.prix_input.text = ''
        self.description_input.text = ''
        self.ville_input.text = ''
        self.image_urls = []
        self.image_container.clear_widgets()
        self.sous_categorie_input.disabled = True
    
    def go_back(self):
        """Retour à l'accueil"""
        MDApp.get_running_app().sm.current = 'home'