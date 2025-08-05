import json
from datetime import datetime
import os

CAMINHO_MEMORIA = os.path.join("base_dados", "memoria.json")

class MemoriaNarrativa:
    def __init__(self):
        self.eventos = []
        self.carregar()

    def registar_evento(self, descricao, tipo="interacao", origem="utilizador", resultado=None):
        evento = {
            "timestamp": datetime.now().isoformat(),
            "tipo": tipo,
            "descricao": descricao,
            "origem": origem,
            "resultado": resultado
        }
        self.eventos.append(evento)
        self.guardar()

    def obter_eventos(self, tipo=None):
        if tipo:
            return [e for e in self.eventos if e["tipo"] == tipo]
        return self.eventos

    def guardar(self):
        with open(CAMINHO_MEMORIA, "w", encoding="utf-8") as f:
            json.dump(self.eventos, f, indent=4)

    def carregar(self):
        try:
            with open(CAMINHO_MEMORIA, "r", encoding="utf-8") as f:
                self.eventos = json.load(f)
        except FileNotFoundError:
            self.eventos = []

    def reconstruir_historia(self):
        return "\n".join([f"[{e['timestamp']}] ({e['tipo']}) {e['descricao']}" for e in self.eventos])
