# %% [markdown]
# # 1. generar el caso de prueba

# %%
from multiprocessing.pool import ThreadPool
import random
import pathlib
import json
import sys
import threading
import time
import subprocess


def gen_test_case():
    randomGen = random.Random()
    # categorias
    randomEpsilon = randomGen.uniform(0.3, 0.9)
    nCats = randomGen.randint(2, 8)
    # items por categoria
    itemsCat = randomGen.randint(2, 10)
    # rangos de fairness
    lranks = []
    uranks = []
    for i in range(nCats):
        lrank = randomGen.randint(1, itemsCat-1)
        urank = randomGen.randint(lrank+1, itemsCat)
        lranks.append(lrank)
        uranks.append(urank)

    # genero items fase 1
    minValues = []
    itemsGen = []

    optimalValue = 0
    maxWeight = 0
    for i in range(nCats):
        items = []
        minValue = randomGen.randint(75, 85)
        for j in range(uranks[i]):
            peso = randomGen.randint(50, 100)
            valor = randomGen.randint(minValue, 100)
            optimalValue += valor
            maxWeight += peso
            items.append((peso, valor))
        minValues.append(minValue)
        itemsGen.append(items)

    # genero items de nuevo

    for i in range(nCats):
        for j in range(uranks[i], randomGen.randint(itemsCat-uranks[i], itemsCat)):
            peso = randomGen.randint(1, 75)
            valor = randomGen.randint(0, minValues[i])
            itemsGen[i].append((peso, valor))
    returnObject = {
        "lowerRanks": lranks,
        "upperRanks": uranks,
        "nCategories": nCats,
        "optimalValue": optimalValue,
        "maxWeight": maxWeight,
        "epsilon": randomEpsilon,
        "itemMatrix": itemsGen
    }
    # print(returnObject)
    return returnObject
# print(lranks,uranks,sep="canoa")
# print(itemsGen,optimalValue,maxWeight,sep="canoa")


def parse_input(obj) -> str:
    inputString = ""
    inputString += f'{obj["nCategories"]}\t{obj["maxWeight"]}\t{obj["epsilon"]}\n'
    for cat in range(obj["nCategories"]):
        inputString += f'{obj["lowerRanks"][cat]}\t{obj["upperRanks"][cat]}\n'
        inputString += f'{obj["itemMatrix"][cat][0][0]}'
        for item in range(1, len(obj["itemMatrix"][cat])):
            inputString += f'\t{obj["itemMatrix"][cat][item][0]}'
        inputString += f'\n'
        inputString += f'{obj["itemMatrix"][cat][0][1]}'
        for item in range(1, len(obj["itemMatrix"][cat])):
            inputString += f'\t{obj["itemMatrix"][cat][item][1]}'
        inputString += f'\n'
    return inputString.rstrip("\n")


def gen_test_case_input():
    testCase = gen_test_case()
    # print(testCase)
    return {"input": parse_input(testCase), "case": testCase}
# %% [markdown]
# # 2.5 Ejecutar caso de prueba v2

# %%

# myrandomdataparsed = "3\t67\t0.5\n1\t2\n15\t10\t20\n2\t4\t6\n2\t3\n10\t20\t30\n1\t7\t2\n2\t5\n12\t15\t18\n5\t4\t3"


def measure_time(command, pinput):
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    timestart = time.time()
    output = process.communicate(input=pinput.encode())[0]
    timeend = time.time()
    totaltime = timeend-timestart
    return output, totaltime


def exec_testcase():
    stdincase = gen_test_case_input()
    optimalValue = stdincase["case"]["optimalValue"]
    # print(stdincase)
    commandNuestro = ["python", r".\algoritmoNuestro.py"]
    commandPaper = ["python", r".\algoritmoPaper.py"]
    nosotros = measure_time(commandNuestro, stdincase["input"])
    paper = measure_time(commandPaper, stdincase["input"])
    paperoutput = int(paper[0].decode('utf-8')) if paper[0].decode('utf-8').strip().isnumeric() else paper[0].decode('utf-8')

    nosotrosoutput = int(nosotros[0].decode('utf-8')) if nosotros[0].decode('utf-8').strip().isnumeric() else nosotros[0].decode('utf-8')

    results = {"optimalValue": optimalValue,
               "resultPaper": paperoutput,
               "resultNuestro": nosotrosoutput,
               "timeTakenPaper": paper[1],
               "timeTakenNosotros": nosotros[1],
               "case": stdincase
               }
    return results


# %% [markdown]
# # 3. tomar tiempos acumualados

# %%


def launchTestCase(i):
    currentjsonfile = pathlib.Path("testdata10K").joinpath(f"exec_data_{i}.json")
    print(f"starting execution #{i+1}")
    if not currentjsonfile.exists():
        currentjsonfile.touch()
    with open(currentjsonfile, "w") as file:
        json.dump(exec_testcase(), file)
    print(f"ending execution #{i+1}")


def save_time(times=None):
    nExcecutions = 500 if times is None else int(times)
    threads = 6
    s = threading.Semaphore(threads)
    pool = ThreadPool()
    for i in range(nExcecutions):
        t = threading.Thread(target=launchTestCase(i), name=f'thread_{i}', args=(s, pool))
        t.start()


save_time(sys.argv[1] if len(sys.argv) > 1 else None)
