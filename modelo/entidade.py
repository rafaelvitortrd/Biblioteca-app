from abc import ABC, abstractmethod

class Entidade(ABC):
  def __init__(self, id):
    self.id = id

  def __str__(self):
    return f"ID: {self.id}"

