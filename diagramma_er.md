# Diagramma ER - Majima Construction

```mermaid
erDiagram
    CLIENT {
        INTEGER id PK
        TEXT username UK "NOT NULL"
        TEXT password "NOT NULL"
        TEXT email UK
        TEXT phone UK
        TIMESTAMP created "NOT NULL"
    }
    
    PROJECT {
        INTEGER id PK
        TEXT name UK "NOT NULL"
        TEXT description
        REAL budget
        TEXT status
        INTEGER created_by FK "NOT NULL"
        TIMESTAMP created "NOT NULL"
    }
    
    PROJECT_CLIENT {
        INTEGER project_id PK,FK
        INTEGER client_id PK,FK
    }
    
    CLIENT ||--o{ PROJECT : "crea"
    CLIENT ||--o{ PROJECT_CLIENT : "partecipa"
    PROJECT ||--o{ PROJECT_CLIENT : "coinvolge"
```

## Legenda

| Simbolo | Significato |
|---------|-------------|
| `PK` | Primary Key |
| `FK` | Foreign Key |
| `UK` | Unique Key |
| `\|\|--o{` | Uno a Molti (1:N) |
| `}o--o{` | Molti a Molti (N:N) |

## Relazioni

1. **CLIENT → PROJECT (1:N)**: Un client può creare molti progetti (tramite `created_by`)
2. **CLIENT → PROJECT_CLIENT (1:N)**: Un client può partecipare a molti progetti
3. **PROJECT → PROJECT_CLIENT (1:N)**: Un progetto può avere molti partecipanti
