import os
from datetime import datetime

CAMINHO_LOG = os.path.join("base_dados", "logs.txt")

def escrever_log(entrada, resposta):
    with open(CAMINHO_LOG, "a", encoding="utf-8") as f:
        f.write("=" * 40 + "\n")
        f.write(f"🕒 {datetime.now().isoformat()}\n")
        f.write(f"👤 Utilizador: {entrada}\n")
        f.write(f"🤖 Agente: {resposta}\n")
