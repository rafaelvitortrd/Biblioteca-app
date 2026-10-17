import tkinter as tk
from tkinter import ttk, messagebox
from visao.janelaEntidade import JanelaEntidade
from modelo.emprestimo import Emprestimo
from modelo.item_emprestimo import ItemEmprestimo
from persistencia.persistente import EntidadeNaoEncontradaException

class JanelaEmprestimo(JanelaEntidade):
    def __init__(self, parent, banco):
        super().__init__(parent, "Gerenciar Empréstimos")
        self.banco = banco
        self.persist = self.banco.get_emprestimos()
        self.livros = self.banco.get_livros()
        self.create_widgets()
        self.atualizar_tabela()

    def create_widgets(self):
        cols = ("id", "cliente", "itens")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=12)
        self.tree.heading("id", text="ID")
        self.tree.heading("cliente", text="Cliente")
        self.tree.heading("itens", text="Itens (qtd)")
        self.tree.column("itens", width=300)
        self.tree.pack(padx=10, pady=10)

        frame = ttk.Frame(self)
        frame.pack(pady=5)
        ttk.Button(frame, text="Inserir", command=self.inserir).grid(row=0, column=0, padx=5)
        ttk.Button(frame, text="Alterar", command=self.alterar).grid(row=0, column=1, padx=5)
        ttk.Button(frame, text="Apagar", command=self.apagar).grid(row=0, column=2, padx=5)
        ttk.Button(frame, text="Visualizar", command=self.visualizar).grid(row=0, column=3, padx=5)


    def atualizar_tabela(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        for e in self.persist.lista_entidades:
            itens_qtd = ", ".join(f"{it.livro.nome}x{it.quantidade}" for it in e.itens) if e.itens else "—"
            self.tree.insert("", "end", values=(e.id, e.cliente, itens_qtd))

    def inserir(self):
        idv = self.pergunta_inteiro("Inserir Empréstimo", "ID do empréstimo:")
        if idv is None: return
        cliente = self.pergunta_texto("Inserir Empréstimo", "Nome do cliente:")
        if cliente is None: return

        try:
            self.persist.buscar_por_id(idv)
            messagebox.showerror("Erro", "ID já existente.")
            return
        except EntidadeNaoEncontradaException:
            pass

        emprestimo = Emprestimo(idv, cliente)

        while True:
            escolha = messagebox.askyesno("Adicionar item", "Deseja adicionar um livro ao empréstimo?")
            if not escolha:
                break
            id_liv = self.pergunta_inteiro("Adicionar item", "ID do livro:")
            if id_liv is None: continue
            try:
                livro = self.livros.buscar_por_id(id_liv)
            except EntidadeNaoEncontradaException:
                messagebox.showerror("Erro", "Livro não encontrado.")
                continue

            qtd = 1
            if livro.quantidade < qtd:
                messagebox.showerror("Erro", f"Estoque insuficiente. Disponível: {livro.quantidade}")
                continue

            livro.quantidade -= qtd
            item = ItemEmprestimo(len(emprestimo.itens) + 1, livro, qtd)
            emprestimo.adicionar_item(item)
            messagebox.showinfo("OK", f"Item adicionado. Estoque restante: {livro.quantidade}")

        if len(emprestimo.itens) == 0:
            messagebox.showwarning("Aviso", "Nenhum livro adicionado. Empréstimo cancelado.")
            return

        self.persist.inserir(emprestimo)
        messagebox.showinfo("OK", "Empréstimo cadastrado.")
        self.atualizar_tabela()

    def alterar(self):
        idv = self.pergunta_inteiro("Alterar empréstimo", "ID do empréstimo:")
        if idv is None: return
        try:
            emprestimo = self.persist.buscar_por_id(idv)
        except EntidadeNaoEncontradaException:
            messagebox.showerror("Erro", "Empréstimo não encontrado.")
            return

        while True:
            op = messagebox.askquestion("Alterar", "Adicionar item? (Escolha 'Não' para remover item ou Cancel para sair)")
            if op == 'yes':
                id_liv = self.pergunta_inteiro("Adicionar item", "ID do livro:")
                if id_liv is None: continue
                try:
                    livro = self.livros.buscar_por_id(id_liv)
                except EntidadeNaoEncontradaException:
                    messagebox.showerror("Erro", "Livro não encontrado.")
                    continue
                qtd = self.pergunta_inteiro("Quantidade", "Quantidade:")
                if qtd is None: continue
                if qtd <= 0:
                    messagebox.showerror("Erro", "Quantidade inválida.")
                    continue
                if livro.quantidade < qtd:
                    messagebox.showerror("Erro", f"Estoque insuficiente. Disponível: {livro.quantidade}")
                    continue
                livro.quantidade -= qtd
                item = ItemEmprestimo(len(emprestimo.itens) + 1, livro, qtd)
                emprestimo.adicionar_item(item)
                messagebox.showinfo("OK", "Item adicionado.")
            elif op == 'no':
                if not emprestimo.itens:
                    messagebox.showinfo("Info", "Sem itens para remover.")
                    continue
                texto = "\n".join(f"{i+1} - {it}" for i,it in enumerate(emprestimo.itens))
                messagebox.showinfo("Itens", texto)
                idx = self.pergunta_inteiro("Remover item", "Número do item a remover:")
                if idx is None: continue
                idx -= 1
                if 0 <= idx < len(emprestimo.itens):
                    item = emprestimo.itens.pop(idx)
                    livro_original = self.livros.buscar_por_id(item.livro.id)
                    livro_original.quantidade += item.quantidade
                    messagebox.showinfo("OK", "Item removido e estoque atualizado.")
                else:
                    messagebox.showerror("Erro", "Índice inválido.")
            else:
                break

        self.persist.alterar(emprestimo)
        self.atualizar_tabela()
        messagebox.showinfo("OK", "Empréstimo atualizado.")

    def apagar(self):
        idv = self.pergunta_inteiro("Apagar", "ID do empréstimo:")
        if idv is None: return
        try:
            emprestimo = self.persist.buscar_por_id(idv)
        except EntidadeNaoEncontradaException:
            messagebox.showerror("Erro", "Empréstimo não encontrado.")
            return

        for item in emprestimo.itens:
            livro = self.livros.buscar_por_id(item.livro.id)
            livro.quantidade += item.quantidade

        self.persist.excluir(idv)
        messagebox.showinfo("OK", "Empréstimo removido e livros devolvidos.")
        self.atualizar_tabela()

    def visualizar(self):
        idv = self.pergunta_inteiro("Visualizar", "ID do empréstimo:")
        if idv is None: return
        try:
            emprestimo = self.persist.buscar_por_id(idv)
            messagebox.showinfo("Empréstimo", str(emprestimo))
        except EntidadeNaoEncontradaException:
            messagebox.showerror("Erro", "Empréstimo não encontrado.")
