import unittest
from persistencia.persistente import Persistente, EntidadeNaoEncontradaException
from modelo.entidade import Entidade


class TestePersistente(unittest.TestCase):

    def setUp(self):
        self.p = Persistente()

    def teste_inserir_id_novo(self):
        e = Entidade(1)
        resultado = self.p.inserir(e)
        self.assertTrue(resultado)
        self.assertEqual(self.p.buscar(1).id, 1)

    def teste_inserir_id_existente(self):
        e1 = Entidade(1)
        e2 = Entidade(1)
        self.p.inserir(e1)
        resultado = self.p.inserir(e2)
        self.assertFalse(resultado)

    def teste_alterar_id_inexistente(self):
        e = Entidade(1)
        resultado = self.p.alterar(e)
        self.assertFalse(resultado)

    def teste_alterar_id_existente(self):
        e1 = Entidade(1)
        e2 = Entidade(1)
        self.p.inserir(e1)
        resultado = self.p.alterar(e2)
        self.assertTrue(resultado)

    def teste_excluir_id_existente(self):
        e = Entidade(1)
        self.p.inserir(e)
        resultado = self.p.excluir(1)
        self.assertTrue(resultado)
        self.assertIsNone(self.p.buscar(1))

    def teste_excluir_id_inexistente(self):
        resultado = self.p.excluir(999)
        self.assertFalse(resultado)


    def teste_buscar_id_existente(self):
        e = Entidade(1)
        self.p.inserir(e)
        encontrado = self.p.buscar(1)
        self.assertIsNotNone(encontrado)
        self.assertEqual(encontrado.id, 1)

    def teste_buscar_id_inexistente(self):
        encontrado = self.p.buscar(123)
        self.assertIsNone(encontrado)


if __name__ == "__main__":
    unittest.main()
