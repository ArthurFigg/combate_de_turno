# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from abc import ABC, abstractmethod
import random
from typing import Tuple 

class Personagem(ABC):
    def __init__(self, nome: str, nivel: int, vida: int):
        self.nome = nome
        self.nivel = nivel
        self.vida = vida
        self.carga_especial = 0  


    
    @abstractmethod
    def atacar(self) -> Tuple[int, str, str]:
        pass

    @abstractmethod
    def defender(self) -> Tuple[int, str, str]:
        pass

    @abstractmethod
    def especial(self) -> Tuple[int, str, str]:
        pass

class Guerreiro(Personagem):
    def atacar(self) -> Tuple[int, str, str]:
        dano = random.randint(8, 23)
        efeito = "NENHUM"
        # Regra: Dano alto atordoa
        if dano >= 20: 
            efeito = "stun-guerreiro"
        
        return (dano, f"{self.nome} ataca com espada!", efeito)

    def defender(self) -> Tuple[int, str, str]:
        self.carga_especial += 1

        return (0, f"{self.nome} levanta o escudo! (Carga: {self.carga_especial}/2)", "NENHUM")

    def especial(self) -> Tuple[int, str, str]:
        if self.carga_especial < 2:
            return (0, f"{self.nome} falhou: Carga insuficiente.", "NENHUM")
        
        self.carga_especial = 0 
        dano = random.randint(35, 50)
        return (dano, f"{self.nome} realiza um GOLPE ESMAGADOR!", "NENHUM")

class Mago(Personagem):
    def atacar(self) -> Tuple[int, str, str]:
        dano = random.randint(10, 25)
        efeito = "NENHUM"
        # Regra: Dano alto queima
        if dano > 20:
            efeito = "queimado-mago"
        
        self.carga_especial += 1
        return (dano, f"{self.nome} lança raio de fogo! (Carga: {self.carga_especial}/4)", efeito)

    def defender(self) -> Tuple[int, str, str]:
        return (0, f"{self.nome} cria uma barreira mágica!", "NENHUM")

    def especial(self) -> Tuple[int, str, str]:
        if self.carga_especial < 4:
            return (0, f"{self.nome} falhou: Carga insuficiente.", "NENHUM")
        
        self.carga_especial = 0
        dano = random.randint(30, 60) # Mago tem dano explosivo maior
        return (dano, f"{self.nome} invoca uma METEORO DE FOGO!", "QUEIMADO") # Especial sempre queima? (Opcional)

class Arqueiro(Personagem):
    def atacar(self) -> Tuple[int, str, str]:
        dano = random.randint(10, 20)
        efeito = "NENHUM"
        # Regra: Dano BAIXO marca o alvo (Corrigido para < 15)
        if dano < 15:
            efeito = "marcado-arqueiro"
        
        self.carga_especial += 1 
        return (dano, f"{self.nome} dispara uma flecha! (Carga: {self.carga_especial}/3)", efeito)

    def defender(self) -> Tuple[int, str, str]:
        self.carga_especial += 1
        return (0, f"{self.nome} esquiva agilmente! (Carga: {self.carga_especial}/3)", "NENHUM")

    def especial(self) -> Tuple[int, str, str]:
        if self.carga_especial < 3:
            return (0, f"{self.nome} falhou: Carga insuficiente.", "NENHUM")
        
        self.carga_especial = 0 
        dano = random.randint(25, 40)

        return (dano, f"{self.nome} dispara uma CHUVA DE FLECHAS!", "NENHUM")

class Inimigo(Personagem):

    def atacar(self) -> Tuple[int, str, str]:
        dano = random.randint(5, 25)
        return (dano, f"{self.nome} ataca ferozmente!", "NENHUM")

    def defender(self) -> Tuple[int, str, str]:
        return (0, f"{self.nome} se prepara para o impacto!", "NENHUM")

    def especial(self) -> Tuple[int, str, str]:
        dano = random.randint(15, 25)
        return (dano, f"{self.nome} usa um ataque sombrio!", "NENHUM")
    

