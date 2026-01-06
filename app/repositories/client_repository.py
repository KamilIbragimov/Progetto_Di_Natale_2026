# Importiamo la nostra funzione per prendere la connessione
from app.db import get_db

# --- FUNZIONI PER AUTENTICAZIONE ---

def create_client(username, password_hash, email=None, phone=None):
    """Inserisce un nuovo cliente (usato per la registrazione).
    Restituisce None se tutto ok, altrimenti una stringa con l'errore.
    """
    db = get_db()
    
    # Verifica se username già esiste
    if db.execute('SELECT id FROM client WHERE username = ?', (username,)).fetchone():
        return 'username'
    
    # Verifica se email già esiste
    if email and db.execute('SELECT id FROM client WHERE email = ?', (email,)).fetchone():
        return 'email'
    
    # Verifica se phone già esiste
    if phone and db.execute('SELECT id FROM client WHERE phone = ?', (phone,)).fetchone():
        return 'phone'
    
    db.execute(
        "INSERT INTO client (username, password, email, phone) VALUES (?, ?, ?, ?)",
        (username, password_hash, email, phone),
    )
    db.commit()
    return None

def get_client_by_username(username):
    """Cerca un cliente per username (usato per login)."""
    db = get_db()
    client = db.execute(
        'SELECT * FROM client WHERE username = ?', (username,)
    ).fetchone()
    return client

def get_client_by_id(client_id):
    """Recupera un singolo cliente per ID."""
    db = get_db()
    client = db.execute(
        'SELECT * FROM client WHERE id = ?', (client_id,)
    ).fetchone()
    return client

# --- FUNZIONI CRUD ---

def get_all_clients():
    """Recupera tutti i clienti, ordinati per username."""
    db = get_db()
    clients = db.execute(
        'SELECT * FROM client ORDER BY username'
    ).fetchall()
    return clients

# --- FUNZIONI PER RELAZIONE N:N ---

def get_projects_for_client(client_id):
    """
    Recupera tutti i progetti finanziati da un cliente.
    Usa JOIN sulla tabella ponte project_client.
    """
    db = get_db()
    query = """
        SELECT p.*
        FROM project p
        JOIN project_client pc ON p.id = pc.project_id
        WHERE pc.client_id = ?
        ORDER BY p.name
    """
    return db.execute(query, (client_id,)).fetchall()
