from modelo.entidade import Entidade

class Funcionario(Entidade):
    def __init__(self, id, nome, login, senha):
        super().__init__(id)
        self.nome = nome
        self.login = login
        self.senha = senha

    def __str__(self):
        return f"ID: {self.id} | Nome: {self.nome} | Login: {self.login}"
