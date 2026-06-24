import sqlite3

DB_NAME = "banco.db"

def get_conexao():
    # 1. Conectar ao banco em disco
  conexao = sqlite3.connect(DB_NAME)
  conexao.row_factory = sqlite3.Row
  cursor = conexao.cursor()
  return cursor, conexao


def inicializar_banco(cursor):
    # CREATE TABLE IF NOT EXISTS ...
    # 2. Criar tabela (DDL)
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descricao TEXT NOT NULL,
        concluido TEXT NOT NULL DEFAULT 'N'
    )
""")

def adicionar_tarefa(descricao, titulo):
    # INSERT parametrizado com with ...

    cursor, conexao = get_conexao()
    with conexao:
        cursor.execute("INSERT INTO tarefas (titulo, descricao) VALUES (?, ?)", (titulo, descricao))
        

def listar_tarefas():
    # SELECT * ...
    cursor, conexao = get_conexao() 
    with conexao:
        cursor.execute("SELECT * FROM tarefas")
        tarefas = cursor.fetchall()
        for tarefa in tarefas:
            print(f"ID: {tarefa['id']}, Título: {tarefa['titulo']}, Descrição: {tarefa['descricao']}, Concluído: {tarefa['concluido']}")

# ...

def concluir_tarefa(id_tarefa):
    # UPDATE parametrizado com with ...
    cursor, conexao = get_conexao()
    with conexao:
        cursor.execute("UPDATE tarefas SET concluido = 'S' WHERE id = ?", (id_tarefa,))
        if cursor.rowcount == 0:
            print(f"Tarefa com ID {id_tarefa} não encontrada.")
        else:
            print(f"Tarefa com ID {id_tarefa} concluída.")

def show_menu():
    print("Menu:")
    print("1 - Adicionar tarefa")
    print("2 - Listar Tarefas")
    print("3 - Concluir Tarefa")
    print("4 - Sair")   

if __name__ == "__main__":
    cursor, conexao = get_conexao()
    inicializar_banco(cursor)
    show_menu()
    opcao = int(input("Escolha uma opção: 1 - Adicionar tarefa, 2 - Listar Tarefas, 3 - Conluir Tarefa: , 4- Sair:"))
    while opcao != 4:
        if opcao == 1:
           titulo = input("Digite o título da tarefa: ")
           descricao = input("Digite a descrição da tarefa: ")
           adicionar_tarefa(descricao, titulo)
           show_menu()
           opcao = int(input("Escolha uma opção: 1 - Adicionar tarefa, 2 - Listar Tarefas, 3 - Conluir Tarefa: , 4- Sair:"))
        if opcao == 2:
           listar_tarefas()
           show_menu()
           opcao = int(input("Escolha uma opção: 1 - Adicionar tarefa, 2 - Listar Tarefas, 3 - Conluir Tarefa: , 4- Sair:"))
        if opcao == 3:
           listar_tarefas()
           id_tarefa = int(input("Digite o ID da tarefa a ser concluída: "))
           concluir_tarefa(id_tarefa)
           show_menu()
           opcao = int(input("Escolha uma opção: 1 - Adicionar tarefa, 2 - Listar Tarefas, 3 - Conluir Tarefa: , 4- Sair:"))
        if opcao == 4:
           print("Saindo do programa.")
        if opcao == 0:
            pass
            #gambiarra para não dar erro na primeira execução
        else:
           print("Opção inválida. Tente novamente.")
           show_menu()
           opcao = int(input("Escolha uma opção: 1 - Adicionar tarefa, 2 - Listar Tarefas, 3 - Conluir Tarefa: , 4- Sair:"))
    # Loop com input() para o menu ...
print("Programa encerrado.")