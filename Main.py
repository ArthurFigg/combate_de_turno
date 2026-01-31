 # pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
import random
from personagem import Guerreiro, Mago, Arqueiro, Inimigo

class BattleEngine:
    def __init__(self, heroi, inimigo):
        self.heroi = heroi
        self.inimigo = inimigo
        
        
        self.status = {
            "stun-guerreiro": False,
            "queimado-mago": False,
            "marcado-arqueiro": False
        }

    def turno_jogador(self):
        print(f"\n-- Turno de {self.heroi.nome} --")
        acao = input("Escolha uma ação: 1) Atacar 2) Defender 3) Especial\n>> ")
        
        dano = 0
        texto = ""
        efeito = "NENHUM"

        if acao == "1":
            dano, texto, efeito = self.heroi.atacar()
        elif acao == "2":
            dano, texto, efeito = self.heroi.defender()
        elif acao == "3":
            dano, texto, efeito = self.heroi.especial()
        else:
            print(" Ação inválida! Perdeu o turno.")
            return

       
        print(texto)
        
        
        if dano > 0:
            self.inimigo.vida -= dano
            print(f" O Inimigo perdeu {dano} HP!")

        
        if efeito != "NENHUM":
            self.status[efeito] = True
            print(f">>> Efeito aplicado no inimigo: {efeito.upper()}")

    def turno_inimigo(self):
        print(f"\n-- Turno de {self.inimigo.nome} --")
        
        
        if self.status["stun-guerreiro"]:
            print(f" {self.inimigo.nome} está ATORDOADO e perdeu a vez!")
            self.status["stun-guerreiro"] = False # Reseta o stun
            return 

       
        
        acoes_possiveis = ["Ataque"] * 6 + ["Defesa"] * 3 + ["Especial"] * 2
        sorteio = random.choice(acoes_possiveis)
        
        dano = 0
        texto = ""
        efeito = "NENHUM"

        if sorteio == "Ataque":
            dano, texto, efeito = self.inimigo.atacar()
        elif sorteio == "Defesa":
            dano, texto, efeito = self.inimigo.defender()
        elif sorteio == "Especial":
            dano, texto, efeito = self.inimigo.especial()
        
        print(texto)
        
       
        if dano > 0:
            self.heroi.vida -= dano
            print(f" VOCÊ sofreu -{dano} HP!")

    def verificar_status(self):
        
        
        
        if self.status["queimado-mago"]:
            dano_queimado = 5
            self.inimigo.vida -= dano_queimado
            print(f"🔥 {self.inimigo.nome} sofre {dano_queimado} de dano por queimadura!")

        
        if self.status["marcado-arqueiro"]:
            dano_marcado = 7
            self.inimigo.vida -= dano_marcado
            print(f"🎯 {self.inimigo.nome} sofre {dano_marcado} de dano extra por estar marcado!")

    def iniciar_batalha(self):
        print(f"⚔️ Uma batalha começa entre {self.heroi.nome} e {self.inimigo.nome}!")
        
        while self.heroi.vida > 0 and self.inimigo.vida > 0:
            
            
            print(f"\n📊 HP {self.heroi.nome}: {self.heroi.vida} | HP {self.inimigo.nome}: {self.inimigo.vida}")
            
            
            self.turno_jogador()
            
           
            if self.inimigo.vida <= 0:
                print(f"\n🏆 {self.inimigo.nome} foi derrotado! VITÓRIA!")
                break
            
            
            self.verificar_status()
            
            
            if self.inimigo.vida <= 0:
                print(f"\n🏆 {self.inimigo.nome} morreu pelos efeitos! VITÓRIA!")
                break

            
            self.turno_inimigo()
            
            
            if self.heroi.vida <= 0:
                print(f"\n💀 {self.heroi.nome} foi derrotado... GAME OVER.")
                break
        
        print("--- Batalha encerrada ---")

# --- EXECUÇÃO DO JOGO ---
if __name__ == "__main__":
    print("=== RPG DE TURNOS PYTHON ===")
    print("Escolha sua classe:")
    print("1. Guerreiro (Tank - 150 HP)")
    print("2. Mago (Dano/Fogo - 80 HP)")
    print("3. Arqueiro (Crítico/Marca - 110 HP)")
    
    escolha = input(">> ")
    
    heroi = None
    
   
    if escolha == "1":
        heroi = Guerreiro("Arthur", 1, 150)
    elif escolha == "2":
        heroi = Mago("Merlin", 1, 80)
    elif escolha == "3":
        heroi = Arqueiro("Legolas", 1, 110)
    else:
        
        heroi = Guerreiro("Aventureiro", 1, 120)

    
    monstro = Inimigo("Orc", 1, 120)
    
    
    engine = BattleEngine(heroi, monstro)
    engine.iniciar_batalha()
    escolha = input(">> ")
    
    heroi = None
    if escolha == "1":
        heroi = Guerreiro("Arthur", 1, 120)
    elif escolha == "2":
        heroi = Mago("Merlin", 1, 80)
    elif escolha == "3":
        heroi = Arqueiro("Legolas", 1, 100)
    else:
        heroi = Guerreiro("Testador", 1, 100)

    monstro = Inimigo("Orc", 1, 100)
    
    engine = BattleEngine(heroi, monstro)
    engine.iniciar_batalha()