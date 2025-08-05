import subprocess
from agente_narrativo.modulo_memoria import MemoriaNarrativa

class ModuloInterpretacao:
    def __init__(self, memoria: MemoriaNarrativa, modelo="mistral"):
        self.memoria = memoria
        self.modelo = modelo

    def gerar_prompt(self, entrada_utilizador):
        contexto = self.memoria.reconstruir_historia()
        prompt = f"""
Abaixo está uma sequência de interações narrativas de um agente que constrói sua identidade através da linguagem. Responde com base apenas nessa história, como se estivesses a continuar a tua própria narrativa.

{contexto}

Novo evento: {entrada_utilizador}
"""
        return prompt.strip()

    def consultar_modelo(self, prompt):
        try:
            comando = ['ollama', 'run', self.modelo, prompt]
            resultado = subprocess.run(
                comando,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            return resultado.stdout.strip()
        except Exception as e:
            return f"[Erro ao invocar LLM: {str(e)}]"

    def interpretar(self, entrada_utilizador):
        prompt = self.gerar_prompt(entrada_utilizador)
        resposta = self.consultar_modelo(prompt)
        self.memoria.registar_evento(entrada_utilizador, tipo="input", origem="utilizador")
        self.memoria.registar_evento(resposta, tipo="resposta", origem="agente")
        return resposta
