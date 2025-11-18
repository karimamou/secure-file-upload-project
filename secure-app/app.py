
# secure-app/app.py
import os
from flask import Flask, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename # On importe une fonction de sécurité utile

# ==================== NOUVEAU CODE DE SÉCURITÉ (PARTIE 1) ====================
# 1. Définir les extensions de fichiers que nous autorisons
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

# 2. Créer une fonction pour vérifier si l'extension est autorisée
def allowed_file(filename):
    # On vérifie s'il y a un '.' dans le nom du fichier ET
    # ce qui est après le '.' est dans notre liste d'extensions autorisées.
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# ==============================================================================

UPLOAD_FOLDER = 'uploads' # On peut garder le même nom pour l'instant

app = Flask(__name__)
# Une clé secrète est nécessaire pour afficher des messages d'erreur (flash messages)
app.secret_key = 'super-secret-key' 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html') # On utilisera un nouveau template

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('Aucun fichier sélectionné')
        return redirect(request.url)
    
    file = request.files['file']

    if file.filename == '':
        flash('Aucun fichier sélectionné')
        return redirect(request.url)
    
    # === LA SÉCURITÉ COMMENCE ICI ! ===
    # On utilise la fonction 'secure_filename' pour nettoyer le nom du fichier
    filename = secure_filename(file.filename)

    # On vérifie si le fichier et son extension sont valides
    if file and allowed_file(filename):
        
        # ==================== NOUVEAU CODE DE SÉCURITÉ (PARTIE 2) ====================
        # 3. Vérification du type MIME
        # Cela ajoute une couche de sécurité, mais attention, elle peut être contournée !
        allowed_mimetypes = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf']
        if file.content_type not in allowed_mimetypes:
            flash(f"Erreur : Type de fichier non valide (MIME type '{file.content_type}' incorrect).")
            return redirect(request.url)
        # ==============================================================================

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash(f"Fichier '{filename}' téléversé avec succès !")
        return redirect(url_for('index'))
    else:
        # Si l'extension n'est pas autorisée, on affiche une erreur
        flash('Erreur : Extension de fichier non autorisée !')
        return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)