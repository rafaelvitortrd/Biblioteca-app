from modelo.entidade import Entidade

class Livro(Entidade):
    def __init__(self, id, nome, autor, quantidade):
        super().__init__(id)
        self.nome = nome
        self.autor = autor
        self.quantidade = int(quantidade)

    def __str__(self):
        return f"{super().__str__()}\tNome: {self.nome}\tAutor: {self.autor}\tQuantidade: {self.quantidade}"
