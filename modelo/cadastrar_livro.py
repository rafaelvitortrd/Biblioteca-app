from modelo.livro import Livro

class CadastrarLivro(Livro):
    def __init__(self):
        self.livros = []

    def cadastrar(self, id, nome, autor, quantidade):
        livro = Livro(id, nome, autor, quantidade)
        self.livros.append(livro)
        print(f"Livro '{nome}' cadastrado com sucesso!")

    def listar(self):
        if not self.livros:
            print("Nenhum livro cadastrado ainda.")
            return
        for livro in self.livros:
            alerta = " Esgotado!" if livro.quantidade == 0 else ""
            print(f"{livro} {alerta}")

    def buscar_por_id(self, id):
        for livro in self.livros:
            if livro.id == id:
                return livro
        return None

    def remover(self, id):
        if livro:
            if livro.quantidade > 0:
                livro.quantidade -= 1
                print(f" Livro '{livro.nome}' foi removido do estoque.")
                if livro.quantidade == 0:
                    print(f" O livro '{livro.nome}' está esgotado!")
        else:
            print(" Livro não encontrado.")
