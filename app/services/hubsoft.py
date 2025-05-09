import requests
import os

HUBSOFT_TOKEN = os.getenv("HUBSOFT_TOKEN")
HUBSOFT_BASE_URL = os.getenv("HUBSOFT_BASE_URL")

def buscar_ordens_servico():
    headers = {
        "Authorization": f"Token token={HUBSOFT_TOKEN}"
    }

    response = requests.get(f"{HUBSOFT_BASE_URL}/ordens_servico", headers=headers)
    response.raise_for_status()

    dados_os = response.json()
    ordens_formatadas = []

    for os in dados_os.get("ordens_servico", []):
        item = {
            "Cliente": os.get("cliente", {}).get("razao_social") or os.get("cliente", {}).get("nome"),
            "Tipo": os.get("tipo_ordem"),
            "Descricao_Servico": os.get("descricao_servico"),
            "Tecnicos": ", ".join(t.get("nome") for t in os.get("tecnicos", [])),
            "Descricao_Fechamento": os.get("descricao_fechamento") or "",
            "Status": os.get("status")
        }
        ordens_formatadas.append(item)

    return ordens_formatadas
