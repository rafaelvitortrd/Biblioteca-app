import tkinter as tk
from tkinter import ttk, messagebox
from persistencia.banco_de_dados import BancoDados
from visao.janelaLivros import JanelaLivro
from visao.janelaFuncionarios import JanelaFuncionario
from visao.janelaEmprestimos import JanelaEmprestimo

class JanelaMain(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Biblioteca")
        self.geometry("600x300")
        self.resizable(False, False)

        self.bd = BancoDados()
        if not self.bd.get_funcionarios().lista_entidades:
            self.bd.get_funcionarios().inserir(
                __import__("modelo.funcionario", fromlist=["Funcionario"]).Funcionario(1, "Admin", "admin", "123")
            )

        ttk.Label(self, text="Biblioteca", font=("Arial", 18)).pack(pady=10)
        ttk.Button(self, text="Gerenciar Livros", width=30, command=lambda: JanelaLivro(self, self.bd)).pack(pady=5)
        ttk.Button(self, text="Gerenciar Empréstimos", width=30, command=lambda: JanelaEmprestimo(self, self.bd)).pack(pady=5)
        ttk.Button(self, text="Gerenciar Funcionários", width=30, command=lambda: JanelaFuncionario(self, self.bd)).pack(pady=5)
        ttk.Button(self, text="Sair", width=30, command=self.quit).pack(pady=10)

        self.after(100, self.abrir_login)

    def abrir_login(self):
        from tkinter import simpledialog
        funcionarios = self.bd.get_funcionarios()
        attempts = 0
        while attempts < 5:
            login = simpledialog.askstring("Login", "Login:", parent=self)
            senha = simpledialog.askstring("Senha", "Senha:", parent=self, show="*")
            if login is None or senha is None:
                self.quit(); return

            valid = False
            for f in funcionarios.lista_entidades:
                if f.login == login and f.senha == senha:
                    valid = True
                    break
            if valid:
                messagebox.showinfo("OK", f"Bem-vindo, {f.nome}!")
                return
            else:
                messagebox.showerror("Erro", "Login ou senha inválidos.")
                attempts += 1
        messagebox.showerror("Erro", "Falha na autenticação. Encerrando.")
        self.quit()
