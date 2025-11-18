import os
from flask import Flask, request, render_template, send_from_directory

# --- Configuration ---
# This tells Flask where to save the uploaded files.
UPLOAD_FOLDER = 'uploads' 

# Create the Flask application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the 'uploads' directory if it doesn't exist
# This prevents an error on the first run.
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# --- Routes ---

# This is the main route for the homepage.
# It just displays your 'index.html' file.
@app.route('/')
def index():
    return render_template('index.html')

# This route handles the file upload.
# It only accepts POST requests, which is what the form sends.
@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if a file was actually sent in the request
    if 'file' not in request.files:
        return "Error: No file part in the request."
    
    file = request.files['file']

    # If the user submits the form without selecting a file,
    # the browser might send a file with an empty name.
    if file.filename == '':
        return "Error: No file was selected."
    
    if file:
        # === THE SECURITY VULNERABILITY IS RIGHT HERE ===
        # The code takes the file and saves it using its original name.
        # There are NO CHECKS on the file type, extension, or content.
        # An attacker can upload ANY file, including a malicious script.
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Give the user a success message
        return f"Success! The file '{filename}' has been uploaded."

# This route is needed so the 'hacker' can access the uploaded webshell.
# It allows anyone to view a file from the 'uploads' directory.
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# This is the standard way to run the Flask development server.
if __name__ == '__main__':
    # debug=True means the server will auto-reload when you save the file.
    app.run(debug=True)