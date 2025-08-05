import subprocess

class ModuloInterpretacao:
    def __init__(self, agente_narrativo, modelo="mistral"):
        self.agente = agente_narrativo  # referência ao orquestrador
        self.modelo = modelo

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
        prompt = self.agente.gerar_prompt_emergente(entrada_utilizador)
        resposta = self.consultar_modelo(prompt)
        self.agente.memoria.registar_evento(entrada_utilizador, tipo="input", origem="utilizador")
        self.agente.memoria.registar_evento(resposta, tipo="resposta", origem="agente")
        return resposta
