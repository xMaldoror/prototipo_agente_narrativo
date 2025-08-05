import networkx as nx
import json
from datetime import datetime

class GrafoConceitual:
    def __init__(self):
        self.grafo = nx.DiGraph()

    def adicionar_conceito(self, conceito, contexto=None):
        if conceito not in self.grafo:
            self.grafo.add_node(conceito, historico=[], contexto=[])
        if contexto:
            self.grafo.nodes[conceito]['contexto'].append(contexto)

    def adicionar_relacao(self, origem, destino, tipo_relacao):
        self.grafo.add_edge(origem, destino, tipo=tipo_relacao, timestamp=datetime.now().isoformat())

    def atualizar_conceito(self, conceito, nova_definicao, contexto):
        if conceito in self.grafo:
            self.grafo.nodes[conceito]['historico'].append({
                "definicao": nova_definicao,
                "timestamp": datetime.now().isoformat(),
                "contexto": contexto
            })

    def exportar_para_json(self, caminho):
        data = nx.node_link_data(self.grafo)
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def carregar_de_json(self, caminho):
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.grafo = nx.node_link_graph(data)
        except FileNotFoundError:
            self.grafo = nx.DiGraph()

    def obter_conceitos(self):
        return list(self.grafo.nodes)

    def obter_relacoes(self):
        return list(self.grafo.edges(data=True))
