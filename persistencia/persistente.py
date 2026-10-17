from typing import Generic, TypeVar, List
from modelo.entidade import Entidade

T = TypeVar("T", bound="Entidade")


class Persistente(Generic[T]):
    def __init__(self):
        self.lista_entidades: List[T] = []

    def inserir(self, entidade: T) -> bool:
        for e in self.lista_entidades:
            if e.id == entidade.id:
                return False
        self.lista_entidades.append(entidade)
        return True

    def alterar(self, entidade: T) -> bool:
        for i, e in enumerate(self.lista_entidades):
            if e.id == entidade.id:
                self.lista_entidades[i] = entidade
                return True
        return False

    def excluir(self, id: int) -> bool:
        for e in self.lista_entidades:
            if e.id == id:
                self.lista_entidades.remove(e)
                return True
        return False

    def buscar_por_id(self, id: int) -> T:
        for e in self.lista_entidades:
            if e.id == id:
                return e
        raise EntidadeNaoEncontradaException(id)

    def buscar(self, id: int) -> T | None:
        try:
            return self.buscar_por_id(id)
        except EntidadeNaoEncontradaException:
            return None

    def __str__(self) -> str:
        if not self.lista_entidades:
            return "Nenhuma entidade armazenada."
        return "\n".join(str(e) for e in self.lista_entidades)


class EntidadeNaoEncontradaException(Exception):
    def __init__(self, id: int):
        super().__init__(f"Entidade com id {id} não encontrada.")
