import requests
import rich

from rich.console import Console
from rich.table import Table

console = Console()

def coluna_estados(estados):
    table = rich.table.Table(title="Estados")
    table.add_column("ID", style="cyan")
    table.add_column("Nome", style="magenta")
    table.add_column("Sigla", style="green")

    for estado in estados:
        table.add_row(str(estado['id']), estado['nome'], estado['sigla'])

    rich.print(table)

def coluna_cidades(cidades):
    table = rich.table.Table(title="Cidades")
    table.add_column("ID", style="cyan")
    table.add_column("Nome", style="magenta")

    for cidade in cidades:
        table.add_row(str(cidade['id']), cidade['nome'])

    rich.print(table)

def detalhar_cidade(cidade_id):
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/municipios/{cidade_id}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API do IBGE: {e}")
        return None

    try:
        cidade = response.json()
    except ValueError:
        print("Erro ao decodificar a resposta JSON.")
        return None

    return cidade   

def listar_estados():
    """
    Consulta a API do IBGE e retorna uma lista de estados brasileiros.
    """
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Lança exceção para códigos HTTP de erro
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API do IBGE: {e}")
        return []

    try:
        estados = response.json()
    except ValueError:
        print("Erro ao decodificar a resposta JSON.")
        return []

    # Ordena por nome do estado
    estados_ordenados = sorted(estados, key=lambda x: x['nome'])

    return estados_ordenados


def listar_cidades(estado_id):
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{estado_id}/municipios"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API do IBGE: {e}")
        return []

    try:
        cidades = response.json()
    except ValueError:
        print("Erro ao decodificar a resposta JSON.")
        return []

    # Ordena por nome da cidade
    cidades_ordenadas = sorted(cidades, key=lambda x: x['nome'])

    return cidades_ordenadas

if __name__ == "__main__":
    estados = listar_estados()
    if estados:
        print(f"Total de estados: {len(estados)}\n")
        coluna_estados(estados)

    selecionarEstado = input("\nDigite o ID do estado que deseja selecionar: ")
    estado_selecionado = next((estado for estado in estados if str(estado['id']) == selecionarEstado), None)
    if estado_selecionado:
        print(f"voce selecionou: {estado_selecionado['id']} - {estado_selecionado['nome']} ({estado_selecionado['sigla']})")
        # Aqui você pode adicionar mais funcionalidades, como consultar cidades do estado selecionado, etc. 
        cidades = listar_cidades(estado_selecionado['id'])
        #listar as cidades do estado seleionado

        if cidades:
            print(f"\nTotal de cidades em {estado_selecionado['nome']}: {len(cidades)}")
            coluna_cidades(cidades)
            selecionarCidade = input("\nDigite o ID da cidade que deseja selecionar: ")
            cidade_selecionada = next((cidade for cidade in cidades if str(cidade['id']) == selecionarCidade), None)
                
            if cidade_selecionada:
                print(f"voce selecionou: {cidade_selecionada['id']} - {cidade_selecionada['nome']}")
                print("\nDetalhes da cidade selecionada:")
                print(f"detalhes: {detalhar_cidade(cidade_selecionada['id'])}")
            else:
                print("Cidade não encontrada.")

    else:
        print("Estado não encontrado.")
