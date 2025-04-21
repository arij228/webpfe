from flask import Flask, render_template, request, redirect, url_for, session, flash
import random
import string
import os
import pyodbc
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = secrets.token_hex(24)

# Configuration de la connexion ODBC
server = 'localhost'  # ou 'Arij' si c'est le nom de votre serveur
database = 'users'

# Fonction pour obtenir une connexion à la base de données
def get_db_connection():
    try:
        conn = pyodbc.connect(
            "DRIVER={SQL Server};"
            f"SERVER={server};"
            f"DATABASE={database};"
            "Trusted_Connection=yes;"
        )
        print("Connexion à la base de données établie avec succès!")
        return conn
    except Exception as e:
        print(f"Erreur de connexion à la base de données: {e}")
        return None

# Fonction pour initialiser la base de données
def init_db():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        
        # Vérifier si la table des utilisateurs existe déjà
        try:
            cursor.execute("""
                SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_NAME = 'Users' AND TABLE_SCHEMA = 'dbo'
            """)
            
            table_exists = cursor.fetchone()[0] > 0
            
            if not table_exists:
                # Créer la table Users avec uniquement les 5 champs requis
                cursor.execute("""
                    CREATE TABLE dbo.Users (
                        id INT IDENTITY(1,1) PRIMARY KEY,
                        email NVARCHAR(100) NOT NULL UNIQUE,
                        password NVARCHAR(255) NOT NULL,
                        otp NVARCHAR(6) NULL,
                        otp_expiry DATETIME NULL
                    )
                """)
                print("Table Users créée avec succès!")
            
            conn.commit()
        except Exception as e:
            print(f"Erreur lors de l'initialisation de la base de données: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

# Alternative à before_first_request pour Flask 2+
# Utilisation d'un point d'entrée avec contexte d'application
@app.route('/')
def index():
    # Initialiser la BD lors de la première requête
    if getattr(app, '_db_init_done', False) is False:
        with app.app_context():
            init_db()
            app._db_init_done = True
    
    # Affiche la page de login/signup par défaut
    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Vérification basique
        if not all([email, password]):
            return render_template('login.html', signup_message="Tous les champs sont obligatoires")
        
        conn = get_db_connection()
        if not conn:
            return render_template('login.html', signup_message="Erreur de connexion à la base de données")
        
        cursor = conn.cursor()
        
        # Vérifier si l'email existe déjà
        try:
            cursor.execute("SELECT COUNT(*) FROM dbo.Users WHERE email = ?", (email,))
            if cursor.fetchone()[0] > 0:
                cursor.close()
                conn.close()
                return render_template('login.html', signup_message="Cet email est déjà utilisé")
        except Exception as e:
            print(f"Erreur lors de la vérification de l'email: {e}")
            cursor.close()
            conn.close()
            return render_template('login.html', signup_message="Erreur lors de la vérification de l'email")
        
        if len(password) < 6:
            cursor.close()
            conn.close()
            return render_template('login.html', signup_message="Le mot de passe doit contenir au moins 6 caractères")
        
        # Hacher le mot de passe
        hashed_password = generate_password_hash(password)
        
        # Générer un code OTP à 6 chiffres
        otp = ''.join(random.choices(string.digits, k=6))
        # Définir la date d'expiration de l'OTP (15 minutes)
        otp_expiry = datetime.now() + timedelta(days=1)
        
        try:
            # Stocker l'utilisateur avec l'OTP directement dans la table Users
            cursor.execute("""
                INSERT INTO dbo.Users (email, password, otp, otp_expiry) 
                VALUES (?, ?, ?, ?)
            """, (email, hashed_password, otp, otp_expiry))
            
            conn.commit()
        except Exception as e:
            print(f"Erreur lors de l'insertion de l'utilisateur avec OTP: {e}")
            conn.rollback()
            cursor.close()
            conn.close()
            return render_template('login.html', signup_message="Erreur lors de l'enregistrement, veuillez réessayer")
        
        cursor.close()
        conn.close()
        
        print(f"Code OTP pour {email}: {otp}")  # Dans une vraie application, envoyez par email
        
        # Rediriger vers la page avec section OTP visible
        return render_template('login.html', 
                              show_otp=True, 
                              email_for_otp=email,
                              signup_message=f"Code OTP envoyé à {email}")
    
    return redirect(url_for('index'))

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    if request.method == 'POST':
        entered_otp = request.form.get('otp')
        email = request.form.get('email')
        
        conn = get_db_connection()
        if not conn:
            return render_template('login.html', otp_message="Erreur de connexion à la base de données")
        
        cursor = conn.cursor()
        
        # Récupérer les données de l'OTP
        try:
            cursor.execute("""
                SELECT otp, otp_expiry FROM dbo.Users WHERE email = ?
            """, (email,))
            
            otp_data = cursor.fetchone()
            
            if not otp_data:
                cursor.close()
                conn.close()
                return render_template('login.html', otp_message="Email non trouvé, veuillez réessayer")
            
            stored_otp, expiry_time = otp_data
            
            # Vérifier si l'OTP est expiré
            if datetime.now() > expiry_time:
                cursor.close()
                conn.close()
                return render_template('login.html', otp_message="Code OTP expiré, veuillez vous réinscrire")
            
            if entered_otp == stored_otp:  # Vérifie l'OTP
                # OTP valide - Valider l'inscription
                try:
                    # Mettre à jour le statut de l'utilisateur (effacer l'OTP)
                    cursor.execute("""
                        UPDATE dbo.Users 
                        SET otp = NULL, otp_expiry = NULL 
                        WHERE email = ?
                    """, (email,))
                    
                    conn.commit()
                except Exception as e:
                    print(f"Erreur lors de la validation de l'utilisateur: {e}")
                    conn.rollback()
                    cursor.close()
                    conn.close()
                    return render_template('login.html', otp_message="Erreur lors de la validation, veuillez réessayer")
                
                cursor.close()
                conn.close()
                
                # Rediriger vers la page de connexion avec un message
                return render_template('login.html', 
                                    just_registered=True,  # Pour basculer vers l'onglet login
                                    login_message="Inscription réussie! Vous pouvez maintenant vous connecter.")
            else:
                # Code OTP incorrect
                cursor.close()
                conn.close()
                return render_template('login.html', 
                                    show_otp=True, 
                                    email_for_otp=email,
                                    otp_message="Code OTP incorrect")
        except Exception as e:
            print(f"Erreur lors de la vérification de l'OTP: {e}")
            cursor.close()
            conn.close()
            return render_template('login.html', otp_message="Erreur lors de la vérification, veuillez réessayer")
    
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        conn = get_db_connection()
        if not conn:
            return render_template('login.html', login_message="Erreur de connexion à la base de données")
        
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT email, password FROM dbo.Users WHERE email = ? AND otp IS NULL
            """, (email,))
            
            user = cursor.fetchone()
            
            if user and check_password_hash(user[1], password):
                # Connexion réussie
                session['user_email'] = email
                cursor.close()
                conn.close()
                return redirect(url_for('dashboard'))
            else:
                # Échec de connexion
                cursor.close()
                conn.close()
                return render_template('login.html', login_message="Email ou mot de passe incorrect")
        except Exception as e:
            print(f"Erreur lors de la connexion: {e}")
            cursor.close()
            conn.close()
            return render_template('login.html', login_message="Erreur lors de la connexion, veuillez réessayer")
    
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    # Vérifier si l'utilisateur est connecté
    if 'user_email' not in session:
        return redirect(url_for('index'))
    
    # Use email as identifier since we don't have username in our database
    email = session.get('user_email', 'Utilisateur')
    return render_template('dashboard.html', username=email)
@app.route('/user.html')
def user():
    # Vérifier si l'utilisateur est connecté
    if 'user_email' not in session:
        return redirect(url_for('index'))
    
    # Récupérer l'email de l'utilisateur connecté
    email = session.get('user_email')
    
    # Se connecter à la base de données
    conn = get_db_connection()
    if not conn:
        flash("Erreur de connexion à la base de données", "error")
        return redirect(url_for('dashboard'))
    
    cursor = conn.cursor()
    
    try:
        # Récupérer les informations de l'utilisateur
        cursor.execute("SELECT email FROM dbo.Users WHERE email = ?", (email,))
        user_info = cursor.fetchone()
        
        if not user_info:
            cursor.close()
            conn.close()
            flash("Utilisateur non trouvé", "error")
            return redirect(url_for('dashboard'))
        
        # Créer un dictionnaire avec les informations disponibles
        user_data = {
            'email': user_info[0],
            # Pour l'instant, on n'a que l'email dans la base de données
            # Les autres champs seront soit vides, soit remplis avec des valeurs par défaut
            'username': email.split('@')[0],  # On utilise la partie locale de l'email comme username par défaut
            'first_name': '',
            'last_name': '',
            'address': '',
            'city': '',
            'country': '',
            'postal_code': ''
        }
        
    except Exception as e:
        print(f"Erreur lors de la récupération des informations utilisateur: {e}")
        cursor.close()
        conn.close()
        flash("Erreur lors de la récupération des informations utilisateur", "error")
        return redirect(url_for('dashboard'))
    
    cursor.close()
    conn.close()
    
    # Passer les informations au template
    return render_template('user.html', user=user_data)
@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user_email' not in session:
        return redirect(url_for('index'))
    
    # Récupérer les données du formulaire
    username = request.form.get('username')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    address = request.form.get('address')
    city = request.form.get('city')
    country = request.form.get('country')
    postal_code = request.form.get('postal_code')
    
    # Mettre à jour la base de données
    # (Vous devrez d'abord modifier votre schéma pour ajouter ces colonnes)
    
    flash('Profil mis à jour avec succès', 'success')
    return redirect(url_for('user'))
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Vous pouvez aussi initialiser la BD ici
    # with app.app_context():
    #     init_db()
    app.run(debug=True)