# Combate de Turno — RPG em Python

Jogo de RPG por turnos com interface gráfica feita em Pygame. O jogador
escolhe uma classe, enfrenta um inimigo controlado por IA e usa ataques,
defesa e habilidades especiais para vencer o combate.

## Sobre

Projeto desenvolvido para explorar orientação a objetos com classes abstratas,
interface gráfica com Pygame, animações por sprite sheet e testes automatizados
com pytest. O jogo possui duas versões: terminal e interface gráfica completa.

## Tecnologias

- Python
- Pygame (interface gráfica e animações)
- pytest (testes automatizados)
- ABC / classes abstratas

## Classes disponíveis

| Classe | HP | Habilidade especial | Estilo |
|--------|-----|---------------------|--------|
| Guerreiro | 150 | Golpe Esmagador (2 cargas) | Tank |
| Mago | 80 | Meteoro de Fogo (4 cargas) | Alto dano |
| Arqueiro | 110 | Chuva de Flechas (3 cargas) | Crítico/Marca |

## Efeitos de status

- **Stun** (Guerreiro) — inimigo perde o próximo turno
- **Queimado** (Mago) — inimigo sofre 5 de dano por turno
- **Marcado** (Arqueiro) — inimigo sofre 7 de dano extra por turno

## Como rodar

```bash
git clone https://github.com/ArthurFigg/combate_de_turno.git
cd combate_de_turno

python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

pip install pygame pytest

# Versão gráfica (Pygame):
python interface.py

# Versão terminal:
python Main.py

# Rodar os testes:
pytest test_personagem.py
```

## Aprendizados

- Classes abstratas com ABC para definir contratos entre subclasses
- Herança e polimorfismo aplicados a um sistema de combate
- Animações por sprite sheet com Pygame (carregamento, corte e troca de frames)
- Máquina de estados para gerenciar fases do jogo (menu, turno, processando, fim)
- Testes unitários com pytest cobrindo criação de personagens e mecânicas de combate
