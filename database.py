import sqlite3
from datetime import datetime

DB_NAME = "estoque_vendas.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tabela Produtos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT,
            preco_venda REAL NOT NULL,
            preco_compra REAL,
            quantidade INTEGER NOT NULL,
            ativo INTEGER DEFAULT 1,
            foto TEXT,
            codigo_barras TEXT,
            descricao TEXT,
            fornecedor TEXT
        )
    ''')

    # Tabela Clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT,
            cpf TEXT,
            email TEXT
        )
    ''')

    # Tabela Vendas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            total REAL NOT NULL,
            status TEXT DEFAULT 'PAGO', -- 'PAGO' ou 'PENDENTE'
            data DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (cliente_id) REFERENCES clientes (id)
        )
    ''')

    # Tabela Itens da Venda
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS itens_venda (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venda_id INTEGER,
            produto_id INTEGER,
            quantidade INTEGER NOT NULL,
            preco_unitario REAL NOT NULL,
            FOREIGN KEY (venda_id) REFERENCES vendas (id),
            FOREIGN KEY (produto_id) REFERENCES produtos (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Funções CRUD para Produtos
def add_produto(nome, categoria, preco_venda, preco_compra, quantidade, ativo=1, foto="", codigo_barras="", descricao="", fornecedor=""):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO produtos (nome, categoria, preco_venda, preco_compra, quantidade, ativo, foto, codigo_barras, descricao, fornecedor) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nome, categoria, preco_venda, preco_compra, quantidade, ativo, foto, codigo_barras, descricao, fornecedor))
    conn.commit()
    conn.close()

def get_unique_categories():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT categoria FROM produtos WHERE categoria IS NOT NULL AND categoria != ''")
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    return categories

def get_produtos(search_term="", category=None, min_price=None, max_price=None, low_stock=False, out_of_stock=False, best_sellers=False, show_inactive=False, sort_by=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT p.* FROM produtos p"
    params = []
    conditions = []

    # Join for best sellers if needed
    if best_sellers or sort_by == 'best_sellers':
        query = """
            SELECT p.*, COALESCE(SUM(iv.quantidade), 0) as total_sold
            FROM produtos p
            LEFT JOIN itens_venda iv ON p.id = iv.produto_id
        """

    if search_term:
        conditions.append("p.nome LIKE ?")
        params.append(f'%{search_term}%')
    
    if category:
        conditions.append("p.categoria = ?")
        params.append(category)
        
    if min_price is not None and min_price != "":
        conditions.append("p.preco_venda >= ?")
        params.append(float(min_price))
        
    if max_price is not None and max_price != "":
        conditions.append("p.preco_venda <= ?")
        params.append(float(max_price))
        
    if low_stock:
        conditions.append("p.quantidade <= 5 AND p.quantidade > 0")
        
    if out_of_stock:
        conditions.append("p.quantidade = 0")
        
    if not show_inactive:
        conditions.append("p.ativo = 1")
    elif show_inactive == "only_inactive":
        conditions.append("p.ativo = 0")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)
        
    # Group by if we joined
    if best_sellers or sort_by == 'best_sellers':
        query += " GROUP BY p.id"

    # Sorting Logic
    if sort_by == 'name_asc':
        query += " ORDER BY p.nome ASC"
    elif sort_by == 'price_asc':
        query += " ORDER BY p.preco_venda ASC"
    elif sort_by == 'stock_desc':
        query += " ORDER BY p.quantidade DESC"
    elif sort_by == 'date_desc': # Data de cadastro (ID as proxy)
        query += " ORDER BY p.id DESC"
    elif best_sellers: # Fallback for the checkbox if no specific sort
        query += " ORDER BY total_sold DESC"
    else:
        query += " ORDER BY p.nome ASC" # Default sort
    
    cursor.execute(query, params)
    produtos = cursor.fetchall()
    conn.close()
    return produtos

def update_produto(id, nome, categoria, preco_venda, preco_compra, quantidade, ativo=1, foto="", codigo_barras="", descricao="", fornecedor=""):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE produtos 
        SET nome = ?, categoria = ?, preco_venda = ?, preco_compra = ?, quantidade = ?, ativo = ?, foto = ?, codigo_barras = ?, descricao = ?, fornecedor = ?
        WHERE id = ?
    ''', (nome, categoria, preco_venda, preco_compra, quantidade, ativo, foto, codigo_barras, descricao, fornecedor, id))
    conn.commit()
    conn.close()

