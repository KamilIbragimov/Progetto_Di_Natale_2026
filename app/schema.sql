-- Elimina le tabelle esistenti (per ricominciare da capo)
DROP TABLE IF EXISTS project_client;
DROP TABLE IF EXISTS project;
DROP TABLE IF EXISTS client;

-- Tabella Clienti (sono anche gli utenti che si registrano)
CREATE TABLE client (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  email TEXT UNIQUE,
  phone TEXT UNIQUE,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabella Progetti
CREATE TABLE project (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  description TEXT,
  budget REAL DEFAULT 0,
  status TEXT DEFAULT 'pianificazione',
  created_by INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (created_by) REFERENCES client (id)
);

-- TABELLA PONTE: Collega Progetti e Clienti (Relazione N:N)
CREATE TABLE project_client (
  project_id INTEGER NOT NULL,
  client_id INTEGER NOT NULL,
  PRIMARY KEY (project_id, client_id),
  FOREIGN KEY (project_id) REFERENCES project (id) ON DELETE CASCADE,
  FOREIGN KEY (client_id) REFERENCES client (id) ON DELETE CASCADE
);

-- Dati di esempio (password hashate con werkzeug)
INSERT INTO client (username, password, email, phone) VALUES ('admin', 'scrypt:32768:8:1$v8Bzp5tSJRpGd2x2$803dc25210329e392428d5f5061eaa47302ab8cdec53df23bb562aee602e3073d70050a6f6949fec86e00df74a7ad268dc43bab570e397598c350816be16ef67', 'admin@majima.it', '0123456789');
INSERT INTO client (username, password, email, phone) VALUES ('mario', 'mariopass', 'mario@mail.com', '0987654321');
INSERT INTO client (username, password, email, phone) VALUES ('luigi', 'luigipass', 'luigi@pec.it', '0112233445');

INSERT INTO project (name, description, budget, status, created_by) VALUES 
  ('Casa Moderna', 'Costruzione villa unifamiliare', 150000, 'in_corso', 1);
INSERT INTO project (name, description, budget, status, created_by) VALUES 
  ('Ufficio Centro', 'Ristrutturazione uffici', 80000, 'pianificazione', 1);
INSERT INTO project (name, description, budget, status, created_by) VALUES 
  ('Capannone Nord', 'Nuovo capannone industriale', 500000, 'completato', 2);

INSERT INTO project_client (project_id, client_id) VALUES (1, 2);
INSERT INTO project_client (project_id, client_id) VALUES (2, 3);
INSERT INTO project_client (project_id, client_id) VALUES (3, 1);
