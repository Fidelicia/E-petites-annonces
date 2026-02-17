"""
Base de données - VERSION FINALE CORRIGÉE
"""
import sqlite3
import os
from datetime import datetime
import hashlib
import random

DB_PATH = "annonces.db"

# Images par catégorie - PEXELS (toujours disponibles)
CATEGORY_IMAGES = {
    'Immobilier': 'https://images.pexels.com/photos/106399/pexels-photo-106399.jpeg',
    'Véhicules': 'https://images.pexels.com/photos/170811/pexels-photo-170811.jpeg',
    'Multimédia': 'https://images.pexels.com/photos/607812/pexels-photo-607812.jpeg',
    'Maison': 'https://images.pexels.com/photos/276583/pexels-photo-276583.jpeg',
    'Loisirs': 'https://images.pexels.com/photos/261985/pexels-photo-261985.jpeg',
    'Mode': 'https://images.pexels.com/photos/994523/pexels-photo-994523.jpeg',
    'Services': 'https://images.pexels.com/photos/3184292/pexels-photo-3184292.jpeg',
    'Emplois': 'https://images.pexels.com/photos/3760067/pexels-photo-3760067.jpeg',
    'Produits locaux': 'https://images.pexels.com/photos/4110250/pexels-photo-4110250.jpeg',
    'Autres': 'https://images.pexels.com/photos/356056/pexels-photo-356056.jpeg',
}

