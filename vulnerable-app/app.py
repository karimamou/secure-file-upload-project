# vulnerable-app/app.py (VERSION CORRIGÉE ET SUPER VULNÉRABLE)
import subprocess
import os
from flask import Flask, request, render_template, send_from_directory

# --- Configuration ---
UPLOAD_FOLDER = 'uploads' 

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "Error: No file part in the request."
    
    file = request.files['file']

    if file.filename == '':
        return "Error: No file was selected."
    
    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return f"Success! The file '{filename}' has been uploaded."

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # === ATTENTION : FAILLE DE SÉCURITÉ MAJEURE ===
    if filename.endswith('.py'):
        try:
            command_to_run = request.args.get('cmd')
            
            if command_to_run:
                # La ligne suivante exécute la commande et capture le résultat.
                result = subprocess.check_output(command_to_run, shell=True, text=True, cwd=app.config['UPLOAD_FOLDER'])
                
                # On renvoie le résultat de la commande au navigateur.
                return f"<pre>{result}</pre>"
            else:
                return "Script Python trouvé, mais aucune commande 'cmd' n'a été fournie."

        except Exception as e:
            return f"Une erreur est survenue lors de l'exécution du script : {e}"
    else:
        # Pour tous les autres fichiers, on les sert normalement.
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)