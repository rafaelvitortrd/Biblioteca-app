from modelo.entidade import Entidade

class ItemEmprestimo(Entidade):

    def __init__(self, id, livro, quantidade=1):
        super().__init__(id)
        self.livro = livro
        self.idLivro = livro.id
        self.quantidade = quantidade

    def __str__(self):
        return f"ID Item: {self.idLivro}\tLivro: {self.livro.nome}\tAutor: {self.livro.autor}\tQuantidade: {self.quantidade} \n"