def init_db():
    """Initialise la base de données"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Table des utilisateurs
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS utilisateurs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        ville TEXT,
        pays TEXT DEFAULT 'France',
        telephone TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Table des catégories
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT UNIQUE NOT NULL,
        icone TEXT DEFAULT '📦'
    )
    ''')
    
    # Table des annonces
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS annonces (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titre TEXT NOT NULL,
        description TEXT NOT NULL,
        prix REAL NOT NULL,
        categorie_id INTEGER,
        utilisateur_id INTEGER NOT NULL,
        ville TEXT NOT NULL,
        pays TEXT DEFAULT 'France',
        image_path TEXT,
        promu BOOLEAN DEFAULT 0,
        vues INTEGER DEFAULT 0,
        statut TEXT DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (categorie_id) REFERENCES categories(id),
        FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id)
    )
    ''')
    
    # Table des favoris
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS favoris (
        utilisateur_id INTEGER,
        annonce_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (utilisateur_id, annonce_id),
        FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id),
        FOREIGN KEY (annonce_id) REFERENCES annonces(id)
    )
    ''')
    
    # Table des messages
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        expediteur_id INTEGER NOT NULL,
        destinataire_id INTEGER NOT NULL,
        annonce_id INTEGER,
        contenu TEXT NOT NULL,
        lu BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (expediteur_id) REFERENCES utilisateurs(id),
        FOREIGN KEY (destinataire_id) REFERENCES utilisateurs(id),
        FOREIGN KEY (annonce_id) REFERENCES annonces(id)
    )
    ''')
    
    # Table des signalements
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS signalements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        annonce_id INTEGER NOT NULL,
        utilisateur_id INTEGER NOT NULL,
        raison TEXT NOT NULL,
        statut TEXT DEFAULT 'en attente',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (annonce_id) REFERENCES annonces(id),
        FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id)
    )
    ''')
    
    # Insertion des catégories
    categories = [
        ('Immobilier', '🏠'),
        ('Véhicules', '🚗'),
        ('Multimédia', '💻'),
        ('Maison', '🛋️'),
        ('Loisirs', '🎮'),
        ('Mode', '👗'),
        ('Services', '🔧'),
        ('Emplois', '💼'),
        ('Produits locaux', '🌱'),
        ('Autres', '📦')
    ]
    
    for nom, icone in categories:
        cursor.execute('''
        INSERT OR IGNORE INTO categories (nom, icone) VALUES (?, ?)
        ''', (nom, icone))
    
    # Admin par défaut
    admin_email = 'admin@admin.com'
    admin_pass = hashlib.sha256('admin123'.encode()).hexdigest()
    
    cursor.execute('SELECT * FROM utilisateurs WHERE email = ?', (admin_email,))
    if not cursor.fetchone():
        cursor.execute('''
        INSERT INTO utilisateurs (username, email, password, ville, pays) 
        VALUES (?, ?, ?, ?, ?)
        ''', ('admin', admin_email, admin_pass, 'Paris', 'France'))
    
    conn.commit()
    
    # === ANNONCES PAR DÉFAUT ===
    cursor.execute('SELECT COUNT(*) FROM annonces')
    if cursor.fetchone()[0] == 0:
        # Annonces France
        annonces_france = [
            ('Appartement T2 Paris Centre', 'Bel appartement lumineux proche métro, commerces et parcs. Idéal pour couple ou étudiant.', 850, 1, 1, 'Paris', 'France'),
            ('Toyota Corolla 2020', '30.000km, clim, GPS, régulateur, entretien suivi. Très bon état.', 15000, 2, 1, 'Lyon', 'France'),
            ('iPhone 13 Pro 256Go', 'Débloqué, état neuf, batterie 100%, sous garantie jusqu\'à déc 2024.', 899, 3, 1, 'Paris', 'France'),
            ('Canapé 3 places cuir', 'Canapé en cuir véritable, couleur beige, très bon état.', 450, 4, 1, 'Toulouse', 'France'),
            ('Vélo course Carbone', 'Vélo de course professionnel, cadre carbone 56cm, groupe Shimano 105.', 1200, 5, 1, 'Bordeaux', 'France'),
        ]
        
        for a in annonces_france:
            image = CATEGORY_IMAGES.get('Immobilier' if a[2] == 850 else 'Véhicules' if a[2] == 15000 else 'Multimédia' if a[2] == 899 else 'Maison' if a[2] == 450 else 'Loisirs')
            cursor.execute('''
            INSERT INTO annonces (titre, description, prix, categorie_id, utilisateur_id, ville, pays, image_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (a[0], a[1], a[2], a[3], a[4], a[5], a[6], image))
        
        # Annonces Madagascar
        annonces_mada = [
            ('Maison Tanjombato', 'Belle maison 3 chambres, salon, cuisine équipée, jardin, garage, sécurisé.', 85000, 1, 1, 'Antananarivo', 'Madagascar'),
            ('Toyota Hilux 4x4', 'Pick-up 4x4, excellent état, clim, direction assistée, idéal pour brousse.', 35000, 2, 1, 'Toamasina', 'Madagascar'),
            ('Terrain Ambohimangakely', 'Terrain 500m² viabilisé, proche route, idéal pour construction.', 25000, 1, 1, 'Antananarivo', 'Madagascar'),
            ('Cours de guitare', 'Professeur diplômé, 10 ans d\'expérience, cours à domicile tous niveaux.', 25, 7, 1, 'Antananarivo', 'Madagascar'),
            ('Foulards artisanaux', 'Foulards en soie naturelle, fabrication artisanale malgache, motifs traditionnels.', 45, 6, 1, 'Antsirabe', 'Madagascar'),
        ]
        
        for a in annonces_mada:
            if a[2] == 85000 or a[2] == 25000:
                image = CATEGORY_IMAGES['Immobilier']
            elif a[2] == 35000:
                image = CATEGORY_IMAGES['Véhicules']
            elif a[2] == 25:
                image = CATEGORY_IMAGES['Services']
            else:
                image = CATEGORY_IMAGES['Mode']
                
            cursor.execute('''
            INSERT INTO annonces (titre, description, prix, categorie_id, utilisateur_id, ville, pays, image_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (a[0], a[1], a[2], a[3], a[4], a[5], a[6], image))
    
    conn.commit()
    conn.close()
    os.makedirs("uploads", exist_ok=True)

# ============================================
# FONCTIONS UTILISATEURS
# ============================================

def hash_password(password):
    """Hash le mot de passe"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, email, password, ville=None, pays=None, telephone=None):
    """Crée un nouvel utilisateur"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        hashed_password = hash_password(password)
        cursor.execute('''
        INSERT INTO utilisateurs (username, email, password, ville, pays, telephone) 
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, email, hashed_password, ville, pays, telephone))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Erreur création utilisateur: {e}")
        return None
    finally:
        conn.close()

def authenticate_user(email, password):
    """Authentifie un utilisateur"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    
    cursor.execute('''
    SELECT id, username, email, ville, pays 
    FROM utilisateurs 
    WHERE email = ? AND password = ?
    ''', (email, hashed_password))
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'ville': user[3],
            'pays': user[4]
        }
    return None

