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
        # --- 1. NOVO: Estado de defesa ---
        self.em_defesa = False 


    def receber_dano(self, quantidade: int) -> bool:
        """
        Aplica o dano, considera a defesa e retorna True se morreu.
        """

        if self.em_defesa:
            print(f" {self.nome} BLOQUEOU o dano completamente!")
            quantidade = 0 
            self.em_defesa = False 
        self.vida -= quantidade
        if self.vida < 0:
            self.vida = 0
        return self.vida <= 0 

    def esta_vivo(self) -> bool:
        return self.vida > 0

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
        self.em_defesa = False # Se atacar, baixa a guarda
        dano = random.randint(8, 23)
        efeito = "NENHUM"
        if dano >= 20: 
            efeito = "stun-guerreiro"
        return (dano, f"{self.nome} ataca com espada!", efeito)

    def defender(self) -> Tuple[int, str, str]:
        self.em_defesa = True # --- ATIVA A DEFESA ---
        self.carga_especial += 1
        return (0, f"{self.nome} levanta o escudo! (Carga: {self.carga_especial}/2)", "NENHUM")

    def especial(self) -> Tuple[int, str, str]:
        self.em_defesa = False # Se atacar, baixa a guarda
        if self.carga_especial < 2:
            return (0, f"{self.nome} falhou: Carga insuficiente.", "NENHUM")
        
        self.carga_especial = 0 
        dano = random.randint(35, 50)
        return (dano, f"{self.nome} realiza um GOLPE ESMAGADOR!", "NENHUM")

class Mago(Personagem):
    def atacar(self) -> Tuple[int, str, str]:
        self.em_defesa = False
        dano = random.randint(10, 25)
        efeito = "NENHUM"
        if dano > 20:
            efeito = "queimado-mago"
        self.carga_especial += 1
        return (dano, f"{self.nome} lança raio de fogo! (Carga: {self.carga_especial}/4)", efeito)

    def defender(self) -> Tuple[int, str, str]:
        self.em_defesa = True # --- ATIVA A DEFESA ---
        return (0, f"{self.nome} cria uma barreira mágica!", "NENHUM")

    def especial(self) -> Tuple[int, str, str]:
        self.em_defesa = False
        if self.carga_especial < 4:
            return (0, f"{self.nome} falhou: Carga insuficiente.", "NENHUM")
        
        self.carga_especial = 0
        dano = random.randint(30, 60)
        return (dano, f"{self.nome} invoca uma METEORO DE FOGO!", "queimado-mago")

class Arqueiro(Personagem):
    def atacar(self) -> Tuple[int, str, str]:
        self.em_defesa = False
        dano = random.randint(10, 20)
        efeito = "NENHUM"
        if dano < 15:
            efeito = "marcado-arqueiro"
        self.carga_especial += 1 
        return (dano, f"{self.nome} dispara uma flecha! (Carga: {self.carga_especial}/3)", efeito)

    def defender(self) -> Tuple[int, str, str]:
        self.em_defesa = True 
        self.carga_especial += 1
        return (0, f"{self.nome} esquiva agilmente! (Carga: {self.carga_especial}/3)", "NENHUM")

    def especial(self) -> Tuple[int, str, str]:
        self.em_defesa = False
        if self.carga_especial < 3:
            return (0, f"{self.nome} falhou: Carga insuficiente.", "NENHUM")
        
        self.carga_especial = 0 
        dano = random.randint(25, 40)
        return (dano, f"{self.nome} dispara uma CHUVA DE FLECHAS!", "NENHUM")

class Inimigo(Personagem):
    def atacar(self) -> Tuple[int, str, str]:
        self.em_defesa = False
        dano = random.randint(5, 25)
        return (dano, f"{self.nome} ataca ferozmente!", "NENHUM")

    def defender(self) -> Tuple[int, str, str]:
        self.em_defesa = True 
        return (0, f"{self.nome} se prepara para o impacto!", "NENHUM")

    def especial(self) -> Tuple[int, str, str]:
        self.em_defesa = False
        dano = random.randint(15, 25)
        return (dano, f"{self.nome} usa um ataque sombrio!", "NENHUM")


    def inteligencia_artificial(self):
        acoes = ["atacar"] * 60 + ["defender"] * 30 + ["especial"] * 10
        escolha = random.choice(acoes)
        
        if escolha == "atacar":
            return "atacar", self.atacar()
        elif escolha == "especial":
            return "especial", self.especial()
        else: 
            return "defender", self.defender()