from flask import Blueprint, render_template
from app.repositories import project_repository

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Homepage con panoramica dei progetti."""
    projects = project_repository.get_all_projects()
    return render_template('index.html', projects=projects)

@bp.route('/about')
def about():
    """Pagina informativa."""
    return render_template('about.html')
