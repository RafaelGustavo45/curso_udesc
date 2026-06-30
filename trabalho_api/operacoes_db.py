import sqlite3

def conectar():
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fipe_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_fipe TEXT,
            marca TEXT,
            modelo TEXT,
            ano_modelo INTEGER,
            preco REAL,
            preco_extenso TEXT
        )
    ''')
    conn.commit()
    return conn

def buscar_no_cache(codigo_fipe):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fipe_cache WHERE codigo_fipe = ? ORDER BY id DESC LIMIT 1", (codigo_fipe,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado # Retorna os dados da tupla se existir, senão None

def salvar_consulta(dados):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO fipe_cache (codigo_fipe, marca, modelo, ano_modelo, preco, preco_extenso)
                      VALUES (?, ?, ?, ?, ?, ?)''', dados)
    conn.commit()
    conn.close()


def salvar_marcas(tipo, marcas):
    conn = conectar()
    cursor = conn.cursor()
    # Limpa marcas antigas do mesmo tipo para atualizar
    cursor.execute("DELETE FROM marcas_catalogo WHERE tipo_veiculo = ?", (tipo,))
    for marca in marcas:
        cursor.execute("INSERT INTO marcas_catalogo (codigo, nome, tipo_veiculo) VALUES (?, ?, ?)",
                       (marca['valor'], marca['nome'], tipo))
    conn.commit()
    conn.close()

def listar_marcas_com_historico(tipo):
    conn = conectar()
    cursor = conn.cursor()
    # Join com o histórico para contar modelos já consultados
    cursor.execute('''
        SELECT m.codigo, m.nome, COUNT(f.id) as modelos_consultados
        FROM marcas_catalogo m
        LEFT JOIN fipe_cache f ON m.nome = f.marca
        WHERE m.tipo_veiculo = ?
        GROUP BY m.codigo, m.nome
    ''', (tipo,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def listar_consultas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fipe_cache ")
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def listar_marca(marca):
    #pode ser carro/caminhao/moto
    conn = conectar()
    cursor = conn.cursor()
    # Join com o histórico para contar modelos já consultados
    cursor.execute('''
        SELECT preco, nome, codigo from fipe_cache where marca = ? 
    ''', (marca))
    resultados = cursor.fetchall()
    conn.close()
    return resultados
    