def get_user(user_id):
    """Récupère un utilisateur par ID"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT id, username, email, ville, pays, telephone, created_at
    FROM utilisateurs WHERE id = ?
    ''', (user_id,))
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'ville': user[3],
            'pays': user[4],
            'telephone': user[5],
            'created_at': user[6]
        }
    return None

def update_user(user_id, ville=None, pays=None, telephone=None):
    """Met à jour les informations d'un utilisateur"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    updates = []
    params = []
    
    if ville:
        updates.append("ville = ?")
        params.append(ville)
    if pays:
        updates.append("pays = ?")
        params.append(pays)
    if telephone:
        updates.append("telephone = ?")
        params.append(telephone)
    
    if updates:
        params.append(user_id)
        query = f"UPDATE utilisateurs SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
        success = True
    else:
        success = False
    
    conn.close()
    return success

# ============================================
# FONCTIONS ANNONCES
# ============================================

def create_annonce(titre, description, prix, categorie, utilisateur_id, ville, pays, image_path=None, promu=False):
    """Crée une nouvelle annonce"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Récupérer l'ID de la catégorie
    cursor.execute('SELECT id FROM categories WHERE nom = ?', (categorie,))
    cat = cursor.fetchone()
    categorie_id = cat[0] if cat else 10
    
    # Image par défaut si non fournie
    if not image_path:
        image_path = CATEGORY_IMAGES.get(categorie, CATEGORY_IMAGES['Autres'])
    
    cursor.execute('''
    INSERT INTO annonces (titre, description, prix, categorie_id, utilisateur_id, ville, pays, image_path, promu, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (titre, description, prix, categorie_id, utilisateur_id, ville, pays, image_path, 1 if promu else 0, datetime.now()))
    
    annonce_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return annonce_id

def get_all_annonces(limit=20, offset=0, categorie=None, ville=None, pays=None, search=None, prix_min=None, prix_max=None):
    """Récupère toutes les annonces avec filtres"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    query = '''
    SELECT a.*, c.nom as categorie, c.icone, u.username as vendeur, u.id as user_id
    FROM annonces a
    JOIN categories c ON a.categorie_id = c.id
    JOIN utilisateurs u ON a.utilisateur_id = u.id
    WHERE a.statut = 'active'
    '''
    params = []
    
    if categorie and categorie != 'Toutes':
        query += ' AND c.nom = ?'
        params.append(categorie)
    if ville:
        query += ' AND a.ville LIKE ?'
        params.append(f'%{ville}%')
    if pays and pays != 'Tous':
        query += ' AND a.pays = ?'
        params.append(pays)
    if search:
        query += ' AND (a.titre LIKE ? OR a.description LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%'])
    if prix_min:
        query += ' AND a.prix >= ?'
        params.append(prix_min)
    if prix_max:
        query += ' AND a.prix <= ?'
        params.append(prix_max)
    
    query += ' ORDER BY a.promu DESC, a.created_at DESC LIMIT ? OFFSET ?'
    params.extend([limit, offset])
    
    cursor.execute(query, params)
    annonces = [dict(row) for row in cursor.fetchall()]
    
    # Ajouter l'URL de l'image
    for a in annonces:
        if a['image_path']:
            a['image'] = a['image_path']
        else:
            a['image'] = CATEGORY_IMAGES.get(a['categorie'], CATEGORY_IMAGES['Autres'])
    
    conn.close()
    return annonces

def get_annonce_by_id(annonce_id):
    """Récupère une annonce par ID"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT a.*, c.nom as categorie, c.icone, u.username as vendeur, u.id as user_id, u.email, u.telephone
    FROM annonces a
    JOIN categories c ON a.categorie_id = c.id
    JOIN utilisateurs u ON a.utilisateur_id = u.id
    WHERE a.id = ?
    ''', (annonce_id,))
    
    annonce = cursor.fetchone()
    
    if annonce:
        cursor.execute('UPDATE annonces SET vues = vues + 1 WHERE id = ?', (annonce_id,))
        conn.commit()
        annonce = dict(annonce)
        
        # Ajouter l'URL de l'image
        if annonce['image_path']:
            annonce['image'] = annonce['image_path']
        else:
            annonce['image'] = CATEGORY_IMAGES.get(annonce['categorie'], CATEGORY_IMAGES['Autres'])
    
    conn.close()
    return annonce

