#!/usr/bin/python3

import random;
from enum import Enum;

MAXIMO_PARTIDAS = 300
MAXIMO_RODADAS = 1000
MAXIMO_PROPRIEDADES = 20
MINIMO_JOGADORES = 4
MAXIMO_JOGADORES = 4
VALOR_INICIAL_JOGADOR = 500
BONUS_VOLTA_COMPLETA = 100
PROPRIEDADE_VALORVENDA = 50
PROPRIEDADE_VALORALUGUEL = 5

class Perfil(Enum):
    IMPULSIVO = 1
    EXIGENTE = 2
    CAUTELOSO = 3
    ALEATORIO = 4

class Resultado:
    saidasPorTimeout = 0
    mediaDeTurnos = 0
    vitoriasImpulsivo = 0
    vitoriasExigente = 0
    vitoriasCauteloso = 0
    vitoriasAleatorio = 0

class Propriedade:
    custoVenda = 0
    valorAluguel = 0
    proprietario = None

    def __init__(self, valorVenda, aluguel):
        self.custoVenda = valorVenda
        self.valorAluguel = aluguel

class Tabuleiro:
    posicao = []

    def __init__(self):
        for prop in range(1, MAXIMO_PROPRIEDADES):
            self.posicao.append( Propriedade(PROPRIEDADE_VALORVENDA, PROPRIEDADE_VALORALUGUEL) )
            #Insere uma posicao em branco sem propriedade
            self.posicao.append( None )

    def print_proprietarios(self):
        for prop in self.posicao:
            if prop != None:
                if prop.proprietario == None:
                    print('Propriedade sem dono')
                else:
                    print('Dono da propriedade: ' + str(prop.proprietario.identidade))


class Jogador:
    saldo = 0
    _perfil = Perfil.IMPULSIVO
    posicao = 0
    identidade = 0

    def __init__(self, valorSaldo, perfilJogador, ident):
        self.saldo = valorSaldo
        self.setPerfil(perfilJogador)
        self.identidade = ident

    def setPerfil (self, perfil):
        if perfil in Perfil._value2member_map_:
            self._perfil = perfil

    def ganhaBonus(self):
        self.saldo += BONUS_VOLTA_COMPLETA

    def recebeAluguel(self, valorAluguel):
        self.saldo += valorAluguel

    def comprar(self, propriedade):
        if self._perfil == Perfil.IMPULSIVO:
            if self.saldo < propriedade.custoVenda:
                #print(str(self.saldo) + ' é menor que ' + str(propriedade.custoVenda))
                return
            self.saldo -= propriedade.custoVenda
            propriedade.proprietario = self
            #print('COMPRADO 1')
            return
        elif self._perfil == Perfil.EXIGENTE:
            if self.saldo < propriedade.custoVenda or propriedade.valorAluguel <= 50:
                return
            self.saldo -= propriedade.custoVenda
            propriedade.proprietario = self
            #print('COMPRADO 2')
            return
        elif self._perfil == Perfil.CAUTELOSO:
            if self.saldo < propriedade.custoVenda or (self.saldo - propriedade.custoVenda) < 80:
                return
            self.saldo -= propriedade.custoVenda
            propriedade.proprietario = self
            #print('COMPRADO 3')
            return
        elif self._perfil == Perfil.ALEATORIO:
            if self.saldo < propriedade.custoVenda or random.randrange(0, 2) == 0:
                return
            self.saldo -= propriedade.custoVenda
            propriedade.proprietario = self
            #print('COMPRADO 4')
            return
        else:
            print('Nenhum perfil para comprar')



class Dado:
    def __init__(self):
        pass

    def sorteio(self):
        return random.randrange(1,7)



