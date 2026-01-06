from flask import Blueprint, render_template
from werkzeug.exceptions import abort
from app.repositories import client_repository

bp = Blueprint('clients', __name__, url_prefix='/clients')

@bp.route('/')
def index():
    """Mostra tutti i clienti (solo visualizzazione)."""
    clients = client_repository.get_all_clients()
    return render_template('clients/list.html', clients=clients)

@bp.route('/<int:id>')
def detail(id):
    """Mostra i dettagli di un cliente e i suoi progetti."""
    client = client_repository.get_client_by_id(id)
    if client is None:
        abort(404, f"Cliente {id} non trovato.")
    
    projects = client_repository.get_projects_for_client(id)
    return render_template('clients/detail.html', client=client, projects=projects)
