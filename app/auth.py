from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
# werkzeug.security ci offre strumenti professionali per la crittografia
from werkzeug.security import check_password_hash, generate_password_hash
from app.repositories import client_repository

# url_prefix='/auth' significa che tutte le route qui inizieranno con /auth
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    """
    Questa funzione viene eseguita AUTOMATICAMENTE prima di ogni richiesta.
    Serve a caricare l'utente dal DB e renderlo disponibile in tutto il sito.
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        # Carichiamo l'utente e lo mettiamo in g.user
        # Ora g.user sarà disponibile anche nei template HTML!
        g.user = client_repository.get_client_by_id(user_id)

@bp.route('/register', methods=('GET', 'POST'))
def register():
    # CASO 2: POST (L'utente ha inviato i dati)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']
        error = None

        if not username:
            error = 'Username obbligatorio.'
        elif not password:
            error = 'Password obbligatoria.'
        elif not email:
            error = 'Email obbligatoria.'
        elif not phone:
            error = 'Telefono obbligatorio.'
        elif not phone.isdigit():
            error = 'Inserisci solo numeri per il telefono.'
        elif len(phone) < 6:
            error = 'Il numero di telefono deve avere almeno 6 cifre.'
        elif len(phone) > 15:
            error = 'Il numero di telefono non può superare 15 cifre.'

        if error is None:
            # Hashiamo la password (MAI salvarla in chiaro!)
            hashed_pwd = generate_password_hash(password)
            
            # Chiamiamo il Repository
            result = client_repository.create_client(username, hashed_pwd, email, phone)
            
            if result is None:
                return redirect(url_for('auth.login'))
            elif result == 'username':
                error = f"L'utente {username} è già registrato."
            elif result == 'email':
                error = "Email già usata."
            elif result == 'phone':
                error = "Numero di telefono già usato."

        flash(error)

    # CASO 1: GET (Mostriamo il form)
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        
        # 1. Cerchiamo l'utente nel DB
        user = client_repository.get_client_by_username(username)

        if user is None:
            error = 'Username non corretto.'
        # 2. Verifichiamo la password
        elif not check_password_hash(user['password'], password):
            error = 'Password non corretta.'

        if error is None:
            # 3. GESTIONE SESSIONE (Mettiamo il "braccialetto")
            # Puliamo eventuali vecchie sessioni
            session.clear()
            # Salviamo l'ID dell'utente nel cookie di sessione
            session['user_id'] = user['id']
            
            # Ora il browser ricorderà chi siamo!
            return redirect(url_for('main.index'))

        flash(error)

    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    # Per uscire, "tagliamo il braccialetto"
    session.clear()
    return redirect(url_for('main.index'))
