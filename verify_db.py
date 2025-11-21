import sqlite3
import os

DB_NAME = "estoque_vendas.db"

def verify_tables():
    if not os.path.exists(DB_NAME):
        # Tenta inicializar o banco se não existir
        from database import init_db
        init_db()
        
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    tables = ['produtos', 'clientes', 'vendas', 'itens_venda']
    missing_tables = []
    
    for table in tables:
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
        if not cursor.fetchone():
            missing_tables.append(table)
            
    conn.close()
    
    if missing_tables:
        print(f"FALHA: Tabelas faltando: {', '.join(missing_tables)}")
    else:
        print("SUCESSO: Todas as tabelas foram criadas corretamente.")

if __name__ == "__main__":
    verify_tables()
