# 🏗️ Majima Construction

## Cos'è questo progetto?

**Majima Construction** è un'applicazione web per la gestione di un'impresa edile, sviluppata con il framework **Flask** (Python) seguendo il pattern **Repository**.

Il sistema permette di:
- **Registrare utenti** che diventano automaticamente clienti
- **Gestire progetti edilizi** con nome, descrizione, budget e stato
- **Associare clienti ai progetti** come finanziatori (relazione molti-a-molti)
- **Autenticarsi** con sistema di login/logout sicuro (password hashate)

---

## 🗂️ Struttura dei File

```
majima_construction/
│
├── run.py                  # Script per avviare il server
├── setup_db.py             # Script per creare/ricreare il database
├── Introduzione.md         # Questo file di documentazione
│
├── app/                    # Pacchetto principale dell'applicazione
│   ├── __init__.py         # Factory dell'applicazione Flask
│   ├── db.py               # Gestione connessione al database
│   ├── schema.sql          # Schema SQL delle tabelle
│   │
│   ├── auth.py             # Blueprint per autenticazione
│   ├── main.py             # Blueprint per homepage
│   ├── clients.py          # Blueprint per gestione clienti
│   ├── projects.py         # Blueprint per gestione progetti
│   │
│   ├── repositories/       # Pattern Repository (accesso ai dati)
│   │   ├── __init__.py
│   │   ├── client_repository.py
│   │   └── project_repository.py
│   │
│   ├── static/             # File statici
│   │   └── images/
│   │       └── majima_crew.png
│   │
│   └── templates/          # Template HTML (Jinja2)
│       ├── base.html
│       ├── index.html
│       ├── about.html
│       ├── auth/
│       │   ├── login.html
│       │   └── register.html
│       ├── clients/
│       │   ├── list.html
│       │   └── detail.html
│       └── projects/
│           ├── list.html
│           ├── detail.html
│           ├── create.html
│           └── update.html
│
└── instance/               # Cartella generata automaticamente
    └── majima.sqlite       # Database SQLite
```

---

## 📄 Descrizione di ogni File

### File Principali

| File | Descrizione |
|------|-------------|
| `run.py` | Script di avvio del server Flask. Verifica se il database esiste e avvia l'applicazione in modalità debug. |
| `setup_db.py` | Script per inizializzare il database. Elimina il database esistente e lo ricrea con i dati di esempio. |

### Pacchetto `app/`

| File | Descrizione |
|------|-------------|
| `__init__.py` | **Factory dell'applicazione**. Crea e configura l'istanza Flask, registra i blueprint e inizializza il database. |
| `db.py` | **Gestione database**. Contiene `get_db()` per ottenere la connessione e `close_db()` per chiuderla automaticamente. |
| `schema.sql` | **Schema SQL**. Definisce le tabelle `client`, `project` e `project_client` (tabella ponte N:N). Include dati di esempio. |
| `auth.py` | **Blueprint autenticazione**. Gestisce registrazione, login e logout. Carica l'utente in `g.user` prima di ogni richiesta. |
| `main.py` | **Blueprint principale**. Route per homepage (`/`) e pagina about (`/about`). |
| `clients.py` | **Blueprint clienti**. Lista clienti (`/clients`) e dettaglio singolo cliente (`/clients/<id>`). |
| `projects.py` | **Blueprint progetti**. CRUD completo: lista, dettaglio, creazione, modifica, eliminazione. Gestisce anche l'aggiunta/rimozione di finanziatori. |

### Cartella `repositories/`

| File | Descrizione |
|------|-------------|
| `client_repository.py` | Funzioni per accesso ai dati dei clienti: `create_client()`, `get_client_by_username()`, `get_client_by_id()`, `get_all_clients()`, `get_projects_for_client()`. |
| `project_repository.py` | Funzioni per accesso ai dati dei progetti: `get_all_projects()`, `get_project_by_id()`, `create_project()`, `update_project()`, `delete_project()`, `get_clients_for_project()`, `add_client_to_project()`, `remove_client_from_project()`. |

### Cartella `templates/`

