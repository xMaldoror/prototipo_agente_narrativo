import tkinter as tk
from tkinter import scrolledtext, messagebox
from agente_narrativo.modulo_narrativo import AgenteNarrativo
from analise_dados.modulo_analise_dados import registar_interacao
import os

class InterfaceTkinter:
    def __init__(self):
        self.agente = AgenteNarrativo()
        self.root = tk.Tk()
        self.root.title("Agente Narrativo com Ética Emergente")
        self.root.geometry("700x600")

        self.texto_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=25)
        self.texto_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.entrada = tk.Entry(self.root, font=("Arial", 12))
        self.entrada.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.entrada.bind("<Return>", self.enviar_input)

        botoes_frame = tk.Frame(self.root)
        botoes_frame.pack(pady=5)

        tk.Button(botoes_frame, text="Enviar", command=self.enviar_input).pack(side=tk.LEFT, padx=5)
        tk.Button(botoes_frame, text="Reiniciar", command=self.reiniciar).pack(side=tk.LEFT, padx=5)

        self.texto_display.insert(tk.END, "Agente iniciado. Pode começar a interagir.\n\n")

    def enviar_input(self, event=None):
        entrada = self.entrada.get().strip()
        if entrada:
            self.texto_display.insert(tk.END, f"Você: {entrada}\n\n")
            resposta = self.agente.interagir(entrada)
            self.texto_display.insert(tk.END, f"Agente: {resposta}\n\n")
            self.entrada.delete(0, tk.END)
            self.texto_display.see(tk.END)
            registar_interacao(entrada, resposta)

    def reiniciar(self):
        resposta = messagebox.askyesno("Reiniciar", "Deseja apagar a memória e reiniciar o agente?")
        if resposta:
            for ficheiro in ["memoria.json", "esquema.json", "identidade.json"]:
                caminho = os.path.join("base_dados", ficheiro)
                try:
                    os.remove(caminho)
                except FileNotFoundError:
                    pass
            self.texto_display.insert(tk.END, "\n⚠️ Agente reiniciado. Memória apagada.\n\n")
            self.agente = AgenteNarrativo()

    def executar(self):
        self.root.mainloop()
