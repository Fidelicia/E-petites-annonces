from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import AsyncImage
from kivy.uix.gridlayout import GridLayout
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField  # 🔴 IMPORTANT : AJOUTER CETTE LIGNE !
from kivymd.uix.toolbar import MDTopAppBar

class AnnonceDetailScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.annonce_id = 0
        self.est_favori = False
        self.annonce_data = None
        self.dialog = None
        self.raison_input = None
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical')
        
        # Toolbar
        self.toolbar = MDTopAppBar(
            title="Détail annonce",
            elevation=4,
            md_bg_color=(0, 0.8, 0.8, 1),
            specific_text_color=(1, 1, 1, 1),
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            right_action_items=[["heart-outline", lambda x: self.toggle_favori()]]
        )
        layout.add_widget(self.toolbar)
        
        # ScrollView
        scroll = ScrollView()
        content = MDBoxLayout(
            orientation='vertical',
            padding=15,
            spacing=15,
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter('height'))
        
        # Image principale
        self.main_image = AsyncImage(
            size_hint=(1, None),
            height=250,
            allow_stretch=True,
            keep_ratio=True
        )
        content.add_widget(self.main_image)
        
        # Galerie
        self.gallery = GridLayout(
            cols=5,
            size_hint_y=None,
            height=80,
            spacing=5,
            padding=5
        )
        content.add_widget(self.gallery)
        
        # Titre
        self.titre = MDLabel(
            font_style='H5',
            size_hint_y=None,
            height=60,
            bold=True
        )
        content.add_widget(self.titre)
        
        # Prix
        self.prix = MDLabel(
            font_style='H4',
            theme_text_color='Custom',
            text_color=(0, 0.8, 0.8, 1),
            size_hint_y=None,
            height=50
        )
        content.add_widget(self.prix)
        
        # Informations
        info_card = MDCard(
            orientation='vertical',
            padding=15,
            spacing=10,
            size_hint_y=None,
            height=200,
            elevation=2
        )
        info_card.add_widget(MDLabel(
            text='Informations',
            font_style='Subtitle1',
            bold=True
        ))
        
        self.categorie = MDLabel(text='Catégorie: ')
        info_card.add_widget(self.categorie)
        self.localisation = MDLabel(text='Localisation: ')
        info_card.add_widget(self.localisation)
        self.date = MDLabel(text='Publié le: ')
        info_card.add_widget(self.date)
        self.vues = MDLabel(text='Vues: 0')
        info_card.add_widget(self.vues)
        content.add_widget(info_card)
        
        # Description
        desc_card = MDCard(
            orientation='vertical',
            padding=15,
            spacing=10,
            size_hint_y=None,
            elevation=2
        )
        desc_card.bind(minimum_height=desc_card.setter('height'))
        desc_card.add_widget(MDLabel(
            text='Description',
            font_style='Subtitle1',
            bold=True,
            size_hint_y=None,
            height=30
        ))
        self.description = MDLabel(
            size_hint_y=None
        )
        desc_card.add_widget(self.description)
        content.add_widget(desc_card)
        
        # Vendeur
        vendeur_card = MDCard(
            orientation='vertical',
            padding=15,
            spacing=10,
            size_hint_y=None,
            height=120,
            elevation=2
        )
        vendeur_layout = MDBoxLayout(spacing=10)
        
        self.vendeur_avatar = AsyncImage(
            source='https://ui-avatars.com/api/?name=User&size=64&background=00CED1&color=fff',
            size_hint=(0.15, 1),
            allow_stretch=True,
            keep_ratio=True
        )
        vendeur_layout.add_widget(self.vendeur_avatar)
        
        vendeur_info = MDBoxLayout(orientation='vertical', spacing=5)
        self.vendeur_nom = MDLabel(
            text='Vendeur',
            font_style='Subtitle1',
            bold=True
        )
        vendeur_info.add_widget(self.vendeur_nom)
        
        self.vendeur_telephone = MDLabel(
            text='Téléphone: ',
            font_style='Caption'
        )
        vendeur_info.add_widget(self.vendeur_telephone)
        
        vendeur_layout.add_widget(vendeur_info)
        vendeur_card.add_widget(vendeur_layout)
        content.add_widget(vendeur_card)
        
        # Boutons d'action
        actions = MDBoxLayout(
            size_hint_y=None,
            height=60,
            spacing=10,
            padding=10
        )
        
        self.btn_contacter = MDRaisedButton(
            text='CONTACTER',
            size_hint=(0.5, 1),
            md_bg_color=(0, 0.8, 0.8, 1),
            on_release=self.contacter_vendeur
        )
        actions.add_widget(self.btn_contacter)
        
        self.btn_signal = MDRaisedButton(
            text='SIGNALER',
            size_hint=(0.5, 1),
            md_bg_color=(1, 0.5, 0, 1),
            on_release=self.signaler_annonce
        )
        actions.add_widget(self.btn_signal)
        content.add_widget(actions)
        
        # Bouton supprimer
        self.btn_supprimer = MDRaisedButton(
            text='SUPPRIMER L\'ANNONCE',
            size_hint=(1, None),
            height=50,
            md_bg_color=(1, 0, 0, 1),
            on_release=self.supprimer_annonce
        )
        self.btn_supprimer.opacity = 0
        self.btn_supprimer.disabled = True
        content.add_widget(self.btn_supprimer)
        
        scroll.add_widget(content)
        layout.add_widget(scroll)
        self.add_widget(layout)
    
    def on_enter(self):
        """Chargement des données"""
        self.load_annonce()
    
    def load_annonce(self):
        """Charger les détails de l'annonce"""
        if self.annonce_id:
            app = MDApp.get_running_app()
            annonce = app.db.get_annonce_by_id(self.annonce_id)
            if annonce:
                self.annonce_data = annonce
                self.toolbar.title = annonce['titre'][:20] + '...' if len(annonce['titre']) > 20 else annonce['titre']
                
                # Images
                if annonce['image_urls'] and len(annonce['image_urls']) > 0:
                    self.main_image.source = annonce['image_urls'][0]
                    
                    # Galerie
                    self.gallery.clear_widgets()
                    for i, url in enumerate(annonce['image_urls'][:5]):
                        thumb = AsyncImage(
                            source=url,
                            size_hint=(0.2, 1),
                            allow_stretch=True,
                            keep_ratio=True
                        )
                        thumb.bind(on_touch_down=lambda x, y, idx=i: self.change_main_image(idx))
                        self.gallery.add_widget(thumb)
                
                # Texte
                self.titre.text = annonce['titre']
                self.prix.text = f"{annonce['prix']} €" if annonce['prix'] else "Prix non spécifié"
                self.categorie.text = f"Catégorie: {annonce['categorie']} / {annonce['sous_categorie']}"
                self.localisation.text = f"Localisation: {annonce['ville']}, {annonce['pays']}"
                self.date.text = f"Publié le: {annonce['date_publication'][:10]}"
                self.vues.text = f"Vues: {annonce['vues']}"
                self.description.text = annonce['description']
                
                # Vendeur
                self.vendeur_nom.text = annonce['username']
                self.vendeur_telephone.text = f"Téléphone: {annonce.get('telephone', 'Non renseigné')}"
                self.vendeur_avatar.source = f"https://ui-avatars.com/api/?name={annonce['username']}&size=64&background=00CED1&color=fff"
                
                # Propriétaire ?
                app = MDApp.get_running_app()
                if app.user and app.user['id'] == annonce['utilisateur_id']:
                    self.btn_supprimer.opacity = 1
                    self.btn_supprimer.disabled = False
                else:
                    self.btn_supprimer.opacity = 0
                    self.btn_supprimer.disabled = True
                
                # Favoris
                if app.user:
                    self.est_favori = app.db.est_favori(app.user['id'], self.annonce_id)
                    self.toolbar.right_action_items[0] = ['heart' if self.est_favori else 'heart-outline', lambda x: self.toggle_favori()]
    
    def change_main_image(self, index):
        """Changer l'image principale"""
        if self.annonce_data and self.annonce_data['image_urls']:
            if index < len(self.annonce_data['image_urls']):
                self.main_image.source = self.annonce_data['image_urls'][index]
    
    def toggle_favori(self, *args):
        """Ajouter/retirer des favoris"""
        app = MDApp.get_running_app()
        if not app.user:
            self.show_dialog("Connexion requise", "Connectez-vous pour ajouter aux favoris")
            return
        
        if self.est_favori:
            app.db.retirer_favori(app.user['id'], self.annonce_id)
            self.est_favori = False
            self.toolbar.right_action_items[0] = ['heart-outline', lambda x: self.toggle_favori()]
            self.show_dialog("Favoris", "Annonce retirée des favoris")
        else:
            app.db.ajouter_favori(app.user['id'], self.annonce_id)
            self.est_favori = True
            self.toolbar.right_action_items[0] = ['heart', lambda x: self.toggle_favori()]
            self.show_dialog("Favoris", "Annonce ajoutée aux favoris")
    
    def contacter_vendeur(self, *args):
        """Contacter le vendeur"""
        app = MDApp.get_running_app()
        if not app.user:
            self.show_dialog("Connexion requise", "Connectez-vous pour contacter le vendeur")
            return
        
        if self.annonce_data:
            conv_screen = app.sm.get_screen('conversation')
            conv_screen.set_conversation(
                app.user['id'],
                self.annonce_data['utilisateur_id'],
                self.annonce_data['username'],
                self.annonce_data['id']
            )
            app.sm.current = 'conversation'
    
    def signaler_annonce(self, *args):
        """Signaler une annonce"""
        app = MDApp.get_running_app()
        if not app.user:
            self.show_dialog("Connexion requise", "Connectez-vous pour signaler")
            return
        
        # Dialogue de signalement
        content = MDBoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        content.height = 150
        
        content.add_widget(MDLabel(
            text="Pourquoi signalez-vous cette annonce ?",
            font_style='Subtitle2'
        ))
        
        self.raison_input = MDTextField(
            hint_text="Motif du signalement",
            mode='rectangle',
            multiline=True
        )
        content.add_widget(self.raison_input)
        
        self.dialog = MDDialog(
            title="Signaler l'annonce",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="ANNULER",
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDRaisedButton(
                    text="SIGNALER",
                    md_bg_color=(1, 0.5, 0, 1),
                    on_release=self.confirmer_signalement
                )
            ]
        )
        self.dialog.open()
    
    def confirmer_signalement(self, *args):
        """Confirmer le signalement"""
        raison = self.raison_input.text.strip()
        if not raison:
            raison = "Annonce inappropriée"
        
        app = MDApp.get_running_app()
        app.db.signaler_annonce(self.annonce_id, app.user['id'], raison)
        
        self.dialog.dismiss()
        self.show_dialog("Merci", "Votre signalement a été envoyé")
    
    def supprimer_annonce(self, *args):
        """Supprimer l'annonce"""
        dialog = MDDialog(
            title="Supprimer l'annonce",
            text="Êtes-vous sûr de vouloir supprimer cette annonce ?",
            buttons=[
                MDFlatButton(
                    text="ANNULER",
                    on_release=lambda x: dialog.dismiss()
                ),
                MDRaisedButton(
                    text="SUPPRIMER",
                    md_bg_color=(1, 0, 0, 1),
                    on_release=lambda x: self.confirmer_suppression(dialog)
                )
            ]
        )
        dialog.open()
    
    def confirmer_suppression(self, dialog):
        """Confirmer la suppression"""
        dialog.dismiss()
        app = MDApp.get_running_app()
        
        if app.db.supprimer_annonce(self.annonce_id, app.user['id']):
            self.show_dialog("Succès", "Annonce supprimée")
            self.go_back()
    
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
    
    def go_back(self):
        """Retour à l'accueil"""
        MDApp.get_running_app().sm.current = 'home'