def get_user_annonces(user_id):
    """Récupère les annonces d'un utilisateur"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT a.*, c.nom as categorie
    FROM annonces a
    JOIN categories c ON a.categorie_id = c.id
    WHERE a.utilisateur_id = ? AND a.statut = 'active'
    ORDER BY a.created_at DESC
    ''', (user_id,))
    
    annonces = [dict(row) for row in cursor.fetchall()]
    
    for a in annonces:
        if not a['image_path']:
            a['image'] = CATEGORY_IMAGES.get(a['categorie'], CATEGORY_IMAGES['Autres'])
        else:
            a['image'] = a['image_path']
    
    conn.close()
    return annonces

def delete_annonce(annonce_id, user_id):
    """Supprime une annonce (soft delete)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE annonces SET statut = 'supprimee' 
    WHERE id = ? AND utilisateur_id = ?
    ''', (annonce_id, user_id))
    conn.commit()
    rows = cursor.rowcount
    conn.close()
    return rows > 0

# ============================================
# FONCTIONS FAVORIS
# ============================================

def toggle_favori(user_id, annonce_id):
    """Ajoute/retire une annonce des favoris"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM favoris WHERE utilisateur_id = ? AND annonce_id = ?', 
                  (user_id, annonce_id))
    
    if cursor.fetchone():
        cursor.execute('DELETE FROM favoris WHERE utilisateur_id = ? AND annonce_id = ?', 
                      (user_id, annonce_id))
        action = 'removed'
    else:
        cursor.execute('INSERT INTO favoris (utilisateur_id, annonce_id) VALUES (?, ?)', 
                      (user_id, annonce_id))
        action = 'added'
    
    conn.commit()
    conn.close()
    return action

def get_user_favoris(user_id):
    """Récupère les favoris d'un utilisateur"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT a.*, c.nom as categorie, u.username as vendeur
    FROM favoris f
    JOIN annonces a ON f.annonce_id = a.id
    JOIN categories c ON a.categorie_id = c.id
    JOIN utilisateurs u ON a.utilisateur_id = u.id
    WHERE f.utilisateur_id = ? AND a.statut = 'active'
    ORDER BY f.created_at DESC
    ''', (user_id,))
    
    favoris = [dict(row) for row in cursor.fetchall()]
    
    for f in favoris:
        if not f['image_path']:
            f['image'] = CATEGORY_IMAGES.get(f['categorie'], CATEGORY_IMAGES['Autres'])
        else:
            f['image'] = f['image_path']
    
    conn.close()
    return favoris

