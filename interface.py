import sys
import os
import pygame
from personagem import Guerreiro, Mago, Arqueiro, Inimigo

LARGURA = 800
ALTURA = 600
TITULO = "RPG Final - Python Portfolio"
FPS = 60
ALTURA_CHAO = 480 

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (200, 0, 0)
VERDE = (0, 200, 0)
AZUL = (0, 0, 200)
CINZA = (50, 50, 50)
CINZA_CLARO = (100, 100, 100)
AMARELO = (255, 215, 0)

MENU = 0
TURNO_JOGADOR = 1
TURNO_INIMIGO = 2
FIM_DE_JOGO = 3
PROCESSANDO = 4

class SpriteCompleto(pygame.sprite.Sprite):
    def __init__(self, animacoes_dict, escala=1, flip=False, pos_x=0, pos_y=0):
        super().__init__()
        self.animacoes = {}
        self.flip = flip
        self.escala = escala
        self.pos_x = pos_x 
        self.pos_y = pos_y 
        
        for nome_acao, dados in animacoes_dict.items():
            self.carregar_tira(nome_acao, dados['path'], dados['frames'])

        self.estado_atual = 'idle'
        self.frame_atual = 0
        
        if 'idle' in self.animacoes:
            self.image = self.animacoes['idle'][0]
        else:
            self.image = list(self.animacoes.values())[0][0]
             
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.pos_x, self.pos_y)
        
        self.cronometro = 0
        self.velocidade = 0.20
        self.em_acao = False 

    def carregar_tira(self, nome, caminho, frames):
        try:
            sheet = pygame.image.load(caminho).convert_alpha()
            largura_tira = sheet.get_width()
            altura_tira = sheet.get_height()
            largura_quadro = largura_tira / frames
            
            lista_imgs = []
            for i in range(frames):
                corte = (i * largura_quadro, 0, largura_quadro, altura_tira)
                quadro = sheet.subsurface(corte)
                
                if self.escala != 1:
                    novo_tam = (int(largura_quadro * self.escala), int(altura_tira * self.escala))
                    quadro = pygame.transform.scale(quadro, novo_tam)
                
                if self.flip:
                    quadro = pygame.transform.flip(quadro, True, False)
                
                lista_imgs.append(quadro)
            
            self.animacoes[nome] = lista_imgs
        except FileNotFoundError:
            print(f"AVISO: Imagem não encontrada: {caminho}")
            erro_surf = pygame.Surface((50, 50))
            erro_surf.fill((255, 0, 255))
            self.animacoes[nome] = [erro_surf] * frames

    def animar_ataque_normal(self):
        if 'attack' in self.animacoes:
            self.em_acao = True
            self.estado_atual = 'attack'
            self.frame_atual = 0

    def animar_especial(self):
        if 'special' in self.animacoes:
            self.em_acao = True
            self.estado_atual = 'special'
            self.frame_atual = 0
        else:
            self.animar_ataque_normal()

    def animar_defesa(self):
        if 'defend' in self.animacoes:
            self.em_acao = True
            self.estado_atual = 'defend'
            self.frame_atual = 0

    def animar_dano(self):
        if 'hurt' in self.animacoes:
            self.em_acao = True
            self.estado_atual = 'hurt'
            self.frame_atual = 0

    def update(self):
        self.cronometro += self.velocidade
        if self.cronometro >= 1:
            self.cronometro = 0
            self.frame_atual += 1
            
            lista_atual = self.animacoes[self.estado_atual]
            
            if self.frame_atual >= len(lista_atual):
                if self.em_acao:
                    self.em_acao = False
                    self.estado_atual = 'idle'
                    self.frame_atual = 0
                else:
                    self.frame_atual = 0 
            
            self.image = self.animacoes[self.estado_atual][self.frame_atual]
            self.rect = self.image.get_rect()
            self.rect.midbottom = (self.pos_x, self.pos_y)

