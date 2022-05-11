import math
import sys
import numpy as np


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

    max = -1
    for categoria in matrizItems:
        for item in categoria:
            max = item.valor if item.valor >= max else max
    return max


vmax = paso1()


def paso2():
    global vmax, cantidadItems, epsilon
    for categoria in matrizItems:
        for item in categoria:
            item.valorRedondeado = math.floor(((item.valor)/(epsilon*vmax))*cantidadItems)
            # print(f"value: {item.valor}, rounded: {item.valorRedondeado}")
    return


paso2()


def paso3():
    vBound = math.ceil(math.pow(cantidadItems, 2)/epsilon)
    dp1 = np.full((cantidadCategorias, maxItems, vBound, maxItems+1), float("inf"))
    rangei = range(0, cantidadCategorias)
    rangej = range(1, maxItems)
    rangev = range(0, vBound)
    ranget = range(0, maxItems+1)
    # vraro = range (0, vBound)

    for i in range(0, cantidadCategorias):
        for v in range(0, vBound):
            for t in range(0, maxItems+1):
                j = 0
                # base cases
                currentItem = matrizItems[i][j] if j < len(matrizItems[i]) else matrizItems[i][len(matrizItems[i])-1]
                itemValor = currentItem.valorRedondeado
                itemPeso = currentItem.peso
                if v == itemValor and t == 1:
                    weight = itemPeso
                    dp1[i, j, v, t] = weight
                elif t == 0 and v == 0:
                    dp1[i, j, v, t] = 0
                # elif v != itemValor:
                #     dp1[i, j, v, t] = float("inf")

    for i in rangei:
        for j in rangej:
            for v in rangev:
                for t in ranget:
                    # base cases
                    currentItem = matrizItems[i][j] if j < len(matrizItems[i]) else matrizItems[i][len(matrizItems[i])-1]
                    itemValor = currentItem.valorRedondeado
                    itemPeso = currentItem.peso
                    # if j == 0 and v == itemValor and t == 1:
                    #     weight = itemPeso
                    #     dp1[i, j, v, t] = weight
                    # elif j == 0 and t == 0 and v == 0:
                    #     dp1[i, j, v, t] = 0
                    # elif j == 0 and v != itemValor:
                    #     dp1[i, j, v, t] = float("inf")
                    # induction cases
                    if v < currentItem.valor or t == 0:
                        dp1[i, j, v, t] = dp1[i, j-1, v, t]
                    else:
                        dpItem2p = dp1[i, j-1, v, t]
                        dpItems1p = dp1[i, j-1, :v+1, t-1].min() + itemPeso
                        minWeightFound = min(dpItems1p, dpItem2p)
                        dp1[i, j, v, t] = minWeightFound
    return dp1


def paso4(dp1: np.ndarray):
    vBound = math.ceil(math.pow(cantidadItems, 2)/epsilon)
    dp2 = np.zeros((cantidadCategorias, vBound))
    rangei = range(1, cantidadCategorias)
    rangev = range(0, vBound)

    for v in range(0, vBound):
        dp2[0, v] = dp1[0, len(matrizItems[0])-1, v, rangosInferiores[0]:rangosSuperiores[0]+1].min()
        # dp1values = [dp1[0, len(matrizItems[0])-1, v, t] for t in ranget]
        # dp2[0, v] = min(dp1values)

    for i in rangei:
        for v in rangev:
            minvalue = dp1[i, len(matrizItems[i])-1, :v+1, rangosInferiores[0]:rangosSuperiores[0]+1].min()
            foundValue = np.where(dp1[i, len(matrizItems[i])-1, :v+1, rangosInferiores[0]:rangosSuperiores[0]+1] == minvalue)
            vr = v - foundValue[0][0]
            dp2[i, v] = minvalue + dp2[i-1, vr]
            # ranget = range(rangosInferiores[0], rangosSuperiores[0]+1)
            # if i == 0:
            #     dp1values = [dp1[0, len(matrizItems[i])-1, v, t] for t in ranget]
            #     dp2[0, v] = min(dp1values)
            # else:
            # rangevSub = range(0, v)
            # for tr in ranget:
            #     for subv in rangevSub:
            #         mindp2Value = min(dp2[i-1, subv] + dp1[i, len(matrizItems[i])-1, v-subv, tr], mindp2Value)
            # dp2[i, v] = mindp2Value
    return dp2


def paso5(dp2):
    found = False
    vmax = 0
    col = dp2[cantidadCategorias-1]
    valueRange = len(col)-1
    while not found and valueRange >= 0:
        vmax = valueRange
        if col[valueRange] <= capacidad:
            found = True
        valueRange -= 1
    return vmax


matrizA = paso3()

matrizB = paso4(matrizA)

resultado = paso5(matrizB)
roundedBack = math.floor((resultado*epsilon*vmax)/(cantidadItems))

print(roundedBack)
