# secure-app/app.py
import os
import uuid
from flask import Flask, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename 

# --- Fonctions de sécurité (inchangées) ---
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

MAGIC_NUMBERS = {
    "jpg": b'\xff\xd8\xff',
    "jpeg": b'\xff\xd8\xff',
    "png": b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a',
    "gif": b'\x47\x49\x46\x38',
    "pdf": b'\x25\x50\x44\x46'
}

def is_file_content_valid(file_stream, extension):
    file_header = file_stream.read(8)
    file_stream.seek(0)
    if extension in MAGIC_NUMBERS:
        return file_header.startswith(MAGIC_NUMBERS[extension])
    return False
# ---------------------------------------------

UPLOAD_FOLDER = 'safe_uploads' 
app = Flask(__name__)
app.secret_key = 'super-secret-key' 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ==========================================================
# ▼▼▼ LA CORRECTION PRINCIPALE EST DANS CETTE SECTION ▼▼▼
# ==========================================================
# On fusionne les deux routes en une seule fonction qui gère GET et POST
@app.route('/', methods=['GET', 'POST'])
def index():
    # Si la méthode est POST, c'est que l'utilisateur a envoyé le formulaire
    if request.method == 'POST':
        if 'file' not in request.files:
            # On ajoute la catégorie 'error' pour les messages d'erreur
            flash('Erreur : Aucun fichier sélectionné', 'error')
            return redirect(url_for('index'))
        
        file = request.files['file']

        if file.filename == '':
            flash('Erreur : Aucun fichier sélectionné', 'error')
            return redirect(url_for('index'))
        
        original_filename = secure_filename(file.filename)

        if file and allowed_file(original_filename):
            extension = original_filename.rsplit('.', 1)[1].lower()
            
            if not is_file_content_valid(file.stream, extension):
                flash('Erreur : Le contenu du fichier ne correspond pas à son extension ! Attaque détectée.', 'error')
                return redirect(url_for('index'))
            
            secure_name = f"{uuid.uuid4()}.{extension}"
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_name))
            
            # On crée un message de succès formaté en HTML
            success_message = f"{secure_name} téléchargé avec succès !"
            # On envoie le message avec la catégorie 'success' pour le popup
            flash(success_message, 'success')

            return redirect(url_for('index'))
        else:
            flash('Erreur : Extension de fichier non autorisée !', 'error')
            return redirect(url_for('index'))
            
    # Si la méthode est GET, on affiche simplement la page normalement
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
  # ======== L'anicenne version de code (sécurité)=====================================================

#UPLOAD_FOLDER = 'uploads' # On peut garder le même nom pour l'instant

#app = Flask(__name__)
# Une clé secrète est nécessaire pour afficher des messages d'erreur (flash messages)
# app.secret_key = 'super-secret-key' 
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# @app.route('/')
# def index():
#     return render_template('index.html') # On utilisera un nouveau template

# @app.route('/', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         flash('Aucun fichier sélectionné')
#         return redirect(request.url)
    
#     file = request.files['file']

#     if file.filename == '':
#         flash('Aucun fichier sélectionné')
#         return redirect(request.url)
    
#     # === LA SÉCURITÉ COMMENCE ICI ! ===
#     # On utilise la fonction 'secure_filename' pour nettoyer le nom du fichier
#     filename = secure_filename(file.filename)

#     # On vérifie si le fichier et son extension sont valides
#     if file and allowed_file(filename):
        
#         # ==================== CODE DE SÉCURITÉ (PARTIE 2) ====================
#         # 3. Vérification du type MIME
#         # Cela ajoute une couche de sécurité, mais attention, elle peut être contournée !
#         allowed_mimetypes = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf']
#         if file.content_type not in allowed_mimetypes:
#             flash(f"Erreur : Type de fichier non valide (MIME type '{file.content_type}' incorrect).")
#             return redirect(request.url)
#         # ==============================================================================

#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         flash(f"Fichier '{filename}' téléversé avec succès !")
#         return redirect(url_for('index'))
#     else:
#         # Si l'extension n'est pas autorisée, on affiche une erreur
#         flash('Erreur : Extension de fichier non autorisée !')
#         return redirect(request.url)

# if __name__ == '__main__':
#     app.run(debug=True)

