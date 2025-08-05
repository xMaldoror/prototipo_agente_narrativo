import networkx as nx
import json
from datetime import datetime
import os

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
            json.dump(data, f, indent=4, ensure_ascii=False)

    def carregar_de_json(self, caminho):
        if not os.path.exists(caminho):
            self.grafo = nx.DiGraph()
            return
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if "nodes" in data and "links" in data:
                    self.grafo = nx.node_link_graph(data, directed=True, multigraph=False, edges="links")
                else:
                    # estrutura inválida → criar grafo vazio
                    print("Aviso: esquema.json com estrutura inválida. Criado grafo novo.")
                    self.grafo = nx.DiGraph()
        except Exception as e:
            print(f"Erro ao carregar esquema conceitual: {e}")
            self.grafo = nx.DiGraph()

    def obter_conceitos(self):
        return list(self.grafo.nodes)

    def obter_relacoes(self):
        return list(self.grafo.edges(data=True))
