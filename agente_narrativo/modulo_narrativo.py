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
        self.interpretador = ModuloInterpretacao(self)
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

    def gerar_prompt_emergente(self, entrada_utilizador):
        # 🧠 História recente
        historia = self.memoria.reconstruir_historia()

        # 🕸️ Conceitos em uso
        conceitos = self.esquema.obter_conceitos()
        relacoes = self.esquema.obter_relacoes()
        bloco_conceitos = "\n".join([f"- {c}" for c in conceitos])
        bloco_relacoes = "\n".join([
            f"{origem} {dados['tipo']} {destino}"
            for origem, destino, dados in relacoes
        ])

        # 🧬 Identidade
        identidade = self.identidade.obter_identidade_atual()
        bloco_identidade = ""
        if identidade["metanarrativas"]:
            bloco_identidade += "Metanarrativas recentes:\n"
            bloco_identidade += "\n".join(f"• {m['descricao']}" for m in identidade["metanarrativas"])
        if identidade["tensoes"]:
            bloco_identidade += "\nTensões em aberto:\n"
            bloco_identidade += "\n".join(f"• {t['descricao']}" for t in identidade["tensoes"])

        prompt = f"""
Memória narrativa:
{historia}

Conceitos em uso:
{bloco_conceitos}

Relações conceptuais:
{bloco_relacoes}

Identidade narrativa:
{bloco_identidade}

Novo evento:
{entrada_utilizador}
""".strip()

        return prompt
