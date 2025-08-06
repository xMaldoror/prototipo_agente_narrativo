import networkx as nx
import random

class ModuloFocoNarrativo:
    def __init__(self, memoria, esquema, identidade):
        self.memoria = memoria
        self.esquema = esquema
        self.identidade = identidade

    def selecionar_contexto(self, entrada_utilizador, top_n=3):
        # História recente (limite de tokens)
        historia = self.memoria.reconstruir_historia()[-1500:]

        # Grafo e centralidade
        grafo = self.esquema.grafo.grafo
        centralidade = nx.degree_centrality(grafo)
        conceitos_ordenados = sorted(centralidade.items(), key=lambda x: x[1], reverse=True)
        conceitos_principais = [n for n, _ in conceitos_ordenados[:top_n]]

        # Relações focadas
        relacoes_focadas = []
        for origem, destino, dados in grafo.edges(data=True):
            if origem in conceitos_principais or destino in conceitos_principais:
                relacoes_focadas.append(f"{origem} {dados['tipo']} {destino}")

        # Fragmentos identitários focados
        identidade = self.identidade.obter_identidade_atual()
        metanarrativas = [m['descricao'] for m in identidade["metanarrativas"]
                          if any(c in m['descricao'] for c in conceitos_principais)]
        tensoes = [t['descricao'] for t in identidade["tensoes"]
                   if any(c in t['descricao'] for c in conceitos_principais)]

        # Construção ponderada dos blocos
        blocos = []
        if historia:
            blocos.append(("historia", historia))
        if conceitos_principais:
            blocos.append(("conceitos", " ".join(conceitos_principais)))
        if relacoes_focadas:
            blocos.append(("relacoes", " ".join(relacoes_focadas)))
        if metanarrativas:
            blocos.append(("metanarrativas", " ".join(metanarrativas)))
        if tensoes:
            blocos.append(("tensoes", " ".join(tensoes)))

        # Ordenação emergente dos blocos com base em prioridade heurística
        prioridade = {
            "tensoes": 5,
            "metanarrativas": 4,
            "conceitos": 3,
            "relacoes": 2,
            "historia": 1
        }
        blocos_ordenados = sorted(blocos, key=lambda b: prioridade.get(b[0], 0), reverse=True)

        # Construção final do prompt funcional
        partes = [conteudo for _, conteudo in blocos_ordenados]
        partes.append(entrada_utilizador)

        prompt = "\n\n".join(partes)
        return prompt

