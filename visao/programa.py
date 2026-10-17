# Trabalho Pratico 1 - Programacao Modular
# Aluno: Rafael Vitor Teixeira Rezende Dutra
# Tema: Aplicativo de uma Biblioteca

from persistencia.banco_de_dados import BancoDados
from modelo.livro import Livro
from modelo.emprestimo import Emprestimo
from modelo.item_emprestimo import ItemEmprestimo
from modelo.funcionario import Funcionario
from persistencia.persistente import EntidadeNaoEncontradaException

class Programa:
    def __init__(self):
        self.bd = BancoDados()
        self.usuario_logado = None

    def executar(self):
        if not self.autenticar():
            print("Falha na autenticação!")
            return

        while True:
            print("\n -------------BIBLIOTECA-------------")
            print("\n -----------MENU PRINCIPAL-----------")
            print("1 - Gerenciar Livros")
            print("2 - Gerenciar Empréstimos")
            print("3 - Gerenciar Funcionários")
            print("0 - Sair")
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.menu_livros()
            elif opcao == "2":
                self.menu_emprestimos()
            elif opcao == "3":
                self.menu_funcionarios()
            elif opcao == "0":
                print(" Saindo do sistema...")
                break
            else:
                print(" Opção inválida!")

    def autenticar(self):
        funcionarios = self.bd.get_funcionarios()
        if not funcionarios.lista_entidades:
            print("Nenhum funcionário cadastrado. Cadastre o primeiro usuário.")
            self.cadastrar_funcionario()

        for _ in range(3):
            login = input("Login: ")
            senha = input("Senha: ")
            for f in funcionarios.lista_entidades:
                if f.login == login and f.senha == senha:
                    self.usuario_logado = f
                    print(f"Bem-vindo, {f.nome}!")
                    return True
            print("Login ou senha inválidos.")
        return False

    def cadastrar_funcionario(self):
        id = int(input("ID do funcionário: "))
        funcionarios = self.bd.get_funcionarios()

        try:
            funcionarios.buscar_por_id(id)
            print(f"Erro: Já existe um funcionário com ID {id}.")
            return
        except EntidadeNaoEncontradaException:
            pass 

        nome = input("Nome: ")
        login = input("Login: ")
        senha = input("Senha: ")
        f = Funcionario(id, nome, login, senha)
        funcionarios.inserir(f)
        print(f"Funcionário {nome} cadastrado com sucesso!")

    def menu_funcionarios(self):
        while True:
            print("\n -----------MENU FUNCIONÁRIOS-----------")
            print("1 - Cadastrar funcionário")
            print("2 - Listar funcionários")
            print("0 - Voltar")
            opcao = input("Escolha uma opção: ")

            funcionarios = self.bd.get_funcionarios()

            if opcao == "1":
                self.cadastrar_funcionario()
            elif opcao == "2":
                print("\n* Todos os funcionários:")
                print(funcionarios)
            elif opcao == "0":
                break
            else:
                print(" Opção inválida!")

    def menu_livros(self):
        while True:
            print("\n -----------MENU LIVROS-----------")
            print("1 - Inserir Livro")
            print("2 - Alterar Livro")
            print("3 - Apagar Livro")
            print("4 - Visualizar Livro por ID")
            print("5 - Visualizar Todos os Livros")
            print("0 - Voltar")
            opcao = input("Escolha uma opção: ")

            livros = self.bd.get_livros()

            if opcao == "1":
                id = int(input("ID: "))
                nome = input("Nome: ")
                autor = input("Autor: ")
                quantidade = int(input("Quantidade: "))

                try:
                    livros.buscar_por_id(id)
                    print(" ID já existente!")
                except EntidadeNaoEncontradaException:
                    livros.inserir(Livro(id, nome, autor, quantidade))
                    print(" Livro inserido com sucesso!")

            elif opcao == "2":
                id = int(input("ID do livro a alterar: "))

                try:
                    livro = livros.buscar_por_id(id)
                    nome = input("Novo nome: ")
                    autor = input("Novo autor: ")
                    quantidade = int(input("Quantidade: "))
                    livros.alterar(Livro(id, nome, autor, quantidade))
                    print(" Livro alterado!")
                except EntidadeNaoEncontradaException:
                    print(" Livro não encontrado.")

            elif opcao == "3":
                id = int(input("ID do livro a remover: "))
                if livros.excluir(id):
                    print(" Livro removido.")
                else:
                    print(" Livro não encontrado.")

            elif opcao == "4":
                id = int(input("ID do livro: "))
                try:
                    livro = livros.buscar_por_id(id)
                    print(livro)
                except EntidadeNaoEncontradaException:
                    print(" Livro não encontrado.")

            elif opcao == "5":
                print("\n Todos os livros:")
                print(livros)

            elif opcao == "0":
                break
            else:
                print(" Opção inválida!")

    def menu_emprestimos(self):
        while True:
            print("\n -----------MENU EMPRÉSTIMOS-----------")
            print("1 - Inserir Empréstimo")
            print("2 - Alterar Empréstimo")
            print("3 - Apagar Empréstimo")
            print("4 - Visualizar Empréstimo por ID")
            print("5 - Visualizar Todos os Empréstimos")
            print("0 - Voltar")
            opcao = input("Escolha uma opção: ")

            emprestimos = self.bd.get_emprestimos()

            if opcao == "1":
                self.inserir_emprestimo()

            elif opcao == "2":
                self.alterar_emprestimo()

            elif opcao == "3":
                id = int(input("ID do empréstimo a remover: "))

                try:
                    emprestimo = emprestimos.buscar_por_id(id)
                except EntidadeNaoEncontradaException:
                    print(" Empréstimo não encontrado.")
                    continue

                for item in emprestimo.itens:
                    livro = self.bd.get_livros().buscar_por_id(item.livro.id)
                    livro.quantidade += item.quantidade

                emprestimos.excluir(id)
                print(" Empréstimo removido e livros devolvidos ao estoque.")

            elif opcao == "4":
                id = int(input("ID do empréstimo: "))
                try:
                    emp = emprestimos.buscar_por_id(id)
                    print(emp)
                except EntidadeNaoEncontradaException:
                    print(" Empréstimo não encontrado.")

            elif opcao == "5":
                print("\n* Todos os empréstimos:")
                print(emprestimos)

            elif opcao == "0":
                break
            else:
                print(" Opção inválida!")

    def inserir_emprestimo(self):
        id = int(input("ID do empréstimo: "))
        cliente = input("Nome do cliente: ")

        emprestimo = Emprestimo(id, cliente)

        while True:
            print("\n Adicionar Itens ao Empréstimo")
            print("1 - Adicionar Livro")
            print("0 - Finalizar")
            op = input("Escolha: ")
            if op == "1":
                id_livro = int(input("ID do livro: "))
                qtd = 1

                try:
                    livro = self.bd.get_livros().buscar_por_id(id_livro)
                except EntidadeNaoEncontradaException:
                    print(" Livro inválido!")
                    continue

                if qtd <= 0:
                    print(" Quantidade inválida!")
                    continue
                if livro.quantidade >= qtd:
                    livro.quantidade -= qtd
                    item = ItemEmprestimo(len(emprestimo.itens) + 1, livro, qtd)
                    emprestimo.adicionar_item(item)
                    print(f" Item adicionado! Estoque restante: {livro.quantidade}")
                else:
                    print(f" Estoque insuficiente! Disponível: {livro.quantidade}")

            elif op == "0":
                break

        self.bd.get_emprestimos().inserir(emprestimo)
        print(" Empréstimo cadastrado com sucesso!")

    def alterar_emprestimo(self):
        id = int(input("ID do empréstimo a alterar: "))

        try:
            emprestimo = self.bd.get_emprestimos().buscar_por_id(id)
        except EntidadeNaoEncontradaException:
            print(" Empréstimo não encontrado!")
            return

        while True:
            print("\n Alterar Itens do Empréstimo")
            print("1 - Adicionar Livro")
            print("2 - Remover Item")
            print("0 - Finalizar")
            op = input("Escolha: ")

            if op == "1":
                id_livro = int(input("ID do livro: "))
                try:
                    livro = self.bd.get_livros().buscar_por_id(id_livro)
                except EntidadeNaoEncontradaException:
                    print(" Livro não encontrado!")
                    continue

                qtd = int(input("Quantidade: "))
                item = ItemEmprestimo(len(emprestimo.itens) + 1, livro, qtd)
                emprestimo.adicionar_item(item)
                print(" Item adicionado!")

            elif op == "2":
                if not emprestimo.itens:
                    print(" Nenhum item para remover.")
                    continue

                for i, item in enumerate(emprestimo.itens):
                    print(f"{i + 1} - {item}")

                idx = int(input("Número do item a remover: ")) - 1

                if 0 <= idx < len(emprestimo.itens):
                    item_removido = emprestimo.itens.pop(idx)

                    livro_original = self.bd.get_livros().buscar_por_id(item_removido.livro.id)
                    livro_original.quantidade += item_removido.quantidade
                    print(f" Item removido. Estoque atualizado: {livro_original.quantidade}")
                else:
                    print(" Índice inválido.")

            elif op == "0":
                break

        self.bd.get_emprestimos().alterar(emprestimo)
        print(" Empréstimo atualizado com sucesso!")
