from num2words import num2words
from rich.console import Console
from rich.table import Table
import consulta_API
import operacoes_db
import opcoes

console = Console()

def main():
    print("--- Consultor FIPE ---")
    print("Opções: ")
    print("1- Consultar preço por código FIPE")
    print("2- Listar marcas por tipo de veiculo")
    print("3- Listar modelos por marca e tipo de veiculo")
    print("4- Comparar preços de dois veículos")
    print("5- Histórico de consultas")
    print("6- Sair")
    opcao = input("Escolha uma opção: ")
    if opcao == "1":    
        codigo = input("Digite o código FIPE: ")
        # tipo (carro, moto, caminhao) é ignorado na API FIPE da BrasilAPI, 
       # mas solicitado pelo requisito:
        input("Tipo de veículo (carro/moto/caminhao): ") 

        dados_api = consulta_API.buscar_preco_fipe(codigo)
 
        if not dados_api:
            console.print("[red]Erro: Código inválido ou API indisponível.[/red]")
            return

      # Processamento
        preco_num = float(dados_api[0]['valor'].replace('R$ ', '').replace('.', '').replace(',', '.'))
        preco_extenso = num2words(preco_num, lang='pt_BR', to='currency', currency='BRL')

    # Salvar no DB
        operacoes_db.salvar_consulta((
            codigo, dados_api[0]['marca'], dados_api[0]['modelo'], 
            dados_api[0]['anoModelo'], preco_num, preco_extenso
        ))

    # Exibir via Rich
        table = Table(title="Resultado da Consulta")
        table.add_column("Veículo", style="cyan")
        table.add_column("Ano", style="magenta")
        table.add_column("Preço (R$)", style="green")
        table.add_column("Por Extenso", style="yellow")

        table.add_row(
            f"{dados_api[0]['marca']} {dados_api[0]['modelo']}",
            str(dados_api[0]['anoModelo']),
            f"{preco_num:,.2f}",
            preco_extenso
        )
        console.print(table)
    if opcao=="4":
        opcoes.comparar_veiculos()
    if opcao=="2":
        opcoes.listar_marcas()


if __name__ == "__main__":
    main()