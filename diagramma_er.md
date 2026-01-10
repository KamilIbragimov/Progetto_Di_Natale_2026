# Diagramma ER - Majima Construction

```mermaid
erDiagram
    CLIENT {
        INTEGER id PK
        TEXT username UK
        TEXT password
        TEXT email UK
        TEXT phone UK
        TIMESTAMP created
    }
    
    PROJECT {
        INTEGER id PK
        TEXT name UK
        TEXT description
        REAL budget
        TEXT status
        INTEGER created_by FK
        TIMESTAMP created
    }
    
    PROJECT_CLIENT {
        INTEGER project_id PK,FK
        INTEGER client_id PK,FK
    }
    
    CLIENT ||--o{ PROJECT : "crea"
    CLIENT }o--o{ PROJECT : "partecipa"
    CLIENT ||--o{ PROJECT_CLIENT : ""
    PROJECT ||--o{ PROJECT_CLIENT : ""
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

1. **CLIENT → PROJECT (1:N)**: Un client può creare molti progetti
2. **CLIENT ↔ PROJECT (N:N)**: Un client può partecipare a molti progetti e viceversa (tramite tabella ponte `PROJECT_CLIENT`)
