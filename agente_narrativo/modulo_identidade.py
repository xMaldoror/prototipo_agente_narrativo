import os
import json
from datetime import datetime

CAMINHO_IDENTIDADE = os.path.join("base_dados", "identidade.json")

class IdentidadeNarrativa:
    def __init__(self):
        self.perfil = {
            "metanarrativas": [],
            "pontos_tensao": [],
            "historico_identidade": []
        }
        self.carregar()

    def registar_reflexao(self, texto, origem="redescricao"):
        entrada = {
            "timestamp": datetime.now().isoformat(),
            "origem": origem,
            "conteudo": texto
        }
        self.perfil["historico_identidade"].append(entrada)
        self.guardar()

    def atualizar_metanarrativa(self, descricao):
        self.perfil["metanarrativas"].append({
            "descricao": descricao,
            "timestamp": datetime.now().isoformat()
        })
        self.guardar()

    def registar_tensao(self, descricao):
        self.perfil["pontos_tensao"].append({
            "descricao": descricao,
            "timestamp": datetime.now().isoformat()
        })
        self.guardar()

    def obter_identidade_atual(self):
        return {
            "metanarrativas": self.perfil["metanarrativas"][-3:],
            "tensoes": self.perfil["pontos_tensao"][-3:]
        }

    def guardar(self):
        with open(CAMINHO_IDENTIDADE, "w", encoding="utf-8") as f:
            json.dump(self.perfil, f, indent=4)

    def carregar(self):
        try:
            with open(CAMINHO_IDENTIDADE, "r", encoding="utf-8") as f:
                self.perfil = json.load(f)
        except FileNotFoundError:
            self.perfil = {
                "metanarrativas": [],
                "pontos_tensao": [],
                "historico_identidade": []
            }
