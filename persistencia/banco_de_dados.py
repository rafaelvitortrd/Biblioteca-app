from persistencia.persistente import Persistente


class BancoDados:
    def __init__(self):
        self._livros = Persistente()
        self._emprestimos = Persistente()
        self._itens_emprestimo = Persistente()
        self._funcionarios = Persistente()

    def get_livros(self):
        return self._livros

    def get_emprestimos(self):
        return self._emprestimos

    def get_itens_emprestimo(self):
        return self._itens_emprestimo

    def get_funcionarios(self):
        return self._funcionarios
