import datetime
from dataclasses import dataclass

'''
    DTO (Data Transfer Object) dell'entità Prezzo
'''


@dataclass()
class Prezzo:
    data: datetime.date
    prezzo_litro: float
    id_distributore: int

    def __eq__(self, other):
        return isinstance(other, Prezzo) and self.data == other.data and self.id_distributore == other.id_distributore

    def __str__(self):
        return f"{self.data} | Prezzo: {self.prezzo_litro} €/litro | Distributore: {self.id_distributore}"

    def __repr__(self):
        return f"{self.data} | Prezzo: {self.prezzo_litro} €/litro | Distributore: {self.id_distributore}"
