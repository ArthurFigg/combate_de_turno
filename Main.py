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
        acao = input("Escolha uma ação: 1) Atacar 2) Defender 3) Especial\n")
        
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
            print("Ação inválida! Perdeu o turno.")
            return

        
        print(texto)
        if dano > 0:
            self.inimigo.vida -= dano

        
        if efeito != "NENHUM":
            self.status[efeito] = True
            print(f">>> Efeito aplicado: {efeito}")

    def turno_inimigo(self):
        print(f"\n-- Turno de {self.inimigo.nome} --")
        
        
        if self.status["stun-guerreiro"]:
            print(f" {self.inimigo.nome} está ATORDOADO e perdeu a vez!")
            self.status["stun-guerreiro"] = False 
            return 

       
        dano, texto, efeito = self.inimigo.atacar()
        print(texto)
        
        
        if efeito != "NENHUM":
            pass 
            
        self.heroi.vida -= dano

    def verificar_status(self):
        """Aplica danos passivos no INIMIGO"""
        
        
        if self.status["queimado-mago"]:
            dano_queimado = 5
            self.inimigo.vida -= dano_queimado
            print(f"{self.inimigo.nome} sofre {dano_queimado} de dano por queimadura!")
           

        if self.status["marcado-arqueiro"]:
            dano_marcado = 7
            self.inimigo.vida -= dano_marcado
            print(f" {self.inimigo.nome} sofre {dano_marcado} de dano extra por estar marcado!")

    def iniciar_batalha(self):
        print(f" Uma batalha começa entre {self.heroi.nome} e {self.inimigo.nome}!")
        
        while self.heroi.vida > 0 and self.inimigo.vida > 0:
           
            print(f"\nHP {self.heroi.nome}: {self.heroi.vida} | HP {self.inimigo.nome}: {self.inimigo.vida}")
            
            
            self.turno_jogador()
            
            
            if self.inimigo.vida <= 0:
                print(f"\n {self.inimigo.nome} foi derrotado! VITÓRIA!")
                break
            
            
            self.verificar_status()
            
            
            if self.inimigo.vida <= 0:
                print(f"\n {self.inimigo.nome} morreu pelos efeitos! VITÓRIA!")
                break

            # Turno Inimigo
            self.turno_inimigo()
            
            if self.heroi.vida <= 0:
                print(f"\n {self.heroi.nome} foi derrotado... GAME OVER.")
                break
        
        print("Batalha encerrada.")


if __name__ == "__main__":
   
    print("Escolha seu herói: 1-Guerreiro, 2-Mago, 3-Arqueiro")
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