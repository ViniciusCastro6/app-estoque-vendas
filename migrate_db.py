import sqlite3

DB_NAME = "estoque_vendas.db"

def migrate_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        # Tenta adicionar a coluna status
        cursor.execute("ALTER TABLE vendas ADD COLUMN status TEXT DEFAULT 'PAGO'")
        print("Coluna 'status' adicionada com sucesso.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Coluna 'status' já existe.")
        else:
            print(f"Erro ao migrar banco de dados: {e}")
            
    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate_db()
