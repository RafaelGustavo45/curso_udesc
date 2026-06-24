import sqlite3

DB_NAME = "banco.db"

def get_conexao():
    conexao = sqlite3.connect(DB_NAME)
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()
    return cursor, conexao

def inicializar_banco():
    cursor, conexao = get_conexao()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            concluido TEXT NOT NULL DEFAULT 'N'
        )
    """)
    conexao.close()

def adicionar_tarefa(titulo, descricao):
    cursor, conexao = get_conexao()
    with conexao:
        cursor.execute("INSERT INTO tarefas (titulo, descricao) VALUES (?, ?)", (titulo, descricao))
    conexao.close()

def listar_tarefas():
    cursor, conexao = get_conexao()
    cursor.execute("SELECT * FROM tarefas")
    tarefas = cursor.fetchall()
    print("\n--- Lista de Tarefas ---")
    for t in tarefas:
        print(f"ID: {t['id']} | Título: {t['titulo']} | Desc: {t['descricao']} | Concluído: {t['concluido']}")
    conexao.close()

def concluir_tarefa(id_tarefa):
    cursor, conexao = get_conexao()
    # Verifica se existe antes de atualizar
    cursor.execute("SELECT id FROM tarefas WHERE id = ?", (id_tarefa,))
    if cursor.fetchone():
        with conexao:
            cursor.execute("UPDATE tarefas SET concluido = 'S' WHERE id = ?", (id_tarefa,))
        print(f"Tarefa {id_tarefa} marcada como concluída.")
    else:
        print(f"Erro: Tarefa com ID {id_tarefa} não encontrada.")
    conexao.close()

def deletar_tarefa(id_tarefa):
    cursor, conexao = get_conexao()
    # Verifica se existe antes de deletar
    cursor.execute("SELECT id FROM tarefas WHERE id = ?", (id_tarefa,))
    if cursor.fetchone():
        with conexao:
            cursor.execute("DELETE FROM tarefas WHERE id = ?", (id_tarefa,))
        print(f"Tarefa {id_tarefa} excluída com sucesso.")
    else:
        print(f"Erro: Tarefa com ID {id_tarefa} não encontrada.")
    conexao.close()

def show_menu():
    print("\nMenu: 1-Adicionar, 2-Listar, 3-Concluir, 4-Deletar, 5-Sair")

if __name__ == "__main__":
    inicializar_banco()
    while True:
        show_menu()
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            titulo = input("Título: ")
            descricao = input("Descrição: ")
            adicionar_tarefa(titulo, descricao)
        elif opcao == '2':
            listar_tarefas()
        elif opcao == '3':
            id_tarefa = int(input("ID da tarefa para concluir: "))
            concluir_tarefa(id_tarefa)
        elif opcao == '4':
            id_tarefa = int(input("ID da tarefa para deletar: "))
            deletar_tarefa(id_tarefa)
        elif opcao == '5':
            print("Programa encerrado.")
            break
        else:
            print("Opção inválida.")
