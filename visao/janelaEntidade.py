import tkinter as tk
from tkinter import ttk, messagebox

class JanelaEntidade(tk.Toplevel):
    def __init__(self, parent, title="Gerenciar"):
        super().__init__(parent)
        self.parent = parent
        self.title(title)
        self.geometry("700x450")
        self.resizable(False, False)

    def pergunta_inteiro(self, titulo, prompt):
        popup = tk.Toplevel(self)
        popup.title(titulo)
        tk.Label(popup, text=prompt).pack(padx=10, pady=5)
        entry = ttk.Entry(popup)
        entry.pack(padx=10, pady=5)
        entry.focus()

        resposta = {"value": None}

        def on_ok():
            val = entry.get()
            try:
                resposta["value"] = int(val)
                popup.destroy()
            except ValueError:
                messagebox.showerror("Erro", "Digite um número inteiro válido.")

        ttk.Button(popup, text="OK", command=on_ok).pack(pady=5)
        popup.grab_set()
        self.wait_window(popup)
        return resposta["value"]

    def pergunta_texto(self, titulo, prompt):
        popup = tk.Toplevel(self)
        popup.title(titulo)
        tk.Label(popup, text=prompt).pack(padx=10, pady=5)
        entry = ttk.Entry(popup)
        entry.pack(padx=10, pady=5)
        entry.focus()

        resposta = {"value": None}

        def on_ok():
            resposta["value"] = entry.get()
            popup.destroy()

        ttk.Button(popup, text="OK", command=on_ok).pack(pady=5)
        popup.grab_set()
        self.wait_window(popup)
        return resposta["value"]