| File | Descrizione |
|------|-------------|
| `base.html` | Template base con navbar, stili CSS e struttura comune a tutte le pagine. |
| `index.html` | Homepage con immagine, benvenuto e lista progetti. |
| `about.html` | Pagina informativa "Chi Siamo". |
| `auth/login.html` | Form di login (username e password). |
| `auth/register.html` | Form di registrazione (username, password, email, telefono). |
| `clients/list.html` | Elenco di tutti i clienti registrati. |
| `clients/detail.html` | Dettaglio cliente con i progetti che finanzia. |
| `projects/list.html` | Elenco di tutti i progetti. |
| `projects/detail.html` | Dettaglio progetto con finanziatori e form per aggiungerne. |
| `projects/create.html` | Form per creare un nuovo progetto. |
| `projects/update.html` | Form per modificare un progetto esistente. |

---

## 🗄️ Schema Database

### Tabella `client`
| Campo | Tipo | Vincoli | Descrizione |
|-------|------|---------|-------------|
| id | INTEGER | PRIMARY KEY | Identificativo univoco |
| username | TEXT | UNIQUE, NOT NULL | Nome utente |
| password | TEXT | NOT NULL | Password hashata (scrypt) |
| email | TEXT | UNIQUE | Email del cliente |
| phone | TEXT | UNIQUE | Numero di telefono |
| created | TIMESTAMP | DEFAULT NOW | Data registrazione |

### Tabella `project`
| Campo | Tipo | Vincoli | Descrizione |
|-------|------|---------|-------------|
| id | INTEGER | PRIMARY KEY | Identificativo univoco |
| name | TEXT | UNIQUE, NOT NULL | Nome del progetto |
| description | TEXT | - | Descrizione |
| budget | REAL | DEFAULT 0 | Budget in euro |
| status | TEXT | DEFAULT 'pianificazione' | Stato (pianificazione, in_corso, completato, sospeso) |
| created_by | INTEGER | FK → client.id | ID del creatore |
| created | TIMESTAMP | DEFAULT NOW | Data creazione |

### Tabella `project_client` (Relazione N:N)
| Campo | Tipo | Vincoli | Descrizione |
|-------|------|---------|-------------|
| project_id | INTEGER | FK → project.id | ID progetto |
| client_id | INTEGER | FK → client.id | ID cliente finanziatore |

---

## 🚀 Istruzioni per Avviare il Sito

### Prerequisiti
- **Python 3.x** installato
- **Flask** (`pip install flask`)

### Passaggi

1. **Aprire il terminale** nella cartella `majima_construction`

2. **Creare il database** (da fare solo la prima volta o per resettare i dati):
   ```bash
   python setup_db.py
   ```
   Output atteso:
   ```
   ✅ Database creato con successo!
      Ora puoi avviare il server con: python run.py
   ```

3. **Avviare il server**:
   ```bash
   python run.py
   ```
   Output atteso:
   ```
   🚀 Avvio server...
    * Running on http://127.0.0.1:5000
   ```

4. **Aprire il browser** e andare su:
   ```
   http://127.0.0.1:5000
   ```

### Account di Prova
Per testare il sito senza registrarsi:
- **Username:** `admin`
- **Password:** `admin`

---

## 📐 Pattern e Tecnologie Utilizzate

### Pattern
- **Repository Pattern**: separa la logica di business dall'accesso ai dati
- **Blueprint**: organizza le route in moduli separati
- **Factory Pattern**: creazione dell'app Flask tramite funzione `create_app()`

### Tecnologie
- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML5, CSS3 (inline)
- **Templating**: Jinja2
- **Sicurezza**: Werkzeug (hash password con scrypt)

---

## ✅ Validazioni Implementate

- Username, email e telefono devono essere unici
- Telefono: solo numeri, minimo 6 cifre, massimo 15
- Password hashata (mai salvata in chiaro)
- Solo il creatore può modificare/eliminare un progetto
- Il creatore non può essere aggiunto come finanziatore (lo è già implicitamente)

---

*Progetto didattico - Majima Construction*
