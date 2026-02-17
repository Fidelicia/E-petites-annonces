import sqlite3
import json
from pathlib import Path
from datetime import datetime

class DatabaseHelper:
    """Gestionnaire de base de données SQLite - VERSION FINALE"""
    
    def __init__(self):
        db_path = Path(__file__).parent / 'epetitesannonces.db'
        self.conn = sqlite3.connect(str(db_path))
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.insert_initial_data()
    
    def create_tables(self):
        """Créer toutes les tables"""
        
        # Table utilisateurs
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS utilisateurs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT,
                telephone TEXT,
                avatar_url TEXT,
                pays TEXT DEFAULT 'France',
                date_inscription DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table annonces
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS annonces (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                description TEXT,
                prix REAL,
                categorie TEXT,
                sous_categorie TEXT,
                utilisateur_id INTEGER,
                image_urls TEXT,
                ville TEXT,
                pays TEXT,
                date_publication DATETIME DEFAULT CURRENT_TIMESTAMP,
                statut TEXT DEFAULT 'publiee',
                vues INTEGER DEFAULT 0,
                FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs (id)
            )
        ''')
        
        # Table favoris
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS favoris (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                utilisateur_id INTEGER,
                annonce_id INTEGER,
                date_ajout DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs (id),
                FOREIGN KEY (annonce_id) REFERENCES annonces (id),
                UNIQUE(utilisateur_id, annonce_id)
            )
        ''')
        
        # Table messages
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expediteur_id INTEGER,
                destinataire_id INTEGER,
                annonce_id INTEGER,
                contenu TEXT,
                date_envoi DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (expediteur_id) REFERENCES utilisateurs (id),
                FOREIGN KEY (destinataire_id) REFERENCES utilisateurs (id),
                FOREIGN KEY (annonce_id) REFERENCES annonces (id)
            )
        ''')
        
        # Table signalements
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS signalements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                annonce_id INTEGER,
                utilisateur_id INTEGER,
                raison TEXT,
                date_signalement DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (annonce_id) REFERENCES annonces (id),
                FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs (id)
            )
        ''')
        
        # Table categories
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT UNIQUE NOT NULL,
                icone TEXT
            )
        ''')
        
        # Table sous_categories
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sous_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                categorie_id INTEGER NOT NULL,
                nom TEXT NOT NULL,
                FOREIGN KEY (categorie_id) REFERENCES categories (id)
            )
        ''')
        
        self.conn.commit()
    
    def insert_initial_data(self):
        """Insérer les données de test"""
        
        # === UTILISATEURS ===
        self.cursor.execute("SELECT COUNT(*) FROM utilisateurs")
        if self.cursor.fetchone()[0] == 0:
            utilisateurs = [
                ('test', 'test123', 'test@email.com', '0612345678', 
                 'https://i.pravatar.cc/150?u=test', 'France'),
                ('rabe', '123test', 'rabe@email.mg', '0341234567',
                 'https://i.pravatar.cc/150?u=rabe', 'Madagascar'),
                ('jean', 'pass123', 'jean@email.com', '0623456789',
                 'https://i.pravatar.cc/150?u=jean', 'France'),
                ('sophie', 'sophie123', 'sophie@email.com', '0634567890',
                 'https://i.pravatar.cc/150?u=sophie', 'France'),
            ]
            self.cursor.executemany('''
                INSERT INTO utilisateurs (username, password, email, telephone, avatar_url, pays)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', utilisateurs)
        
        # === CATÉGORIES ===
        self.cursor.execute("SELECT COUNT(*) FROM categories")
        if self.cursor.fetchone()[0] == 0:
            categories = [
                ('Immobilier', '🏠'),
                ('Véhicules', '🚗'),
                ('Emploi', '💼'),
                ('Services', '🔧'),
                ('Multimédia', '📱'),
                ('Mode', '👕'),
                ('Loisirs', '🎮'),
                ('Animaux', '🐕'),
                ('Maison', '🏡'),
            ]
            self.cursor.executemany(
                "INSERT INTO categories (nom, icone) VALUES (?, ?)",
                categories
            )
        
        # === SOUS-CATÉGORIES ===
        self.cursor.execute("SELECT COUNT(*) FROM sous_categories")
        if self.cursor.fetchone()[0] == 0:
            sous_categories = [
                # Immobilier (1)
                (1, 'Appartement'), (1, 'Maison'), (1, 'Terrain'), (1, 'Local commercial'),
                # Véhicules (2)
                (2, 'Voiture'), (2, 'Moto'), (2, 'Camionnette'), (2, '4x4'),
                # Emploi (3)
                (3, 'Informatique'), (3, 'Commercial'), (3, 'Administratif'), (3, 'Service à la personne'),
                # Services (4)
                (4, 'Cours particuliers'), (4, 'Bricolage'), (4, 'Ménage'), (4, 'Jardinage'),
                # Multimédia (5)
                (5, 'Téléphone'), (5, 'Ordinateur'), (5, 'TV'), (5, 'Console'),
                # Mode (6)
                (6, 'Vêtements'), (6, 'Chaussures'), (6, 'Accessoires'), (6, 'Montres'),
                # Loisirs (7)
                (7, 'Sports'), (7, 'Jeux'), (7, 'Livres'), (7, 'Instruments'),
                # Animaux (8)
                (8, 'Chiens'), (8, 'Chats'), (8, 'Poissons'), (8, 'Oiseaux'),
                # Maison (9)
                (9, 'Meubles'), (9, 'Électroménager'), (9, 'Décoration'), (9, 'Ustensiles'),
            ]
            self.cursor.executemany(
                "INSERT INTO sous_categories (categorie_id, nom) VALUES (?, ?)",
                sous_categories
            )
        
        # === ANNONCES ===
        self.cursor.execute("SELECT COUNT(*) FROM annonces")
        if self.cursor.fetchone()[0] == 0:
            annonces = [
                # France
                ('Appartement T2 centre ville', 'Bel appartement lumineux proche métro et commerces. Idéal pour couple ou étudiant.', 850,
                 'Immobilier', 'Appartement', 1,
                 '["https://picsum.photos/400/300?random=101"]', 'Paris', 'France'),
                ('Toyota Corolla 2020', '30.000km, clim, GPS, régulateur, entretien suivi chez Toyota. Très bon état.', 15000,
                 'Véhicules', 'Voiture', 1,
                 '["https://picsum.photos/400/300?random=102"]', 'Lyon', 'France'),
                ('Développeur Python Django', 'Startup recherche développeur Django junior. Télétravail possible.', 42000,
                 'Emploi', 'Informatique', 3,
                 '["https://picsum.photos/400/300?random=103"]', 'Toulouse', 'France'),
                ('iPhone 13 Pro', '128GB, débloqué, état neuf, sous garantie', 899,
                 'Multimédia', 'Téléphone', 4,
                 '["https://picsum.photos/400/300?random=104"]', 'Paris', 'France'),
                ('Cours de guitare', 'Professeur diplômé, 10 ans d\'expérience, tous niveaux', 25,
                 'Services', 'Cours particuliers', 4,
                 '["https://picsum.photos/400/300?random=105"]', 'Bordeaux', 'France'),
                ('Canapé 3 places', 'Canapé en cuir beige, très bon état', 350,
                 'Maison', 'Meubles', 3,
                 '["https://picsum.photos/400/300?random=106"]', 'Lille', 'France'),
                
                # Madagascar
                ('Maison à Tanjombato', '3 chambres, salon, cuisine équipée, jardin, sécurisé', 85000,
                 'Immobilier', 'Maison', 2,
                 '["https://picsum.photos/400/300?random=201"]', 'Antananarivo', 'Madagascar'),
                ('Toyota Hilux 4x4', 'Bon état, idéal pour brousse, clim, direction assistée', 35000,
                 'Véhicules', '4x4', 2,
                 '["https://picsum.photos/400/300?random=202"]', 'Toamasina', 'Madagascar'),
                ('Terrain à Ambohimangakely', '500m², viabilisé, proche route', 25000,
                 'Immobilier', 'Terrain', 2,
                 '["https://picsum.photos/400/300?random=203"]', 'Antananarivo', 'Madagascar'),
            ]
            self.cursor.executemany('''
                INSERT INTO annonces 
                (titre, description, prix, categorie, sous_categorie, utilisateur_id, image_urls, ville, pays)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', annonces)
        
        # === MESSAGES DE TEST ===
        self.cursor.execute("SELECT COUNT(*) FROM messages")
        if self.cursor.fetchone()[0] == 0:
            messages = [
                (1, 2, 1, 'Bonjour, votre annonce est toujours disponible ?'),
                (2, 1, 1, 'Oui, toujours disponible !'),
                (1, 2, 1, 'Super, je peux visiter quand ?'),
                (2, 1, 1, 'Cette semaine, je suis disponible demain après-midi'),
                (3, 1, 3, 'Bonjour, vous avez reçu d\'autres candidatures ?'),
                (1, 3, 3, 'Bonjour, oui mais vous êtes toujours en lice'),
            ]
            self.cursor.executemany('''
                INSERT INTO messages (expediteur_id, destinataire_id, annonce_id, contenu)
                VALUES (?, ?, ?, ?)
            ''', messages)
        
        self.conn.commit()
    
    # ============ UTILISATEURS ============
    
    def login(self, username, password):
        """Connecter un utilisateur"""
        self.cursor.execute(
            "SELECT * FROM utilisateurs WHERE username=? AND password=?",
            (username, password)
        )
        user = self.cursor.fetchone()
        if user:
            columns = [description[0] for description in self.cursor.description]
            return dict(zip(columns, user))
        return None
    
    def register(self, username, password, email=None, telephone=None, pays='France'):
        """Inscrire un nouvel utilisateur"""
        try:
            avatar_url = f"https://i.pravatar.cc/150?u={username}"
            self.cursor.execute('''
                INSERT INTO utilisateurs (username, password, email, telephone, avatar_url, pays)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, password, email, telephone, avatar_url, pays))
            self.conn.commit()
            return self.login(username, password)
        except sqlite3.IntegrityError:
            return None
    
    # ============ ANNONCES ============
    
    def get_annonces_recentes(self, limit=20):
        """Récupérer les annonces récentes"""
        self.cursor.execute('''
            SELECT a.*, u.username, u.avatar_url 
            FROM annonces a
            JOIN utilisateurs u ON a.utilisateur_id = u.id
            WHERE a.statut = 'publiee'
            ORDER BY a.date_publication DESC
            LIMIT ?
        ''', (limit,))
        
        annonces = []
        for row in self.cursor.fetchall():
            columns = [description[0] for description in self.cursor.description]
            annonce = dict(zip(columns, row))
            try:
                annonce['image_urls'] = json.loads(annonce['image_urls'])
            except:
                annonce['image_urls'] = ['https://picsum.photos/400/300?random=1']
            annonces.append(annonce)
        print(f"Chargement de {len(annonces)} annonces")
        return annonces
    
    def get_annonce_by_id(self, annonce_id):
        """Récupérer une annonce par son ID"""
        self.cursor.execute('''
            SELECT a.*, u.username, u.telephone, u.avatar_url 
            FROM annonces a
            JOIN utilisateurs u ON a.utilisateur_id = u.id
            WHERE a.id = ?
        ''', (annonce_id,))
        
        row = self.cursor.fetchone()
        if row:
            columns = [description[0] for description in self.cursor.description]
            annonce = dict(zip(columns, row))
            try:
                annonce['image_urls'] = json.loads(annonce['image_urls'])
            except:
                annonce['image_urls'] = ['https://picsum.photos/400/300?random=1']
            
            # Incrémenter les vues
            self.cursor.execute("UPDATE annonces SET vues = vues + 1 WHERE id = ?", (annonce_id,))
            self.conn.commit()
            return annonce
        return None
    
    def creer_annonce(self, titre, description, prix, categorie, sous_categorie, 
                     utilisateur_id, image_urls, ville, pays):
        """Créer une nouvelle annonce"""
        try:
            if not image_urls:
                import random
                image_urls = [f"https://picsum.photos/400/300?random={random.randint(1,10000)}"]
            
            image_urls_json = json.dumps(image_urls[:5])
            self.cursor.execute('''
                INSERT INTO annonces 
                (titre, description, prix, categorie, sous_categorie, utilisateur_id, image_urls, ville, pays)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (titre, description, prix, categorie, sous_categorie, utilisateur_id, 
                  image_urls_json, ville, pays))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Erreur création annonce: {e}")
            return None
    
    def supprimer_annonce(self, annonce_id, utilisateur_id):
        """Supprimer une annonce"""
        self.cursor.execute(
            "DELETE FROM annonces WHERE id = ? AND utilisateur_id = ?",
            (annonce_id, utilisateur_id)
        )
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def get_annonces_par_utilisateur(self, utilisateur_id):
        """Récupérer les annonces d'un utilisateur"""
        self.cursor.execute('''
            SELECT * FROM annonces
            WHERE utilisateur_id = ?
            ORDER BY date_publication DESC
        ''', (utilisateur_id,))
        
        annonces = []
        for row in self.cursor.fetchall():
            columns = [description[0] for description in self.cursor.description]
            annonce = dict(zip(columns, row))
            try:
                annonce['image_urls'] = json.loads(annonce['image_urls'])
            except:
                annonce['image_urls'] = ['https://picsum.photos/400/300?random=1']
            annonces.append(annonce)
        return annonces
    
    # ============ FAVORIS ============
    
    def ajouter_favori(self, utilisateur_id, annonce_id):
        """Ajouter une annonce aux favoris"""
        try:
            self.cursor.execute(
                "INSERT INTO favoris (utilisateur_id, annonce_id) VALUES (?, ?)",
                (utilisateur_id, annonce_id)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def retirer_favori(self, utilisateur_id, annonce_id):
        """Retirer une annonce des favoris"""
        self.cursor.execute(
            "DELETE FROM favoris WHERE utilisateur_id = ? AND annonce_id = ?",
            (utilisateur_id, annonce_id)
        )
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def get_favoris(self, utilisateur_id):
        """Récupérer les favoris d'un utilisateur"""
        self.cursor.execute('''
            SELECT a.* FROM annonces a
            JOIN favoris f ON a.id = f.annonce_id
            WHERE f.utilisateur_id = ?
            ORDER BY f.date_ajout DESC
        ''', (utilisateur_id,))
        
        favoris = []
        for row in self.cursor.fetchall():
            columns = [description[0] for description in self.cursor.description]
            annonce = dict(zip(columns, row))
            try:
                annonce['image_urls'] = json.loads(annonce['image_urls'])
            except:
                annonce['image_urls'] = ['https://picsum.photos/400/300?random=1']
            favoris.append(annonce)
        return favoris
    
    def est_favori(self, utilisateur_id, annonce_id):
        """Vérifier si une annonce est en favori"""
        self.cursor.execute(
            "SELECT COUNT(*) FROM favoris WHERE utilisateur_id = ? AND annonce_id = ?",
            (utilisateur_id, annonce_id)
        )
        return self.cursor.fetchone()[0] > 0
    
    # ============ MESSAGERIE ============
    
    def get_conversations(self, utilisateur_id):
        """Récupérer toutes les conversations d'un utilisateur"""
        self.cursor.execute('''
            SELECT DISTINCT 
                CASE WHEN expediteur_id = ? THEN destinataire_id ELSE expediteur_id END as autre_id,
                u.username,
                u.avatar_url,
                (SELECT contenu FROM messages m2 
                 WHERE (m2.expediteur_id = ? AND m2.destinataire_id = u.id)
                    OR (m2.expediteur_id = u.id AND m2.destinataire_id = ?)
                 ORDER BY m2.date_envoi DESC LIMIT 1) as dernier_message,
                (SELECT MAX(date_envoi) FROM messages m3
                 WHERE (m3.expediteur_id = ? AND m3.destinataire_id = u.id)
                    OR (m3.expediteur_id = u.id AND m3.destinataire_id = ?)) as date_dernier
            FROM messages m
            JOIN utilisateurs u ON u.id = CASE WHEN m.expediteur_id = ? THEN m.destinataire_id ELSE m.expediteur_id END
            WHERE m.expediteur_id = ? OR m.destinataire_id = ?
            GROUP BY autre_id
            ORDER BY date_dernier DESC
        ''', (utilisateur_id, utilisateur_id, utilisateur_id, utilisateur_id, utilisateur_id,
              utilisateur_id, utilisateur_id, utilisateur_id))
        
        return self.cursor.fetchall()
    
    def envoyer_message(self, expediteur_id, destinataire_id, annonce_id, contenu):
        """Envoyer un message"""
        self.cursor.execute('''
            INSERT INTO messages (expediteur_id, destinataire_id, annonce_id, contenu)
            VALUES (?, ?, ?, ?)
        ''', (expediteur_id, destinataire_id, annonce_id, contenu))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_messages(self, user1_id, user2_id):
        """Récupérer les messages entre deux utilisateurs"""
        self.cursor.execute('''
            SELECT m.*, u.username, u.avatar_url
            FROM messages m
            JOIN utilisateurs u ON u.id = m.expediteur_id
            WHERE (m.expediteur_id = ? AND m.destinataire_id = ?)
               OR (m.expediteur_id = ? AND m.destinataire_id = ?)
            ORDER BY m.date_envoi ASC
        ''', (user1_id, user2_id, user2_id, user1_id))
        return self.cursor.fetchall()
    
    # ============ SIGNALEMENTS ============
    
    def signaler_annonce(self, annonce_id, utilisateur_id, raison):
        """Signaler une annonce"""
        self.cursor.execute('''
            INSERT INTO signalements (annonce_id, utilisateur_id, raison)
            VALUES (?, ?, ?)
        ''', (annonce_id, utilisateur_id, raison))
        self.conn.commit()
        return self.cursor.lastrowid
    
    # ============ RECHERCHE ============
    
    def rechercher_annonces(self, mots_cles='', categorie='', ville='', prix_max=100000):
        """Recherche avancée d'annonces"""
        query = '''
            SELECT a.*, u.username, u.avatar_url 
            FROM annonces a
            JOIN utilisateurs u ON a.utilisateur_id = u.id
            WHERE a.statut = 'publiee'
        '''
        params = []
        
        if mots_cles:
            query += " AND (a.titre LIKE ? OR a.description LIKE ?)"
            params.extend([f'%{mots_cles}%', f'%{mots_cles}%'])
        
        if categorie:
            query += " AND a.categorie = ?"
            params.append(categorie)
        
        if ville:
            query += " AND a.ville LIKE ?"
            params.append(f'%{ville}%')
        
        if prix_max > 0:
            query += " AND a.prix <= ?"
            params.append(prix_max)
        
        query += " ORDER BY a.date_publication DESC LIMIT 50"
        
        self.cursor.execute(query, params)
        
        annonces = []
        for row in self.cursor.fetchall():
            columns = [description[0] for description in self.cursor.description]
            annonce = dict(zip(columns, row))
            try:
                annonce['image_urls'] = json.loads(annonce['image_urls'])
            except:
                annonce['image_urls'] = ['https://picsum.photos/400/300?random=1']
            annonces.append(annonce)
        return annonces
    
    # ============ CATÉGORIES ============
    
    def get_categories(self):
        """Récupérer toutes les catégories"""
        self.cursor.execute("SELECT id, nom FROM categories ORDER BY nom")
        return self.cursor.fetchall()
    
    def get_sous_categories(self, categorie_id):
        """Récupérer les sous-catégories d'une catégorie"""
        self.cursor.execute(
            "SELECT id, nom FROM sous_categories WHERE categorie_id = ? ORDER BY nom",
            (categorie_id,)
        )
        return self.cursor.fetchall()
    
    # ============ STATISTIQUES ============
    
    def get_statistiques_utilisateur(self, utilisateur_id):
        """Obtenir les statistiques d'un utilisateur"""
        stats = {}
        
        self.cursor.execute(
            "SELECT COUNT(*) FROM annonces WHERE utilisateur_id = ?",
            (utilisateur_id,)
        )
        stats['nb_annonces'] = self.cursor.fetchone()[0]
        
        self.cursor.execute(
            "SELECT SUM(vues) FROM annonces WHERE utilisateur_id = ?",
            (utilisateur_id,)
        )
        stats['nb_vues'] = self.cursor.fetchone()[0] or 0
        
        self.cursor.execute('''
            SELECT COUNT(*) FROM favoris f
            JOIN annonces a ON f.annonce_id = a.id
            WHERE a.utilisateur_id = ?
        ''', (utilisateur_id,))
        stats['nb_favoris_recus'] = self.cursor.fetchone()[0]
        
        return stats
    
    # ============ FERMETURE ============
    
    def fermer_connexion(self):
        """Fermer la connexion à la base de données"""
        self.conn.close()