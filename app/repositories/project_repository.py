# Importiamo la nostra funzione per prendere la connessione
from app.db import get_db

# --- FUNZIONI CRUD BASE ---

def get_all_projects():
    """
    Recupera tutti i progetti con il nome del creatore.
    Esegue una JOIN con la tabella client per ottenere anche il nome dell'autore.
    """
    db = get_db()
    query = """
        SELECT p.*, c.username as creator_name
        FROM project p
        JOIN client c ON p.created_by = c.id
        ORDER BY p.created DESC
    """
    return db.execute(query).fetchall()

def get_project_by_id(project_id):
    """
    Recupera un singolo progetto per ID (con JOIN per il creatore).
    """
    db = get_db()
    query = """
        SELECT p.*, c.username as creator_name
        FROM project p
        JOIN client c ON p.created_by = c.id
        WHERE p.id = ?
    """
    return db.execute(query, (project_id,)).fetchone()

def create_project(name, description, budget, created_by):
    """
    Crea un nuovo progetto.
    Lo stato è sempre 'pianificazione' alla creazione.
    """
    db = get_db()
    db.execute(
        'INSERT INTO project (name, description, budget, status, created_by) VALUES (?, ?, ?, ?, ?)',
        (name, description, budget, 'pianificazione', created_by)
    )
    db.commit()

def update_project(project_id, name, description, budget, status):
    """Aggiorna un progetto esistente."""
    db = get_db()
    db.execute(
        '''UPDATE project 
           SET name = ?, description = ?, budget = ?, status = ? 
           WHERE id = ?''',
        (name, description, budget, status, project_id)
    )
    db.commit()

def delete_project(project_id):
    """Elimina un progetto."""
    db = get_db()
    db.execute('DELETE FROM project WHERE id = ?', (project_id,))
    db.commit()

# --- FUNZIONI PER GESTIRE LA RELAZIONE N:N (Finanziatori) ---

def get_clients_for_project(project_id):
    """
    Recupera tutti i clienti che finanziano un progetto.
    Query con JOIN sulla tabella ponte project_client.
    """
    db = get_db()
    query = """
        SELECT c.*
        FROM client c
        JOIN project_client pc ON c.id = pc.client_id
        WHERE pc.project_id = ?
        ORDER BY c.username
    """
    return db.execute(query, (project_id,)).fetchall()

def get_available_clients_for_project(project_id):
    """
    Recupera i clienti che NON sono ancora associati al progetto.
    Esclude anche il creatore del progetto (è già coinvolto).
    Utile per il form "Aggiungi finanziatore".
    """
    db = get_db()
    query = """
        SELECT c.*
        FROM client c
        WHERE c.id NOT IN (
            SELECT client_id FROM project_client WHERE project_id = ?
        )
        AND c.id != (SELECT created_by FROM project WHERE id = ?)
        ORDER BY c.username
    """
    return db.execute(query, (project_id, project_id)).fetchall()

def add_client_to_project(project_id, client_id):
    """
    Associa un cliente a un progetto (aggiunge un finanziatore).
    Restituisce True se successo, False se già associato.
    """
    db = get_db()
    try:
        db.execute(
            'INSERT INTO project_client (project_id, client_id) VALUES (?, ?)',
            (project_id, client_id)
        )
        db.commit()
        return True
    except db.IntegrityError:
        return False

def remove_client_from_project(project_id, client_id):
    """Rimuove un finanziatore dal progetto."""
    db = get_db()
    db.execute(
        'DELETE FROM project_client WHERE project_id = ? AND client_id = ?',
        (project_id, client_id)
    )
    db.commit()
