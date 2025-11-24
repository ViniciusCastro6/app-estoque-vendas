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

    try:
        # Tenta adicionar a coluna ativo na tabela produtos
        cursor.execute("ALTER TABLE produtos ADD COLUMN ativo INTEGER DEFAULT 1")
        print("Coluna 'ativo' adicionada com sucesso.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Coluna 'ativo' já existe.")
        else:
            print(f"Erro ao migrar banco de dados (produtos): {e}")

    # Novas colunas para Quick View
    new_columns = [
        ("foto", "TEXT"),
        ("codigo_barras", "TEXT"),
        ("descricao", "TEXT"),
        ("fornecedor", "TEXT")
    ]

    for col_name, col_type in new_columns:
        try:
            cursor.execute(f"ALTER TABLE produtos ADD COLUMN {col_name} {col_type}")
            print(f"Coluna '{col_name}' adicionada com sucesso.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print(f"Coluna '{col_name}' já existe.")
            else:
                print(f"Erro ao adicionar coluna '{col_name}': {e}")
            
    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate_db()
