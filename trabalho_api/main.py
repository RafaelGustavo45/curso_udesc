from num2words import num2words
from rich.console import Console
from rich.table import Table
import consulta_API
import operacoes_db
import opcoes

console = Console()

def main():
    opcao =0
    while True:
        print("--- Consultor FIPE ---")
        print("Opções: ")
        print("1- Consultar preço por código FIPE")
        print("2- Listar marcas por tipo de veiculo")
        print("3- Listar modelos por marca")
        print("4- Comparar preços de dois veículos")
        print("5- Histórico de consultas")
        print("6- Sair")
        opcao = int(input("Escolha uma opção: "))
        if opcao == 1:    
            codigo = input("Digite o código FIPE: ")
            opcoes.consultar_preco_por_codigo_fipe(codigo)
        if opcao== 4:
            opcoes.comparar_veiculos()
        if opcao== 2:
            opcoes.listar_marcas()
        if opcao == 5:
            opcoes.listar_historico()
        if opcao == 3:
            opcoes.listar_marcas_detalhado()
        if opcao == 6:
            break
        else:
           print("Opcao invalida, retornando")


if __name__ == "__main__":
    main()