class JogoRPG:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption(TITULO)
        self.relogio = pygame.time.Clock()
        self.fonte = pygame.font.SysFont("Arial", 20, bold=True)
        self.fonte_grande = pygame.font.SysFont("Arial", 40, bold=True)

        self.estado_jogo = MENU
        
        self.heroi = None
        self.inimigo = None
        self.sprite_heroi = None
        self.sprite_inimigo = None
        self.grupo_sprites = None
        self.max_vida_heroi = 0
        self.max_vida_inimigo = 0
        self.status = {}
        self.log_combate = ""
        self.timer_turno = 0
        
        self.btn_guerreiro = pygame.Rect(100, 250, 180, 200)
        self.btn_mago = pygame.Rect(310, 250, 180, 200)
        self.btn_arqueiro = pygame.Rect(520, 250, 180, 200)

        y_btns = 520
        self.btn_atacar = pygame.Rect(50, y_btns, 200, 50)
        self.btn_defender = pygame.Rect(275, y_btns, 200, 50)
        self.btn_especial = pygame.Rect(500, y_btns, 200, 50)

    def iniciar_batalha(self, classe_escolhida):
        escala_padrao = 3.5 
        escala_mago = 2.5 
        
        pasta = ""
        escala_final = 1
        anim_dict = {}

        if classe_escolhida == "guerreiro":
            self.heroi = Guerreiro("Arthur", 1, 150)
            pasta = "warrior"
            escala_final = escala_padrao
            anim_dict = {
                'idle':    {'path': os.path.join("img", pasta, "Idle.png"), 'frames': 8},
                'attack':  {'path': os.path.join("img", pasta, "Attack1.png"), 'frames': 4},
                'special': {'path': os.path.join("img", pasta, "Attack2.png"), 'frames': 4}, 
                'hurt':    {'path': os.path.join("img", pasta, "Take Hit.png"), 'frames': 3}, 
                'defend':  {'path': os.path.join("img", pasta, "Idle.png"), 'frames': 8}
            }

        elif classe_escolhida == "mago":
            self.heroi = Mago("Merlin", 1, 80)
            pasta = "mage"
            escala_final = escala_mago
            anim_dict = {
                'idle':    {'path': os.path.join("img", pasta, "Idle.png"), 'frames': 6},
                'attack':  {'path': os.path.join("img", pasta, "Attack1.png"), 'frames': 8},
                'special': {'path': os.path.join("img", pasta, "Attack2.png"), 'frames': 8}, 
                'hurt':    {'path': os.path.join("img", pasta, "Hit.png"), 'frames': 4},
                'defend':  {'path': os.path.join("img", pasta, "Idle.png"), 'frames': 6}
            }

        else: 
            self.heroi = Arqueiro("Legolas", 1, 110)
            pasta = "archer"
            escala_final = escala_padrao
            anim_dict = {
                'idle':    {'path': os.path.join("img", pasta, "spr_ArcherIdle_strip_NoBkg.png"), 'frames': 8},
                'attack':  {'path': os.path.join("img", pasta, "spr_ArcherAttack_strip_NoBkg.png"), 'frames': 8},
                'special': {'path': os.path.join("img", pasta, "spr_ArcherMelee_strip_NoBkg.png"), 'frames': 8},
                'hurt':    {'path': os.path.join("img", pasta, "spr_ArcherIdle_strip_NoBkg.png"), 'frames': 8},
                'defend':  {'path': os.path.join("img", pasta, "spr_ArcherIdle_strip_NoBkg.png"), 'frames': 8}
            }

        self.inimigo = Inimigo("Esqueleto", 1, 120)
        anim_dict_ini = {
            'idle':    {'path': os.path.join("img", "skeleton", "Idle.png"), 'frames': 4},
            'attack':  {'path': os.path.join("img", "skeleton", "Attack.png"), 'frames': 8},
            'special': {'path': os.path.join("img", "skeleton", "Attack.png"), 'frames': 8},
            'hurt':    {'path': os.path.join("img", "skeleton", "Take Hit.png"), 'frames': 4},
            'defend':  {'path': os.path.join("img", "skeleton", "Shield.png"), 'frames': 4}
        }

        self.sprite_heroi = SpriteCompleto(anim_dict, escala=escala_final, pos_x=200, pos_y=ALTURA_CHAO)
        self.sprite_inimigo = SpriteCompleto(anim_dict_ini, escala=3.5, flip=True, pos_x=600, pos_y=ALTURA_CHAO)
        
        self.grupo_sprites = pygame.sprite.Group()
        self.grupo_sprites.add(self.sprite_heroi)
        self.grupo_sprites.add(self.sprite_inimigo)
        
        self.max_vida_heroi = self.heroi.vida
        self.max_vida_inimigo = self.inimigo.vida
        self.status = {"stun-guerreiro": False, "queimado-mago": False, "marcado-arqueiro": False}
        self.log_combate = "Batalha Iniciada!"
        self.timer_turno = 0
        self.estado_jogo = TURNO_JOGADOR

    def desenhar_texto(self, texto, cor, x, y, center=False, font=None):
        fonte_usar = font if font else self.fonte
        surf = fonte_usar.render(texto, True, cor)
        rect = surf.get_rect()
        if center: rect.center = (x, y)
        else: rect.topleft = (x, y)
        self.tela.blit(surf, rect)

    def desenhar_barra_vida(self, x, y, vida_atual, vida_max):
        pygame.draw.rect(self.tela, VERMELHO, (x, y, 200, 20))
        if vida_atual < 0: vida_atual = 0
        
        if vida_max > 0:
            porcentagem = vida_atual / vida_max
        else:
            porcentagem = 0
            
        largura_verde = 200 * porcentagem
        pygame.draw.rect(self.tela, VERDE, (x, y, largura_verde, 20))
        pygame.draw.rect(self.tela, BRANCO, (x, y, 200, 20), 2)
        self.desenhar_texto(f"{vida_atual}/{vida_max}", BRANCO, x + 70, y - 25)

    def logica_inimigo(self):
        if self.status["stun-guerreiro"]:
            self.log_combate = "Inimigo ATORDOADO! Perdeu a vez."
            self.status["stun-guerreiro"] = False
            return

        tipo_acao, (dano, txt, efeito) = self.inimigo.inteligencia_artificial()
        
        if tipo_acao == "atacar":
            self.sprite_inimigo.animar_ataque_normal()
        elif tipo_acao == "especial":
            self.sprite_inimigo.animar_especial()
        elif tipo_acao == "defender":
            self.sprite_inimigo.animar_defesa()

        if dano > 0:
            self.sprite_heroi.animar_dano() 
            morreu = self.heroi.receber_dano(dano) 
            if morreu: 
                self.checar_morte()
            
        if efeito != "NENHUM":
             pass

        self.log_combate = f"Inimigo: {txt} (-{dano} HP)"

    def aplicar_efeitos_passivos(self):
        if self.status["queimado-mago"]:
            self.sprite_inimigo.animar_dano()
            morreu = self.inimigo.receber_dano(5)
            self.log_combate = "Inimigo queima (-5 HP)."
            if morreu: self.checar_morte()

        if self.status["marcado-arqueiro"]:
            self.sprite_inimigo.animar_dano()
            morreu = self.inimigo.receber_dano(7)
            self.log_combate = "Inimigo sangra pela marca (-7 HP)."
            if morreu: self.checar_morte()

    def checar_morte(self):
        if not self.inimigo.esta_vivo():
            self.log_combate = "VITÓRIA! O Inimigo caiu."
            self.sprite_inimigo.kill()
            self.estado_jogo = FIM_DE_JOGO
            return True
        if not self.heroi.esta_vivo():
            self.log_combate = "DERROTA! Você caiu."
            self.sprite_heroi.kill()
            self.estado_jogo = FIM_DE_JOGO
            return True
        return False

    def desenhar_menu(self):
        self.desenhar_texto("ESCOLHA SEU HERÓI", AMARELO, 400, 100, center=True, font=self.fonte_grande)
        pygame.draw.rect(self.tela, VERMELHO, self.btn_guerreiro)
        pygame.draw.rect(self.tela, AZUL, self.btn_mago)
        pygame.draw.rect(self.tela, VERDE, self.btn_arqueiro)
        self.desenhar_texto("GUERREIRO", BRANCO, self.btn_guerreiro.centerx, self.btn_guerreiro.centery, center=True)
        self.desenhar_texto("MAGO", BRANCO, self.btn_mago.centerx, self.btn_mago.centery, center=True)
        self.desenhar_texto("ARQUEIRO", PRETO, self.btn_arqueiro.centerx, self.btn_arqueiro.centery, center=True)

    def desenhar_batalha(self):
        pygame.draw.rect(self.tela, CINZA, (0, ALTURA_CHAO, LARGURA, ALTURA - ALTURA_CHAO))
        
        if self.grupo_sprites:
            self.grupo_sprites.draw(self.tela)
            self.grupo_sprites.update() 
        
        if self.heroi and self.heroi.esta_vivo():
            self.desenhar_barra_vida(100, 50, self.heroi.vida, self.max_vida_heroi)
            self.desenhar_texto(self.heroi.nome, BRANCO, 100, 20)
        if self.inimigo and self.inimigo.esta_vivo():
            self.desenhar_barra_vida(500, 50, self.inimigo.vida, self.max_vida_inimigo)
            self.desenhar_texto(self.inimigo.nome, BRANCO, 500, 20)

        pygame.draw.rect(self.tela, CINZA, (150, 100, 500, 40))
        pygame.draw.rect(self.tela, BRANCO, (150, 100, 500, 40), 2)
        self.desenhar_texto(self.log_combate, AMARELO, 400, 120, center=True)

        if self.estado_jogo != FIM_DE_JOGO:
            cor_btn = AZUL if self.estado_jogo == TURNO_JOGADOR else CINZA_CLARO
            pygame.draw.rect(self.tela, cor_btn, self.btn_atacar)
            pygame.draw.rect(self.tela, cor_btn, self.btn_defender)
            pygame.draw.rect(self.tela, cor_btn, self.btn_especial)
            pygame.draw.rect(self.tela, BRANCO, self.btn_atacar, 2)
            pygame.draw.rect(self.tela, BRANCO, self.btn_defender, 2)
            pygame.draw.rect(self.tela, BRANCO, self.btn_especial, 2)
            self.desenhar_texto("ATACAR", BRANCO, 150, 545, center=True)
            self.desenhar_texto("DEFENDER", BRANCO, 375, 545, center=True)
            self.desenhar_texto("ESPECIAL", BRANCO, 600, 545, center=True)
        else:
            if self.heroi:
                msg = "VITÓRIA!" if self.heroi.esta_vivo() else "GAME OVER"
                cor_fim = VERDE if self.heroi.esta_vivo() else VERMELHO
            else:
                msg = "GAME OVER"
                cor_fim = VERMELHO
                
            surf = self.fonte_grande.render(msg, True, cor_fim)
            rect = surf.get_rect(center=(LARGURA//2, ALTURA//2))
            self.tela.blit(surf, rect)

    def run(self):
        rodando = True
        while rodando:
            self.relogio.tick(FPS)
            mouse_pos = pygame.mouse.get_pos()
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if self.estado_jogo == MENU:
                        if self.btn_guerreiro.collidepoint(mouse_pos): self.iniciar_batalha("guerreiro")
                        elif self.btn_mago.collidepoint(mouse_pos): self.iniciar_batalha("mago")
                        elif self.btn_arqueiro.collidepoint(mouse_pos): self.iniciar_batalha("arqueiro")

                    elif self.estado_jogo == TURNO_JOGADOR:
                        acao_feita = False
                        dano, txt, efeito = 0, "", "NENHUM"

                        if self.btn_atacar.collidepoint(mouse_pos):
                            self.sprite_heroi.animar_ataque_normal()
                            dano, txt, efeito = self.heroi.atacar()
                            acao_feita = True
                        
                        elif self.btn_defender.collidepoint(mouse_pos):
                            self.sprite_heroi.animar_defesa()
                            dano, txt, efeito = self.heroi.defender()
                            acao_feita = True
                            
                        elif self.btn_especial.collidepoint(mouse_pos):
                            self.sprite_heroi.animar_especial()
                            dano, txt, efeito = self.heroi.especial()
                            acao_feita = True

                        if acao_feita:
                            if dano > 0: 
                                self.sprite_inimigo.animar_dano()
                                morreu = self.inimigo.receber_dano(dano)
                                if morreu: self.checar_morte()
                                
                            if efeito != "NENHUM": self.status[efeito] = True
                            self.log_combate = f"Você: {txt}"
                            
                            if not self.checar_morte():
                                self.estado_jogo = PROCESSANDO
                                self.timer_turno = pygame.time.get_ticks()

            self.tela.fill(PRETO)
            
            if self.estado_jogo == MENU:
                self.desenhar_menu()
            else:
                self.desenhar_batalha()
                
                if self.estado_jogo == PROCESSANDO:
                    if pygame.time.get_ticks() - self.timer_turno > 1500:
                        self.aplicar_efeitos_passivos()
                        if not self.checar_morte():
                            self.estado_jogo = TURNO_INIMIGO
                            self.timer_turno = pygame.time.get_ticks()

                if self.estado_jogo == TURNO_INIMIGO:
                    if pygame.time.get_ticks() - self.timer_turno > 1000:
                        self.logica_inimigo()
                        self.checar_morte()
                        if self.estado_jogo != FIM_DE_JOGO:
                            self.estado_jogo = TURNO_JOGADOR

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    JogoRPG().run()