def get_produto_movimentacoes(produto_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT v.data, v.id, c.nome, iv.quantidade, iv.preco_unitario, v.status
        FROM itens_venda iv
        JOIN vendas v ON iv.venda_id = v.id
        LEFT JOIN clientes c ON v.cliente_id = c.id
        WHERE iv.produto_id = ?
        ORDER BY v.data DESC
        LIMIT 50
    ''', (produto_id,))
    movimentacoes = cursor.fetchall()
    conn.close()
    return movimentacoes

def delete_produto(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM produtos WHERE id = ?', (id,))
    conn.commit()
    conn.close()

# Funções CRUD para Clientes
def add_cliente(nome, telefone, cpf, email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO clientes (nome, telefone, cpf, email) VALUES (?, ?, ?, ?)',
                   (nome, telefone, cpf, email))
    conn.commit()
    conn.close()

def get_clientes(search_term=""):
    conn = get_db_connection()
    cursor = conn.cursor()
    if search_term:
        cursor.execute('SELECT * FROM clientes WHERE nome LIKE ? OR cpf LIKE ?', (f'%{search_term}%', f'%{search_term}%'))
    else:
        cursor.execute('SELECT * FROM clientes')
    clientes = cursor.fetchall()
    conn.close()
    return clientes

def delete_cliente(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clientes WHERE id = ?', (id,))
    conn.commit()
    conn.close()

# Funções para Vendas
def registrar_venda(cliente_id, itens, status='PAGO'):
    """
    itens: lista de dicionários {'produto_id': int, 'quantidade': int, 'preco_unitario': float}
    status: 'PAGO' ou 'PENDENTE'
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Calcular total
        total = sum(item['quantidade'] * item['preco_unitario'] for item in itens)
        
        # Criar venda
        cursor.execute('INSERT INTO vendas (cliente_id, total, status) VALUES (?, ?, ?)', (cliente_id, total, status))
        venda_id = cursor.lastrowid
        
        # Inserir itens e atualizar estoque
        for item in itens:
            cursor.execute('''
                INSERT INTO itens_venda (venda_id, produto_id, quantidade, preco_unitario)
                VALUES (?, ?, ?, ?)
            ''', (venda_id, item['produto_id'], item['quantidade'], item['preco_unitario']))
            
            # Baixar estoque
            cursor.execute('''
                UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?
            ''', (item['quantidade'], item['produto_id']))
            
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao registrar venda: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def get_historico_compras(cliente_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT v.id, v.total, v.data, v.status, GROUP_CONCAT(p.nome || ' x' || iv.quantidade, ', ') as itens
        FROM vendas v
        JOIN itens_venda iv ON v.id = iv.venda_id
        JOIN produtos p ON iv.produto_id = p.id
        WHERE v.cliente_id = ?
        GROUP BY v.id
        ORDER BY v.data DESC
    ''', (cliente_id,))
    historico = cursor.fetchall()
    conn.close()
    return historico

def get_devedores():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.id, c.nome, c.telefone, SUM(v.total) as total_divida
        FROM vendas v
        JOIN clientes c ON v.cliente_id = c.id
        WHERE v.status = 'PENDENTE'
        GROUP BY c.id
    ''')
    devedores = cursor.fetchall()
    conn.close()
    return devedores

def quitar_divida(cliente_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE vendas SET status = 'PAGO' WHERE cliente_id = ? AND status = 'PENDENTE'", (cliente_id,))
    conn.commit()
    conn.close()

def get_total_vendas():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(total) as total_vendas FROM vendas')
    result = cursor.fetchone()
    total = result['total_vendas'] if result['total_vendas'] else 0.0
    
    cursor.execute('SELECT SUM(quantidade) as total_itens FROM itens_venda')
    result_itens = cursor.fetchone()
    total_itens = result_itens['total_itens'] if result_itens['total_itens'] else 0
    
    conn.close()
    return total, total_itens

def get_dashboard_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Total Vendido (PAGO)
    cursor.execute("SELECT SUM(total) FROM vendas WHERE status = 'PAGO'")
    total_vendido = cursor.fetchone()[0] or 0.0
    
    # Total Itens Vendidos (PAGO)
    cursor.execute('''
        SELECT SUM(iv.quantidade)
        FROM itens_venda iv
        JOIN vendas v ON iv.venda_id = v.id
        WHERE v.status = 'PAGO'
    ''')
    total_itens = cursor.fetchone()[0] or 0
    
    # Total Investido (Estoque Atual)
    cursor.execute("SELECT SUM(preco_compra * quantidade) FROM produtos")
    total_investido = cursor.fetchone()[0] or 0.0
    
    # Lucro Líquido (PAGO) - Estimado com base no custo atual
    cursor.execute('''
        SELECT SUM((iv.preco_unitario - p.preco_compra) * iv.quantidade)
        FROM itens_venda iv
        JOIN vendas v ON iv.venda_id = v.id
        JOIN produtos p ON iv.produto_id = p.id
        WHERE v.status = 'PAGO'
    ''')
    lucro_liquido = cursor.fetchone()[0] or 0.0
    
    # Total a Receber (PENDENTE)
    cursor.execute("SELECT SUM(total) FROM vendas WHERE status = 'PENDENTE'")
    total_pendente = cursor.fetchone()[0] or 0.0
    
    conn.close()
    return {
        "total_vendido": total_vendido,
        "total_itens": total_itens,
        "total_investido": total_investido,
        "lucro_liquido": lucro_liquido,
        "total_pendente": total_pendente
    }
