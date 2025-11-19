# secure-app/app.py
import os
import uuid
from flask import Flask, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename 

# ==================== CODE DE SÉCURITÉ (PARTIE 1) ====================
# 1. Définir les extensions de fichiers que nous autorisons
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

# 2. Créer une fonction pour vérifier si l'extension est autorisée
def allowed_file(filename):
    # On vérifie s'il y a un '.' dans le nom du fichier ET
    # ce qui est après le '.' est dans notre liste d'extensions autorisées.
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# ==============================================================================

# ==================== CODE DE SÉCURITÉ (PARTIE DE MAGIC NUMBER) ====================
# 1. Dictionnaire des "Magic Numbers" (signatures de fichiers)
# On va lire les premiers octets d'un fichier pour vérifier son vrai type.
MAGIC_NUMBERS = {
    "jpg": b'\xff\xd8\xff',
    "jpeg": b'\xff\xd8\xff',
    "png": b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a',
    "gif": b'\x47\x49\x46\x38',
    "pdf": b'\x25\x50\x44\x46'
}

# 2. Fonction pour valider le contenu du fichier grâce aux Magic Numbers
def is_file_content_valid(file_stream, extension):
    # On lit les premiers octets du fichier (assez pour l'identifier)
    file_header = file_stream.read(8)
    # TRES IMPORTANT : On remet le curseur au début du fichier pour pouvoir le sauvegarder plus tard
    file_stream.seek(0)
    
    # On vérifie si les premiers octets correspondent à la signature attendue pour cette extension
    if extension in MAGIC_NUMBERS:
        return file_header.startswith(MAGIC_NUMBERS[extension])
    
    # Si l'extension n'est pas dans notre dictionnaire, on refuse par sécurité
    return False
# =======================================================================================

# On change le dossier de destination pour plus de sécurité
UPLOAD_FOLDER = 'safe_uploads' 

app = Flask(__name__)
app.secret_key = 'super-secret-key' 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('Aucun fichier sélectionné')
        return redirect(request.url)
    
    file = request.files['file']

    if file.filename == '':
        flash('Aucun fichier sélectionné')
        return redirect(request.url)
    
    # On nettoie le nom de fichier original
    original_filename = secure_filename(file.filename)

    if file and allowed_file(original_filename):
        # On récupère l'extension pour les vérifications
        extension = original_filename.rsplit('.', 1)[1].lower()
        
        # === VALIDATION NIVEAU 2 : MAGIC NUMBERS ===
        if not is_file_content_valid(file.stream, extension):
            flash('Erreur : Le contenu du fichier ne correspond pas à son extension ! Attaque détectée.')
            return redirect(request.url)
        # ============================================

        # ==================== CODE DE SÉCURITÉ (PARTIE DE RENOMMAGE SECURISE) ====================
        # 3. Renommage sécurisé du fichier
        # On génère un nom de fichier unique et aléatoire pour que l'attaquant ne puisse pas le deviner.
        secure_name = f"{uuid.uuid4()}.{extension}"
        # =======================================================================================

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_name))
        flash(f"Fichier téléversé avec succès et sauvegardé sous le nom sécurisé : {secure_name}")
        return redirect(url_for('index'))
    else:
        flash('Erreur : Extension de fichier non autorisée !')
        return redirect(request.url)

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

