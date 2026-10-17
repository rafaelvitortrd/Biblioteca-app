import tkinter as tk
from tkinter import ttk, messagebox
from visao.janelaEntidade import JanelaEntidade
from modelo.funcionario import Funcionario
from persistencia.persistente import EntidadeNaoEncontradaException

class JanelaFuncionario(JanelaEntidade):
    def __init__(self, parent, banco):
      super().__init__(parent, "Gerenciar Funcionários")
      self.banco = banco
      self.persist = self.banco.get_funcionarios()
      self.create_widgets()
      self.atualizar_tabela()


    def create_widgets(self):
      cols = ("id", "nome", "login")
      self.tree = ttk.Treeview(self, columns=cols, show="headings", height=15)
      for c in cols:
          self.tree.heading(c, text=c.capitalize())
          self.tree.column(c, width=200)
      self.tree.pack(padx=10, pady=10)

      frame = ttk.Frame(self)
      frame.pack(pady=5)
      ttk.Button(frame, text="Cadastrar", command=self.cadastrar).grid(row=0, column=0, padx=5)
      ttk.Button(frame, text="Apagar", command=self.apagar).grid(row=0, column=1, padx=5)



    def atualizar_tabela(self):
      for r in self.tree.get_children():
        self.tree.delete(r)
      for f in self.persist.lista_entidades:
        self.tree.insert("", "end", values=(f.id, f.nome, f.login))


    def cadastrar(self):
      try:
        idv = self.pergunta_inteiro("Cadastrar", "ID:")
        if idv is None: return
        try:
          self.persist.buscar_por_id(idv)
          messagebox.showerror("Erro", "ID já existente.")
          return
        except EntidadeNaoEncontradaException:
          pass
        nome = self.pergunta_texto("Cadastrar", "Nome:")
        if nome is None: return
        login = self.pergunta_texto("Cadastrar", "Login:")
        if login is None: return
        senha = self.pergunta_texto("Cadastrar", "Senha:")
        if senha is None: return
        self.persist.inserir(Funcionario(idv, nome, login, senha))
        messagebox.showinfo("OK", "Funcionário cadastrado.")
        self.atualizar_tabela()
      except Exception as e:
        messagebox.showerror("Erro", str(e))


    def apagar(self):
      idv = self.pergunta_inteiro("Apagar", "ID do funcionário:")
      if idv is None: return
      if self.persist.excluir(idv):
        messagebox.showinfo("OK", "Funcionário removido.")
        self.atualizar_tabela()
      else:
        messagebox.showerror("Erro", "Funcionário não encontrado.")
