from modelo.entidade import Entidade

class Usuario(Entidade):

  def __init__(self, nome):
    super().__init__(id)
    self.nome = nome

  def __str__(self):
    return f"{self.nome}"