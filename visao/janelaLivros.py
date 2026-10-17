import tkinter as tk
from tkinter import ttk, messagebox
from visao.janelaEntidade import JanelaEntidade
from modelo.livro import Livro
from persistencia.persistente import EntidadeNaoEncontradaException

class JanelaLivro(JanelaEntidade):
    def __init__(self, parent, banco):
        super().__init__(parent, "Gerenciar Livros")
        self.banco = banco
        self.persist = self.banco.get_livros()
        self.create_widgets()
        self.atualizar_tabela()

    def create_widgets(self):
        cols = ("id", "nome", "autor", "quantidade")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=15)
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, width=150)
        self.tree.pack(padx=10, pady=10)

        frame = ttk.Frame(self)
        frame.pack(pady=5)
        ttk.Button(frame, text="Inserir", command=self.inserir).grid(row=0, column=0, padx=5)
        ttk.Button(frame, text="Alterar", command=self.alterar).grid(row=0, column=1, padx=5)
        ttk.Button(frame, text="Apagar", command=self.apagar).grid(row=0, column=2, padx=5)
        ttk.Button(frame, text="Buscar", command=self.buscar).grid(row=0, column=3, padx=5)


    def atualizar_tabela(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        for l in self.persist.lista_entidades:
            self.tree.insert("", "end", values=(l.id, l.nome, l.autor, l.quantidade))

    def inserir(self):
        try:
            idv = self.pergunta_inteiro("Inserir", "ID:")
            if idv is None: return
            nome = self.pergunta_texto("Inserir", "Nome:")
            if nome is None: return
            autor = self.pergunta_texto("Inserir", "Autor:")
            if autor is None: return
            qtd = self.pergunta_inteiro("Inserir", "Quantidade:")
            if qtd is None: return

            try:
                self.persist.buscar_por_id(idv)
                messagebox.showerror("Erro", "ID já existente.")
                return
            except EntidadeNaoEncontradaException:
                pass

            self.persist.inserir(Livro(idv, nome, autor, qtd))
            messagebox.showinfo("OK", "Livro inserido.")
            self.atualizar_tabela()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def alterar(self):
        try:
            idv = self.pergunta_inteiro("Alterar", "ID do livro:")
            if idv is None: return
            try:
                livro = self.persist.buscar_por_id(idv)
            except EntidadeNaoEncontradaException:
                messagebox.showerror("Erro", "Livro não encontrado.")
                return

            nome = self.pergunta_texto("Alterar", "Novo nome:")
            if nome is None: return
            autor = self.pergunta_texto("Alterar", "Novo autor:")
            if autor is None: return
            qtd = self.pergunta_inteiro("Alterar", "Quantidade:")
            if qtd is None: return

            self.persist.alterar(Livro(idv, nome, autor, qtd))
            messagebox.showinfo("OK", "Livro alterado.")
            self.atualizar_tabela()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def apagar(self):
        idv = self.pergunta_inteiro("Apagar", "ID do livro:")
        if idv is None: return
        if self.persist.excluir(idv):
            messagebox.showinfo("OK", "Livro removido.")
            self.atualizar_tabela()
        else:
            messagebox.showerror("Erro", "Livro não encontrado.")

    def buscar(self):
        idv = self.pergunta_inteiro("Buscar", "ID do livro:")
        if idv is None: return
        try:
            livro = self.persist.buscar_por_id(idv)
            messagebox.showinfo("Encontrado", str(livro))
        except EntidadeNaoEncontradaException:
            messagebox.showerror("Erro", "Livro não encontrado.")
