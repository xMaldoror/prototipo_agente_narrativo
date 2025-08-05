from agente_narrativo.modulo_memoria import MemoriaNarrativa
from agente_narrativo.modulo_esquema import EsquemaConceitual
from agente_narrativo.modulo_identidade import IdentidadeNarrativa
from agente_narrativo.modulo_redescricao import ModuloRedescricao
from agente_narrativo.modulo_interpretacao import ModuloInterpretacao

class AgenteNarrativo:
    def __init__(self):
        self.memoria = MemoriaNarrativa()
        self.esquema = EsquemaConceitual()
        self.identidade = IdentidadeNarrativa()
        self.interpretador = ModuloInterpretacao(self.memoria)
        self.redescritor = ModuloRedescricao(self.memoria, self.esquema, self.identidade)
        self.contador_interacoes = 0
        self.intervalo_redescricao = 5  # redescrever a cada 5 interações

    def interagir(self, entrada_utilizador):
        resposta = self.interpretador.interpretar(entrada_utilizador)

        # Atualização conceptual automática (simples)
        self._detetar_conceitos(entrada_utilizador + " " + resposta)

        self.contador_interacoes += 1
        if self.contador_interacoes >= self.intervalo_redescricao:
            self.redescritor.redescrever()
            self.contador_interacoes = 0

        return resposta

    def _detetar_conceitos(self, texto):
        # Aqui usamos uma heurística simples: palavras com letra maiúscula no meio da frase
        import re
        candidatos = re.findall(r'\b[A-ZÁÉÍÓÚÂÊÎÔÛÀÇ][a-zà-ú]+\b', texto)
        contexto = f"Extraído da interação: {texto[:50]}..."
        for conceito in set(candidatos):
            self.esquema.adicionar_uso_conceito(conceito, definicao=f"Uso narrativo do conceito '{conceito}'", contexto=contexto)

    def identidade_atual(self):
        return self.identidade.obter_identidade_atual()

    def reconstruir_historia(self):
        return self.memoria.reconstruir_historia()
