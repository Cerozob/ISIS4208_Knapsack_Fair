from queue import PriorityQueue
import sys
import math

class Item:
    def __init__(self, peso: int, valor: int) -> None:
        self.peso = peso
        self.valor = valor


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
    items = sorted(items, key=compareByWeight)
    matrizItems[categoriaActual] = items
    i += 3
    categoriaActual += 1

print(f"categorias: {cantidadCategorias}; capacidad: {capacidad}; epsilon: {epsilon}")
for i in range(cantidadCategorias):
    print(f"cat. actual: {i}")
    print(f"rangoInferior: {rangosInferiores[i]}")
    print(f"rangoSuperior: {rangosSuperiores[i]}")
    print(f"pesos: {matrizPesos[i]}")
    print(f"valores: {matrizValores[i]}")

# comparatorPeso=lambda x,y


def precalculateFeasibleSolution():
    solution = [[]]*cantidadCategorias
    suma = 0
    i = 0
    for i in range(cantidadCategorias):
        lowBound = rangosInferiores[i]
        solution[i] = matrizItems[i][:lowBound]
        pesos = [sol.peso for sol in solution[i]]
        suma += sum(pesos)
    return solution, suma


def hasToDeleteFromSolution(precalculated, precalcsum, i, item):
    currentCategory = precalculated[i]
    for j in range(len(currentCategory)):
        if(precalculated[i][j] == item):
            return False
    lastItem = precalculated[i][-1]
    newSum = precalcsum-lastItem.peso+item.peso
    if newSum > capacidad:
        return True
    return False


def paso1():
    precalculated, precalculatedSum = precalculateFeasibleSolution()
    i = 0
    markForDeletion = []
    for i in range(cantidadCategorias):
        j = 0
        categoriaActual = matrizItems[i]
        for j in range(len(categoriaActual)-1, -1, -1):
            deleteResult = hasToDeleteFromSolution(precalculated, precalculatedSum, i, matrizItems[i][j])
            if deleteResult:
                # matrizItems[i].remove(matrizItems[i][j])
                markForDeletion.append((i, j))

    for pair in markForDeletion:
        matrizItems[pair[0]].remove(matrizItems[pair[0]][pair[1]])
    return


paso1()
