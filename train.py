import pandas
import numpy as np
from datetime import datetime
from random import random
from random import randint
import math as m
import json


t0 = datetime.now()
def evaluateCrs(exps, train):
    i = 0
    ers = [None] * len(exps)
    n = len(train)
    for exp in exps:
        er = 0
        for r in train.values:
            try:
                prod = eval(exp)
            except:
                prod = r[1] + 500
            er += (prod - r[1])**2
        ers[i] = er / n
        i += 1
    return ers


def generateCr(nCr, tamCr):
    return np.random.randint(0, 256, size = (nCr, tamCr))


def torneios(crs, ers, nCr, tamCr):
    winners = [None] * nCr 
    for i in range(nCr):
        selected = np.random.choice(nCr, 2, replace = False)
        if ers[selected[0]] < ers[selected[1]]:
            winners[i] = crs[selected[0]]
        else:
            winners[i] = crs[selected[1]]
    for i in range(nCr):
        for j in range(tamCr):
            crs[i][j] = winners[i][j]


def cruzamentos(probC, nCr, tamCr, crs):
    for i in range(nCr/2):
        if random() < probC:
            elem1 = 2 * i
            elem2 = elem1 + 1
            ptCruzamento = randint(1, tamCr - 1)
            for j in range(ptCruzamento, tamCr):
                aux = crs[elem1][j]
                crs[elem1][j] = crs[elem2][j]
                crs[elem2][j] = aux


def mutacoes(probM, crs, tamCr, nCr):
    for i in range(nCr):
        for j in range(tamCr):
            if random() < probM:
                crs[i][j] = randint(0, 256)


def getNaoTerminal(exp):
    for i in range(len(exp)):
        if exp[i] >= 'a' and exp[i] <= 'd':
            return i
    return -1


def generateExps(crs, regras, estInicial):
    exps = []
    for cr in crs:
        exp = estInicial
        idx = 0
        j = 0
        while True:
            exp = exp[:idx] + regras[exp[idx]][cr[j%len(cr)]%len(regras[exp[idx]])] + exp[idx+1:]
            j+=1
            idx = getNaoTerminal(exp)
            if len(exp)>150:
                exp = estInicial
                idx = 0
                j = 0
                for k in range(len(cr)):
                    cr[k] = randint(0, 256)
            if idx < 0:
                break
        exps.append(exp)
    return exps


def get_min(ers, exp, current_min_error, current_min_exp, crs, bestCrs, maximoParaSalvarCr):
    idx = 0
    for i in range(len(ers)):
        if ers[i] < ers[idx]:
            idx = i
    print('Erro minimo')
    print(ers[idx])
    print('Expressao')
    print(exp[idx])
    print('\n')
    if ers[idx] < current_min_error:
        current_min_error = ers[idx]
        current_min_exp = exp[idx]
    if ers[idx] < maximoParaSalvarCr:
        bestCrs['best_crs'].append(list(crs[idx]))
    return current_min_error, current_min_exp
            

def run(nCr, probC, probM, tamCr, regras, estInicial, numRep, maximoParaSalvarCr):
    train = pandas.read_csv("data/train.csv")
    train_results_read = open("train_results.txt", "r")

    bestCrs = {
        'best_crs' : []
    }
    
    current_min_error = float(train_results_read.readline())
    current_min_exp = train_results_read.readline()
    train_results_read.close()

    crs = generateCr(nCr, tamCr)
    with open('best_crs.json') as json_file:
        data = json.load(json_file)
        i=0
        while i<nCr and i<len(data['best_crs']):
            for j in range(tamCr):
                crs[i][j] = data['best_crs'][i][j]
            i+=1

    exps = generateExps(crs, regras, estInicial)
    ers = evaluateCrs(exps, train)
    current_min_error, current_min_exp = get_min(ers, exps, current_min_error, current_min_exp, crs, bestCrs, maximoParaSalvarCr)

    for i in range(numRep): 
        torneios(crs, ers, nCr, tamCr)
        cruzamentos(probC, nCr, tamCr, crs)
        mutacoes(probM, crs, tamCr, nCr)

        exps = generateExps(crs, regras, estInicial)
        ers = evaluateCrs(exps, train)

        current_min_error, current_min_exp = get_min(ers, exps, current_min_error, current_min_exp, crs, bestCrs, maximoParaSalvarCr)
        print(i)

    train_results_write = open("train_results.txt", "w")
    train_results_write.writelines([str(current_min_error), '\n', current_min_exp])
    train_results_write.close()
    with open('best_crs.json', 'w') as outfile:
        json.dump(bestCrs, outfile)

nCr = 300
probC = 0.8
probM = 0.1
tamCr = 30
numRep = 300
maximoParaSalvarCr = 1.5
regras = {
    'a' : ['aba', '(aba)', 'c(a)', 'd'], #exp
    'b' : ['+', '-', '*', '/'], #op
    'c' : ['m.log', 'm.sin', 'm.exp'], #pre-op
    'd' : ['r[2]', 'r[3]', 'r[4]', 'r[5]', 'r[6]', 'r[7]' ,'r[8]', 'r[9]', '1.0', '2.0', 'm.pi', 'm.e']  #var
}
estInicial = 'a'

run(nCr, probC, probM, tamCr, regras, estInicial, numRep, maximoParaSalvarCr)

print(datetime.now() - t0)