# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from personagem import Guerreiro, Mago, Arqueiro, Inimigo

def test_criar_guerreiro_corretamente():
    heroi = Guerreiro("Arthur", 1, 150)

    assert heroi.nome == "Arthur"
    
    assert heroi.vida == 150
    
    assert heroi.carga_especial == 0


def test_criar_mago_corretamente():
    heroi = Mago("Merlin", 1, 100)

    assert heroi.nome == "Merlin"

    assert heroi.vida == 100

    assert heroi.carga_especial == 0
    
def test_criar_arqueiro_corretamente():
    heroi = Arqueiro("Legolas", 1, 120)

    assert heroi.nome == "Legolas"

    assert heroi.vida == 120

    assert heroi.carga_especial == 0

def test_criar_inimigo_corretamente():
    inimigo = Inimigo("Goblin", 1, 90)

    assert inimigo.nome == "Goblin"

    assert inimigo.vida == 90

def test_ataque_guerreiro():
    heroi = Guerreiro("Arthur", 1, 150)
    inimigo = Inimigo("Orc", 1, 120)

    dano, texto, efeito = heroi.atacar()

    assert dano >= 8
    assert isinstance(dano, int)
    
    vida_antes = inimigo.vida
    inimigo.vida -= dano
    assert inimigo.vida < vida_antes

def test_ataque_mago():
    heroi = Mago("Merlin", 1, 100)
    inimigo = Inimigo("Orc", 1, 120)

    dano, texto, efeito = heroi.atacar()

    assert dano >= 10
    assert isinstance(dano, int)
    
    inimigo.vida -= dano
    assert inimigo.vida < 120

def test_ataque_arqueiro():
    heroi = Arqueiro("Legolas", 1, 120)
    inimigo = Inimigo("Orc", 1, 120)

    dano, texto, efeito = heroi.atacar()

    assert dano >= 10
    assert isinstance(dano, int)
    
    inimigo.vida -= dano
    assert inimigo.vida < 120

def test_ataque_inimigo():
    heroi = Guerreiro("Arthur", 1, 150)
    inimigo = Inimigo("Orc", 1, 120)

    dano, texto, efeito = inimigo.atacar()

    assert dano >= 5
    assert isinstance(dano, int)
    
    heroi.vida -= dano
    assert heroi.vida < 150


def test_defesa_guerreiro():
    heroi = Guerreiro("Arthur", 1, 150)

    carga_antes = heroi.carga_especial

    dano, texto, efeito = heroi.defender()

    assert dano == 0
    assert heroi.carga_especial == carga_antes + 1

def test_defesa_mago():
    heroi = Mago("Merlin", 1, 100)

    carga_antes = heroi.carga_especial

    dano, texto, efeito = heroi.defender()

    assert dano == 0
    assert heroi.carga_especial == carga_antes + 1

def test_defesa_arqueiro():
    heroi = Arqueiro("Legolas", 1, 120)

    carga_antes = heroi.carga_especial

    dano, texto, efeito = heroi.defender()

    assert dano == 0
  
