import random
import re
import time
from operator import itemgetter
import math
_n = 25
_prob=0.05


def rand_pick(p):
    individ = []
    for i in range(p):
        temp = random.randint(0, 1)
        individ.append(temp)

    return individ

def rand_pick_m(p,n):
    individ = list()
    for id_rucsac in range(n):
        id_rucsac_l = []
        for ob_sel in range(p):
            temp = random.randint(0, 1)
            id_rucsac_l.append(temp)
        individ.append(id_rucsac_l)
    return individ

def eval(_key, _objects):

    res = pick_objects_rand(_key, _objects)
    s, w = compute_score_and_weight(res)

    return s, w


def eval_m(individ, _objects):
    s_t, w_t = 0,0
    for rucsac in individ:
        res = pick_objects_rand(rucsac, _objects)
        s, w = compute_score_and_weight(res)
        s_t += s
        w_t += w
    return s_t, w_t


def pick_objects_rand(key, _objects):
    results = []
    for i in range(0, len(_objects)):
        if key[i] == 1:
            results.append(_objects[i])
    return results


def compute_score_and_weight(_objects):
    score, weight = 0, 0
    for obj in _objects:
        score += obj[1]
        weight += obj[2]

    return score, weight



def rand_population(n):
    population = []
    for i in range(0, n):
        population.append(rand_pick(n))
    return population


def selection(population):
    n = len(population)
    a =random.randint(0,n-1)
    b = random.randint(0,n-1)
    mom = population[a]
    dad =  population[b]
    return mom, dad

def cross(_mom, _dad):
    n = len(_mom)
    pct = random.randint(0,n-1)
    child1=[]
    child2=[]
    for i in range(0,pct):
        child1.append(_mom[i])
        child2.append(_dad[i])
    for j in range(pct, n):
        child1.append(_dad[j])
        child2.append(_mom[j])
    return child1, child2

def mutation(parent, prob):
    child = []
    for i in range(0, len(parent)):
        prob_ran = random.randint(0,100)
        if prob_ran/100<prob:
            child.append(1-parent[i])
        else:
            child.append(parent[i])
    return child

def generate_and_pick():
    objects = list()
    with open("obiecte200.txt") as fd:
        count = int(fd.readline())
        for i in range(0, int(count)):
            parts = re.split('\s+', fd.readline().strip())
            objects.append((int(parts[0]), int(parts[1]), int(parts[2])))
        max_weight = int(fd.readline())
    return count, objects, max_weight

def evolutiv_alg(nr_iteratii, prob):

    best_score = 0
    n, objects, max_weight = generate_and_pick()
    t=0
    nr_for_avg = 0
    population = rand_population(n)
    _all_population = []
    all_population_fitness = list()
    while t < nr_iteratii:
        kids = []
        for i in range(0,int(n/2)):
            mom, dad = selection(population)
            child1, child2 = cross(mom, dad)
            kids.append(child1)
            kids.append(child2)
        mutated_kids = []
        for i in range(0, len(kids)):
            child = mutation(kids[i], prob)
            mutated_kids.append(child)
        _all_population = population + kids +mutated_kids
        for i in range(0,len(_all_population)):
            s_p, w_p = eval(_all_population[i], objects)
            if w_p<=max_weight:
                all_population_fitness.append((_all_population[i],s_p))
        all_population_fitness.sort(key=lambda x: x[1])
        all_population_fitness.reverse()
        best_score = all_population_fitness[0][1]
        for i in range(0,n):
            population[i] = all_population_fitness[i][0]
        t+=1

    return population, best_score

if __name__ =="__main__":
    k = 10
    k2 = 10
    avg_score = 0
    final_best_score = 0
    start_time = time.time()
    while k > 0:
        population, best_score = evolutiv_alg(200, 0.6)#generatii
       #print(population)
        #print("Best score is: ", best_score)
        if best_score>final_best_score:
            final_best_score = best_score
        avg_score +=best_score
        k-=1
    exec_time = time.time() - start_time
    print("Best score is: ", final_best_score)
    print("Average score is: ", avg_score/k2)
    print("When time for execution is: ", exec_time)
