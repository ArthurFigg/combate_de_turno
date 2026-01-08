# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from abc import ABC, abstractmethod

class Personagem(ABC):
    def __init__(self, nome: str, nivel: int, vida: int):
        self.nome = nome
        self.nivel = nivel
        self.vida = vida
        self.carga_especial = 0  

    @abstractmethod
    def atacar(self) -> str:
        pass

    @abstractmethod
    def defender(self) -> str:
        pass

    @abstractmethod
    def especial(self) -> str:
        pass

class Guerreiro(Personagem):
    def atacar(self) -> str:
        return f"{self.nome} ataca com uma espada!"

    def defender(self) -> str:
        self.carga_especial += 1
        return f"{self.nome} bloqueia o ataque com um escudo! (Carga: {self.carga_especial}/2)"

    def especial(self) -> str:
        if self.carga_especial < 2:
            return f"{self.nome} falhou: Carga insuficiente ({self.carga_especial}/2)."
        
        self.carga_especial = 0 
        return f"{self.nome} realiza um golpe poderoso!"

class Mago(Personagem):
    def atacar(self) -> str:
        self.carga_especial += 1
        return f"{self.nome} lança um raio de fogo! (Carga: {self.carga_especial}/4)"

    def defender(self) -> str:
        return f"{self.nome} cria uma barreira mágica!"

    def especial(self) -> str:
        if self.carga_especial < 4:
            return f"{self.nome} falhou: Carga insuficiente ({self.carga_especial}/4)."
        
        self.carga_especial = 0
        return f"{self.nome} invoca uma enorme bola de fogo!"

class Arqueiro(Personagem):
    def atacar(self) -> str:
        self.carga_especial += 1 
        return f"{self.nome} dispara uma flecha certeira! (Carga: {self.carga_especial}/3)"

    def defender(self) -> str:
        self.carga_especial += 1
        return f"{self.nome} esquiva agilmente! (Carga: {self.carga_especial}/3)"

    def especial(self) -> str:
        if self.carga_especial < 3:
            return f"{self.nome} falhou: Carga insuficiente ({self.carga_especial}/3)."
        
        self.carga_especial = 0 
        return f"{self.nome} dispara uma chuva de flechas!"
    

class Inimigo(Personagem):
    def atacar(self) -> str:
        return f"{self.nome} ataca ferozmente!"

    def defender(self) -> str:
        return f"{self.nome} resiste ao ataque!"

    def especial(self) -> str:
        return f"{self.nome} usa um ataque especial devastador!"