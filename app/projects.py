from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from app.repositories import project_repository, client_repository

bp = Blueprint('projects', __name__, url_prefix='/projects')

PROJECT_STATUSES = ['pianificazione', 'in_corso', 'completato', 'sospeso']

@bp.route('/')
def index():
    """Mostra tutti i progetti."""
    projects = project_repository.get_all_projects()
    return render_template('projects/list.html', projects=projects)

@bp.route('/<int:id>')
def detail(id):
    """Mostra i dettagli di un progetto e i suoi finanziatori."""
    project = project_repository.get_project_by_id(id)
    if project is None:
        abort(404, f"Progetto {id} non trovato.")
    
    clients = project_repository.get_clients_for_project(id)
    available_clients = project_repository.get_available_clients_for_project(id)
    
    return render_template('projects/detail.html', 
                          project=project, 
                          clients=clients,
                          available_clients=available_clients)

@bp.route('/create', methods=('GET', 'POST'))
def create():
    """Crea un nuovo progetto."""
    if g.user is None:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        budget = request.form.get('budget', 0)
        error = None
        
        if not name:
            error = 'Il nome del progetto è obbligatorio.'
        
        try:
            budget = float(budget) if budget else 0
        except ValueError:
            error = 'Il budget deve essere un numero.'
        
        if error is not None:
            flash(error)
        else:
            project_repository.create_project(name, description, budget, g.user['id'])
            return redirect(url_for('projects.index'))
    
    return render_template('projects/create.html')

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    """Modifica un progetto esistente."""
    if g.user is None:
        return redirect(url_for('auth.login'))
    
    project = project_repository.get_project_by_id(id)
    if project is None:
        abort(404, f"Progetto {id} non trovato.")
    
    # Controllo autorizzazione: solo il creatore può modificare
    if project['created_by'] != g.user['id']:
        abort(403)
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        budget = request.form.get('budget', 0)
        status = request.form.get('status', 'pianificazione')
        error = None
        
        if not name:
            error = 'Il nome del progetto è obbligatorio.'
        
        try:
            budget = float(budget) if budget else 0
        except ValueError:
            error = 'Il budget deve essere un numero.'
        
        if error is not None:
            flash(error)
        else:
            project_repository.update_project(id, name, description, budget, status)
            return redirect(url_for('projects.detail', id=id))
    
    return render_template('projects/update.html', 
                          project=project, 
                          statuses=PROJECT_STATUSES)

@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    """Elimina un progetto."""
    if g.user is None:
        return redirect(url_for('auth.login'))
    
    project = project_repository.get_project_by_id(id)
    if project is None:
        abort(404, f"Progetto {id} non trovato.")
    
    if project['created_by'] != g.user['id']:
        abort(403)
    
    project_repository.delete_project(id)
    return redirect(url_for('projects.index'))

@bp.route('/<int:id>/add_client', methods=('POST',))
def add_client(id):
    """Aggiunge un finanziatore al progetto."""
    if g.user is None:
        return redirect(url_for('auth.login'))
    
    project = project_repository.get_project_by_id(id)
    if project is None:
        abort(404, f"Progetto {id} non trovato.")
    
    if project['created_by'] != g.user['id']:
        abort(403)
    
    client_id = request.form.get('client_id')
    if client_id:
        project_repository.add_client_to_project(id, int(client_id))
    
    return redirect(url_for('projects.detail', id=id))

@bp.route('/<int:id>/remove_client/<int:client_id>', methods=('POST',))
def remove_client(id, client_id):
    """Rimuove un finanziatore dal progetto."""
    if g.user is None:
        return redirect(url_for('auth.login'))
    
    project = project_repository.get_project_by_id(id)
    if project is None:
        abort(404, f"Progetto {id} non trovato.")
    
    if project['created_by'] != g.user['id']:
        abort(403)
    
    project_repository.remove_client_from_project(id, client_id)
    return redirect(url_for('projects.detail', id=id))
