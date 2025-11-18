## 1. Project Overview

This repository contains the source code and documentation for a project centered on the *Unrestricted File Upload* vulnerability, a common and critical web application security flaw.

The project follows the "Build It, Break It, Fix It" methodology:

*   *Build It:* A simple web application developed with Python and Flask that contains an intentionally vulnerable file upload feature.
*   *Break It:* A demonstration of how to exploit this vulnerability by uploading a webshell to achieve Remote Code Execution (RCE) on the server.
*   *Fix It:* A secured version of the same application that implements multiple layers of defense to prevent such attacks.

The goal is to provide a clear, practical example of how this vulnerability works and how developers can effectively secure their applications.

## 2. The Vulnerability: Unrestricted File Upload

An Unrestricted File Upload vulnerability occurs when a web application allows a user to upload files to the server without sufficient validation on their name, type, content, or size. Attackers can leverage this to upload malicious files, such as webshells, which are scripts that allow them to execute arbitrary commands on the server. This can lead to a full system compromise.

## 3. Repository Structure

This repository is organized into two main applications:
.
├── vulnerable-app/ # The "Build It" application with the security flaw
│ ├── app.py # The main Flask application
│ ├── templates/ # HTML templates
│ └── uploads/ # Directory where files are uploaded (insecurely)
│
├── secure-app/ # The "Fix It" application with security controls
│ ├── app.py # The secured Flask application
│ ├── templates/ # HTML templates
│ └── safe_uploads/ # A secure, non-web-accessible directory for uploads
│
├── exploits/ # Contains example webshells for the demonstration
│ └── shell.py # A simple Python webshell
│
└── README.md # This file# secure-file-upload-project
## 4. Technologies Used

*   *Backend:* Python 3
*   *Framework:* Flask
*   *Key Python Libraries:* werkzeug for file handling
*   *Development:* Git & GitHub

## 5. Setup and Installation

To run this project on your local machine, please follow these steps.

*Prerequisites:*
*   Python 3.7+
*   pip (Python package installer)
*   Git

*Instructions:*

1.  *Clone the repository:*
    bash
    git clone https://github.com/[Your-Username]/[Your-Repo-Name].git
    cd [Your-Repo-Name]
    

2.  *Set up a virtual environment (recommended):*
    bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    

3.  *Install dependencies:*
    This project uses Flask. Navigate into the desired application folder and install it.
    bash
    # Example for the vulnerable app
    cd vulnerable-app
    pip install Flask
    

## 6. How to Run the Applications

You can run either the vulnerable or the secure application.

### A. Running the Vulnerable App ("Build It")

1.  Navigate to the vulnerable-app directory:
    bash
    cd vulnerable-app
    

2.  Run the Flask application:
    bash
    flask run
    

3.  Open your web browser and go to http://127.0.0.1:5000.

### B. Running the Secure App ("Fix It")

1.  Navigate to the secure-app directory:
    bash
    cd secure-app
    

2.  Run the Flask application:
    bash
    flask run
    
3.  Open your web browser and go to http://127.0.0.1:5000.

---

## 7. The Exploit ("Break It")

Here is how to exploit the vulnerability in the *vulnerable-app*:

1.  *Start the vulnerable application.*
2.  *Access the application* at http://127.0.0.1:5000.
3.  *Upload the webshell:*
    *   On the form, click "Choose File" and select the shell.py file from the /exploits directory.
    *   Click "Upload". The application will confirm the upload.
4.  *Execute commands:*
    *   The webshell is now on the server. You can access it directly via your browser.
    *   To execute a command (e.g., ls on Linux or dir on Windows), use the cmd parameter in the URL:
    
    # For Linux/macOS
    http://127.0.0.1:5000/uploads/shell.py?cmd=ls

    # For Windows
    http://127.0.0.1:5000/uploads/shell.py?cmd=dir
    
    You will see the output of the command in your browser. You now have Remote Code Execution.

## 8. The Mitigation ("Fix It")

The *secure-app* has been hardened to prevent this attack. The following security controls were implemented:

1.  *File Extension Validation:* Only allows a specific set of safe file extensions (e.g., .png, .jpg, .pdf). All other extensions are rejected.
2.  *Magic Number Validation:* The application reads the first few bytes of the file to verify its actual type, preventing an attacker from simply renaming a .py script to a .png file.
3.  *Secure File Storage:* Uploaded files are saved in a directory (safe_uploads/) that is outside the web root and configured with non-executable permissions.
4.  *Randomized Filenames:* Each uploaded file is given a random, secure filename to prevent attackers from guessing the URL of their uploaded file.

*To verify the fix:*
1.  Run the secure-app.
2.  Attempt to upload the shell.py webshell.
3.  The application will correctly identify it as an invalid file type and reject the upload.

## 9. Ethical Disclaimer

This project and its code are provided for educational purposes only. The techniques demonstrated should only be performed in a controlled and authorized lab environment (like your local machine). Unauthorized scanning or attacking of public web applications is illegal and unethical. The goal is to learn how to defend systems, not to cause harm.
