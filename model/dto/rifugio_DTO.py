from dataclasses import dataclass

@dataclass
class RifugioDTO:
    id : int
    nome: str
    localita: str
    altitudine: int
    capienza: int
    aperto: int

    def __str__(self):
        return f'[{str(self.id)}] - {self.nome} - {self.localita}'

    def __hash__(self):
        return hash(self.id)

    def __lt__(self, other):
        return self.id < other.id