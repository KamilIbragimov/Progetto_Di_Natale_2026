import sqlite3
import os

# Cambia directory alla cartella di questo file
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Definiamo dove creare il file del database (nella cartella instance)
if not os.path.exists('instance'):
    os.makedirs('instance')

db_path = os.path.join('instance', 'majima.sqlite')

# Elimina il database esistente se presente
if os.path.exists(db_path):
    try:
        os.remove(db_path)
        print("database esistente eliminato.")
    except PermissionError:
        print("Impossibile eliminare il database (file in uso).")
        print("Chiudi il server Flask e riprova, oppure elimina manualmente il file:")
        print(f"  {os.path.abspath(db_path)}")
        exit(1)

# Ci connettiamo (se il file non esiste, lo crea)
connection = sqlite3.connect(db_path)

# Leggiamo lo schema SQL (solo CREATE TABLE)
with open('app/schema.sql') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()

print("✅ Database creato con successo!")
print("   Ora puoi avviare il server con: python run.py")
