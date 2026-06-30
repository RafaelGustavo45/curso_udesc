from num2words import num2words
from rich.console import Console # Importar Console daqui
from rich.table import Table     # Table vem daqui
import operacoes_db
import consulta_API
console = Console() # Instanciamos o objeto console aqui

def consultar_preco_por_codigo_fipe(codigo):

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

def obter_dados_veiculo(codigo):
    # Tenta buscar no banco
    cache = operacoes_db.buscar_no_cache(codigo)
    if cache:
        return {'marca': cache[2], 'modelo': cache[3], 'ano': cache[4], 'preco': cache[5], 'extenso': cache[6]}
    
    # Se não tiver, busca na API
    dados = consulta_API.buscar_preco_fipe(codigo)
    if dados:
        preco = float(dados[0]['valor'].replace('R$ ', '').replace('.', '').replace(',', '.'))
        extenso = num2words(preco, lang='pt_BR', to='currency', currency='BRL')
        operacoes_db.salvar_consulta((codigo, dados[0]['marca'], dados[0]['modelo'], dados[0]['anoModelo'], preco, extenso))
        return {'marca': dados[0]['marca'], 'modelo': dados[0]['modelo'], 'ano': dados[0]['anoModelo'], 'preco': preco, 'extenso': extenso}
    return None

def comparar_veiculos():
    cod1 = input("Código FIPE 1: ")
    cod2 = input("Código FIPE 2: ")
    
    v1 = obter_dados_veiculo(cod1)
    v2 = obter_dados_veiculo(cod2)
    
    if not v1 or not v2:
        console.print("[red]Erro ao buscar um dos veículos.[/red]")
        return

    dif = abs(v1['preco'] - v2['preco'])
    dif_extenso = num2words(dif, lang='pt_BR', to='currency', currency='BRL')
    
    mais_caro = "Veículo 1" if v1['preco'] > v2['preco'] else "Veículo 2"
    
    table = Table(title="Comparação de Preços")
    table.add_column("Atributo", style="dim")
    table.add_column("Veículo 1", style="cyan")
    table.add_column("Veículo 2", style="magenta")
    
    table.add_row("Modelo", v1['modelo'], v2['modelo'])
    table.add_row("Preço", f"R$ {v1['preco']:,.2f}", f"R$ {v2['preco']:,.2f}")
    table.add_row("Diferença", "-", f"{dif_extenso} ({dif:,.2f})")
    
    console.print(table)
    console.print(f"[bold green]Resultado:[/bold green] O {mais_caro} é mais caro.")

def listar_marcas():
    tipo = input("Tipo (carros, motos, caminhoes): ").lower()
    
    # Busca e salva no DB
    marcas = consulta_API.buscar_marcas(tipo)
    if not marcas:
        console.print("[red]Erro ao buscar marcas ou tipo inválido.[/red]")
        return
        
    operacoes_db.salvar_marcas(tipo, marcas)
    dados = operacoes_db.listar_marcas_com_historico(tipo)
    
    # Exibe em Rich
    table = Table(title=f"Marcas de {tipo.capitalize()}")
    table.add_column("Código", style="dim")
    table.add_column("Nome", style="cyan")
    table.add_column("Modelos no Histórico", style="green")
    
    for cod, nome, count in dados:
        table.add_row(str(cod), nome, str(count))
        
    console.print(table)

def listar_historico():
    dados = operacoes_db.listar_consultas()

    table = Table(title=f"Dados")
    table.add_column("Código", style="dim")
    table.add_column("Nome", style="cyan")
    table.add_column("Modelo", style="green")
    table.add_column("Marca", style="yellow")
    table.add_column("Ano", style="blue")
    table.add_column("Preço", style="red")
    
    for cod, nome, count in dados:
        table.add_row(str(cod), nome, str(count))
        
    console.print(table)

def listar_marcas_detalhado(): # Renomeei para não conflitar com a anterior
    dados = operacoes_db.listar_marca()
    table = Table(title="Dados de Marcas")
    
    # Corrigido: add_column (um 'l' só)
    table.add_column("Preço", style="orange")
    table.add_column("Nome", style="red")
    table.add_column("Código", style="yellow")

    for cod, nome, preco in dados:
        table.add_row(str(preco), nome, str(cod))
        
    console.print(table)