import os
from utils.grafo_utils import GrafoConceitual

CAMINHO_ESQUEMA = os.path.join("base_dados", "esquema.json")

class EsquemaConceitual:
    def __init__(self):
        self.grafo = GrafoConceitual()
        self.grafo.carregar_de_json(CAMINHO_ESQUEMA)

    def adicionar_uso_conceito(self, conceito, definicao, contexto):
        self.grafo.adicionar_conceito(conceito, contexto)
        self.grafo.atualizar_conceito(conceito, definicao, contexto)
        self.guardar()

    def relacionar_conceitos(self, origem, destino, tipo_relacao):
        self.grafo.adicionar_relacao(origem, destino, tipo_relacao)
        self.guardar()

    def guardar(self):
        self.grafo.exportar_para_json(CAMINHO_ESQUEMA)

    def obter_conceitos(self):
        return self.grafo.obter_conceitos()

    def obter_relacoes(self):
        return self.grafo.obter_relacoes()

    def obter_definicoes_conceito(self, conceito):
        if conceito in self.grafo.grafo.nodes:
            return self.grafo.grafo.nodes[conceito].get('historico', [])
        return []