def is_favori(user_id, annonce_id):
    """Vérifie si une annonce est dans les favoris"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM favoris WHERE utilisateur_id = ? AND annonce_id = ?', 
                  (user_id, annonce_id))
    result = cursor.fetchone() is not None
    conn.close()
    return result

# ============================================
# FONCTIONS MESSAGERIE
# ============================================

def send_message(expediteur_id, destinataire_id, annonce_id, contenu):
    """Envoie un message"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO messages (expediteur_id, destinataire_id, annonce_id, contenu, created_at)
    VALUES (?, ?, ?, ?, ?)
    ''', (expediteur_id, destinataire_id, annonce_id, contenu, datetime.now()))
    conn.commit()
    conn.close()

def get_user_conversations(user_id):
    """Récupère les conversations d'un utilisateur"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT DISTINCT
        CASE WHEN expediteur_id = ? THEN destinataire_id ELSE expediteur_id END as interlocuteur_id
    FROM messages 
    WHERE expediteur_id = ? OR destinataire_id = ?
    ''', (user_id, user_id, user_id))
    
    conversations = []
    interlocuteurs = cursor.fetchall()
    
    for row in interlocuteurs:
        other_id = row[0]
        cursor.execute('SELECT username FROM utilisateurs WHERE id = ?', (other_id,))
        other_user = cursor.fetchone()
        
        if other_user:
            cursor.execute('''
            SELECT contenu, created_at FROM messages 
            WHERE (expediteur_id = ? AND destinataire_id = ?) 
               OR (expediteur_id = ? AND destinataire_id = ?)
            ORDER BY created_at DESC LIMIT 1
            ''', (user_id, other_id, other_id, user_id))
            
            last_msg = cursor.fetchone()
            conversations.append({
                'interlocuteur_id': other_id,
                'interlocuteur': other_user[0],
                'dernier_message': last_msg[0] if last_msg else '',
                'derniere_date': last_msg[1] if last_msg else ''
            })
    
    conn.close()
    return conversations

def get_messages_between(user_id, interlocuteur_id):
    """Récupère les messages entre deux utilisateurs - CORRIGÉ"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT m.*, u.username as expediteur
    FROM messages m
    JOIN utilisateurs u ON m.expediteur_id = u.id
    WHERE (m.expediteur_id = ? AND m.destinataire_id = ?)
       OR (m.expediteur_id = ? AND m.destinataire_id = ?)
    ORDER BY m.created_at ASC
    ''', (user_id, interlocuteur_id, interlocuteur_id, user_id))
    
    messages = []
    for row in cursor.fetchall():
        msg = dict(row)
        # S'assurer que created_at est présent
        if 'created_at' not in msg or not msg['created_at']:
            msg['created_at'] = datetime.now().isoformat()
        messages.append(msg)
    
    conn.close()
    return messages

# ============================================
# FONCTIONS STATISTIQUES
# ============================================

def get_stats():
    """Récupère les statistiques"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM annonces WHERE statut = "active"')
    annonces = cursor.fetchone()[0] or 0
    
    cursor.execute('SELECT SUM(vues) FROM annonces')
    vues = cursor.fetchone()[0] or 0
    
    cursor.execute('SELECT COUNT(*) FROM utilisateurs')
    users = cursor.fetchone()[0] or 0
    
    cursor.execute('SELECT COUNT(*) FROM messages')
    messages = cursor.fetchone()[0] or 0
    
    conn.close()
    
    return {
        'annonces': annonces,
        'vues': vues,
        'utilisateurs': users,
        'messages': messages
    }

# ============================================
# FONCTIONS SIGNALEMENT
# ============================================

def signaler_annonce(annonce_id, utilisateur_id, raison):
    """Signale une annonce"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO signalements (annonce_id, utilisateur_id, raison, created_at)
    VALUES (?, ?, ?, ?)
    ''', (annonce_id, utilisateur_id, raison, datetime.now()))
    conn.commit()
    conn.close()

# ============================================
# INITIALISATION
# ============================================

# Initialiser la base de données
init_db()