class Game:
    tabuleiro = Tabuleiro()
    dado = Dado()
    jogadores = []
    resultado = Resultado()

    def __init__(self):
        random.seed()
        #for jog in range(1, MINIMO_JOGADORES + 1):
        self.jogadores.append( Jogador(VALOR_INICIAL_JOGADOR, Perfil.IMPULSIVO, 1 ) )
        self.jogadores.append( Jogador(VALOR_INICIAL_JOGADOR, Perfil.EXIGENTE, 2 ) )
        self.jogadores.append( Jogador(VALOR_INICIAL_JOGADOR, Perfil.CAUTELOSO, 3 ) )
        self.jogadores.append( Jogador(VALOR_INICIAL_JOGADOR, Perfil.ALEATORIO, 4 ) )


    def jogada(self):
        jogadores_jogando = 0
        for jogador in self.jogadores:
            if jogador.identidade == 0:
                #print('Jogador sem identidade...')
                continue
            jogadores_jogando += 1
            #print('Jogador ' + str(jogador.identidade) + ' jogando...')
            saltos = self.dado.sorteio()
            #print('Jogador ' + str(jogador.identidade) + ' andando ' + str(saltos) + ' casas...')
            if (jogador.posicao + saltos) > (len(self.tabuleiro.posicao) - 1):
                #jogador.posicao = self.tabuleiro.posicao[0 + (saltos - (len(self.tabuleiro.posicao) - jogador.posicao))]
                jogador.posicao = saltos - (len(self.tabuleiro.posicao) - jogador.posicao)
                jogador.ganhaBonus()
                #print('Jogador ' + str(jogador.identidade) + ' ganhou bonus')
            else:
                jogador.posicao += saltos
            if self.tabuleiro.posicao[jogador.posicao] != None:
                if self.tabuleiro.posicao[jogador.posicao].proprietario == None:
                    #print('Jogador ' + str(jogador.identidade) + ' comprando...')
                    jogador.comprar(self.tabuleiro.posicao[jogador.posicao])
                elif self.tabuleiro.posicao[jogador.posicao].proprietario.identidade == 0:
                    #print('Jogador ' + str(jogador.identidade) + ' comprando...')
                    jogador.comprar(self.tabuleiro.posicao[jogador.posicao])
                else:
                    #print('Jogador ' + str(jogador.identidade) + ' pagando aluguel...')
                    self.tabuleiro.posicao[jogador.posicao].proprietario.recebeAluguel (self.tabuleiro.posicao[jogador.posicao].valorAluguel)
                    jogador.saldo -= self.tabuleiro.posicao[jogador.posicao].valorAluguel
            if jogador.saldo < 0:
                #print('Jogador ' + str(jogador.identidade) + ' sendo removido do jogo...')
                jogador.identidade = 0
            jogadores_jogando += 1

        return jogadores_jogando;

    def print_jogadores(self):
        for jogador in self.jogadores:
            print('Saldo do jogador: ' + str(jogador.saldo))

    def print_tabuleiro(self):
        self.tabuleiro.print_proprietarios()

    def print_all(self):
        self.print_jogadores()
        self.print_tabuleiro()
        print ('Media de turnos: ' + str (self.resultado.mediaDeTurnos / MAXIMO_PARTIDAS))
        print ('Saidas por timeout: ' + str(self.resultado.saidasPorTimeout))
        print ('Vitorias Impulsivo: ' + str(self.resultado.vitoriasImpulsivo))
        print ('Vitorias Exigente: ' + str(self.resultado.vitoriasExigente))
        print ('Vitorias Cauteloso: ' + str(self.resultado.vitoriasCauteloso))
        print ('Vitorias Aleatorio: ' + str(self.resultado.vitoriasAleatorio))

    def calculaTotais(self, turnos):
        self.resultado.mediaDeTurnos += turnos
        if turnos == MAXIMO_RODADAS:
            self.resultado.saidasPorTimeout += 1
        if self.jogadores[0].saldo > self.jogadores[1].saldo and self.jogadores[0].saldo > self.jogadores[2].saldo and self.jogadores[0].saldo > self.jogadores[3].saldo:
            self.resultado.vitoriasImpulsivo += 1
        elif self.jogadores[1].saldo > self.jogadores[0].saldo and self.jogadores[1].saldo > self.jogadores[2].saldo and self.jogadores[1].saldo > self.jogadores[3].saldo:
            self.resultado.vitoriasExigente += 1
        elif self.jogadores[2].saldo > self.jogadores[0].saldo and self.jogadores[2].saldo > self.jogadores[1].saldo and self.jogadores[2].saldo > self.jogadores[3].saldo:
            self.resultado.vitoriasCauteloso += 1
        elif self.jogadores[3].saldo > self.jogadores[0].saldo and self.jogadores[3].saldo > self.jogadores[1].saldo and self.jogadores[3].saldo > self.jogadores[2].saldo:
            self.resultado.vitoriasAleatorio += 1



def main():
    game = Game()

    for it in range(1, MAXIMO_PARTIDAS + 1):
        turnos = 0
        for jogada in range(1, MAXIMO_RODADAS + 1):
            turnos = jogada
            #print ('Jogada ' + str(jogada))
            if game.jogada() <= 1:
                print ('Game Over!!')
                break

        game.calculaTotais(turnos)
    game.print_all()



if __name__ == '__main__':
    main()
