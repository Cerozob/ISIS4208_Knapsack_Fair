import math
from random import Random
import sys
import numpy as np
import copy


class Item:
    def __init__(self, peso: int, valor: int) -> None:
        self.peso = peso
        self.valor = valor
        self.valorRedondeado = -1


class Categoria:
    def __init__(self, limInf: int, limSup: int, items: list[Item]) -> None:
        self.limInf = limInf
        self.limSup = limSup
        self.items = items

# conjuntos de categorías -
# capacidad del mochila -
# epsilon -
# items de categorias con peso y utilidad
# rangos de cada categoría


inputLines = sys.stdin.read().split("\n")
primeraLinea = inputLines[0].split("\t")
cantidadCategorias = int(primeraLinea[0])
capacidad = int(primeraLinea[1])
epsilon = float(primeraLinea[2])
i = 1
categoriaActual = 0
rangosInferiores = [0]*cantidadCategorias
rangosSuperiores = [0]*cantidadCategorias
matrizPesos = [0]*cantidadCategorias
matrizValores = [0]*cantidadCategorias
matrizItems = [[]]*cantidadCategorias


def compareByWeight(x: Item):
    return x.peso


cantidadItems = 0
maxItems = 0
while i < len(inputLines):
    categoria = inputLines[i:i+3]
    rango = categoria[0].split("\t")
    rangosInferiores[categoriaActual] = (int(rango[0]))
    rangosSuperiores[categoriaActual] = (int(rango[1]))
    pesos = [int(peso) for peso in categoria[1].split("\t")]
    matrizPesos[categoriaActual] = pesos
    valores = [int(valor) for valor in categoria[2].split("\t")]
    items = []
    for peso, valor in zip(pesos, valores):
        items.append(Item(peso, valor))
        cantidadItems += 1
    maxItems = len(items) if len(items) >= maxItems else maxItems
    items = sorted(items, key=compareByWeight)
    matrizItems[categoriaActual] = items
    i += 3
    categoriaActual += 1

# print(f"categorias: {cantidadCategorias}; capacidad: {capacidad}; epsilon: {epsilon}")
# for i in range(cantidadCategorias):
#     print(f"cat. actual: {i}")
#     print(f"rangoInferior: {rangosInferiores[i]}")
#     print(f"rangoSuperior: {rangosSuperiores[i]}")
#     print(f"pesos: {matrizPesos[i]}")
#     print(f"valores: {matrizValores[i]}")

# comparatorPeso=lambda x,y


def precalculateFeasibleSolution():
    solution = [[]]*cantidadCategorias
    util = 0
    i = 0
    for i in range(cantidadCategorias):
        lowBound = rangosInferiores[i]
        solution[i] = matrizItems[i][:lowBound]
        valores = [sol.valor for sol in solution[i]]
        util += sum(valores)
    return solution, util


def invertedFeasibleSolution():
    solution = [[]]*cantidadCategorias
    i = 0
    for i in range(cantidadCategorias):
        lowBound = rangosInferiores[i]
        solution[i] = matrizItems[i][lowBound+1:]
    return solution


randomObject = Random()
solucionRespuesta = []


def getRandomCategory(items):
    global randomObject
    index = randomObject.randint(0, len(items)-1)
    return items[index], index


def solveRandomOnce(items, remainingBounds):
    currentWeight = 0
    partialSolution = []
    finished = False

    for index in range(len(items)-1, -1, -1):
        if len(items[index]) == 0:
            items.pop(index)
            remainingBounds.pop(index)

    while (not finished) and (len(items) > 0):
        category, catIndex = getRandomCategory(items)
        if remainingBounds[catIndex] == 0 or len(category) == 0:
            items.pop(catIndex)
            remainingBounds.pop(catIndex)
            continue
        nextItem = category[0]
        if nextItem.peso+currentWeight > capacidad:
            finished = True
        elif nextItem.peso+currentWeight <= capacidad:
            partialSolution.append(nextItem)
            items[catIndex].pop(0)
            remainingBounds[catIndex] -= 1
            
    valueSum = 0
    for item in partialSolution:
        valueSum += item.valor

    return partialSolution, valueSum


def iterateRandom(s: int):
    solMenorActual = []
    maxValor = 0
    precalculatedSol, precalculatedValue = precalculateFeasibleSolution()
    invertedSolution = invertedFeasibleSolution()
    remainingBounds = [ub-lb for lb, ub in zip(rangosInferiores, rangosSuperiores)]
    for i in range(s):
        currentSol, currentValue = solveRandomOnce(copy.deepcopy(invertedSolution), copy.copy(remainingBounds))
        if currentValue > maxValor:
            solMenorActual = currentSol
            maxValor = currentValue

    for cat in precalculatedSol:
        solMenorActual += cat
    return solMenorActual, maxValor + precalculatedValue


sol = iterateRandom(int(math.log2(cantidadItems*cantidadCategorias)))

# print(sol[0], sol[1])
print(sol[1])
