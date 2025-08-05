from datetime import datetime
from agente_narrativo.modulo_memoria import MemoriaNarrativa
from agente_narrativo.modulo_esquema import EsquemaConceitual
from agente_narrativo.modulo_identidade import IdentidadeNarrativa

class ModuloRedescricao:
    def __init__(self, memoria: MemoriaNarrativa, esquema: EsquemaConceitual, identidade: IdentidadeNarrativa):
        self.memoria = memoria
        self.esquema = esquema
        self.identidade = identidade

    def redescrever(self):
        historia = self.memoria.reconstruir_historia()
        conceitos = self.esquema.obter_conceitos()

        redescricoes = []
        for conceito in conceitos:
            definicoes = self.esquema.obter_definicoes_conceito(conceito)
            if len(definicoes) >= 2:
                anterior = definicoes[-2]["definicao"]
                atual = definicoes[-1]["definicao"]
                if anterior != atual:
                    texto = (
                        f"O conceito '{conceito}' evoluiu: era '{anterior}' e passou a ser '{atual}'. "
                        f"Reflete uma mudança ocorrida em {definicoes[-1]['timestamp']}."
                    )
                    redescricoes.append(texto)
                    self.identidade.registar_reflexao(texto)
                    self.identidade.registar_tensao(f"Mudança no conceito '{conceito}'.")

        if redescricoes:
            narrativa_refletida = "\n".join(redescricoes)
            self.memoria.registar_evento(narrativa_refletida, tipo="redescricao", origem="agente")
            self.identidade.atualizar_metanarrativa("Mudanças emergentes na autointerpretação.")

        return redescricoes
