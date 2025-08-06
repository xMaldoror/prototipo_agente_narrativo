from agente_narrativo.modulo_memoria import MemoriaNarrativa
from agente_narrativo.modulo_esquema import EsquemaConceitual
from agente_narrativo.modulo_identidade import IdentidadeNarrativa
from agente_narrativo.modulo_redescricao import ModuloRedescricao
from agente_narrativo.modulo_interpretacao import ModuloInterpretacao
from agente_narrativo.modulo_foco_narrativo import ModuloFocoNarrativo

class AgenteNarrativo:
    def __init__(self):
        self.memoria = MemoriaNarrativa()
        self.esquema = EsquemaConceitual()
        self.identidade = IdentidadeNarrativa()
        self.foco = ModuloFocoNarrativo(self.memoria, self.esquema, self.identidade)
        self.interpretador = ModuloInterpretacao(self)
        self.redescritor = ModuloRedescricao(self.memoria, self.esquema, self.identidade)
        self.contador_interacoes = 0
        self.intervalo_redescricao = 2  # redescrever a cada 2 interações

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
        import re
        candidatos = re.findall(r'\b[A-ZÁÉÍÓÚÂÊÎÔÛÀÇ][a-zà-ú]+\b', texto)
        contexto = f"Extraído da interação: {texto[:50]}..."
        for conceito in set(candidatos):
            self.esquema.adicionar_uso_conceito(conceito, definicao=f"Uso narrativo do conceito '{conceito}'", contexto=contexto)

    def identidade_atual(self):
        return self.identidade.obter_identidade_atual()

    def reconstruir_historia(self):
        return self.memoria.reconstruir_historia()

    def gerar_prompt_emergente(self, entrada_utilizador):
        return self.foco.selecionar_contexto(entrada_utilizador)

