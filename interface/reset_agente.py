import os
import shutil
import json

BASE_DADOS = os.path.join("base_dados")
FICHEIROS_JSON = {
    "memoria.json": [],
    "esquema.json": {
        "directed": True,
        "multigraph": False,
        "graph": {},
        "nodes": [],
        "links": []
    },
    "identidade.json": {
        "metanarrativas": [],
        "pontos_tensao": [],
        "historico_identidade": []
    }
}

def apagar_pycache():
    for root, dirs, _ in os.walk(".."):  # sobe para raiz do projeto
        for d in dirs:
            if d == "__pycache__":
                caminho = os.path.join(root, d)
                shutil.rmtree(caminho)

def resetar_jsons():
    for nome, estrutura in FICHEIROS_JSON.items():
        caminho = os.path.join(BASE_DADOS, nome)
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(estrutura, f, indent=2, ensure_ascii=False)

def executar_reset():
    apagar_pycache()
    resetar_jsons()
