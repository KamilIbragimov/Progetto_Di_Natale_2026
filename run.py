# Avvia il server Flask per Majima Construction
import os

# Cambia la directory di lavoro alla cartella di questo file
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from app import create_app

# Creiamo l'applicazione Flask
app = create_app()

if __name__ == '__main__':
    # Prima di avviare, verifica se il database esiste
    if not os.path.exists('instance/majima.sqlite'):
        print("⚠️  Database non trovato! Esegui prima: python setup_db.py")
    else:
        print("🚀 Avvio server...")
    app.run(debug=True)
