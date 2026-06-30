import json
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

def buscar_preco_fipe(codigo_fipe):
    url = f"https://brasilapi.com.br/api/fipe/preco/v1/{codigo_fipe}"
    try:
        with urlopen(url) as response:
            if response.status == 200:
                return json.load(response)
        return None
    except (HTTPError, URLError, ValueError):
        return None

def buscar_marcas(tipo):
    url = f"https://brasilapi.com.br/api/fipe/marcas/v1/{tipo}"
    try:
        response = requests.get(url)
        return response.json() if response.status_code == 200 else []
    except:
        return []