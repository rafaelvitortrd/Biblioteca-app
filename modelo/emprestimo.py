from modelo.entidade import Entidade
from datetime import date, timedelta

class Emprestimo(Entidade):

    def __init__(self, id, cliente, data_emprestimo=None, data_devolucao=None):
        super().__init__(id)
        self.cliente = cliente
        self.data_emprestimo = data_emprestimo if data_emprestimo else date.today()
        self.data_devolucao = self.data_emprestimo + timedelta(days=30)
        self.itens = []

    def adicionar_item(self, item):
        self.itens.append(item)

    def remover_item(self, item):
        self.itens.remove(item)

    def __str__(self):
        itens_str = "\n".join([str(item) for item in self.itens]) if self.itens else "Nenhum item"
        return (f"Empréstimo ID: {self.id}\n"
                f"Cliente: {self.cliente}\n"
                f"Data Empréstimo: {self.data_emprestimo}\n"
                f"Data Devolução: {self.data_devolucao}\n"
                f"Itens:\n{itens_str}")
