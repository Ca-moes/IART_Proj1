from objects.primitives import *
from numpy import random, mean
import search.greedy_solution as greed


def create_population(n_pop) -> list[Chromosome]:
    population = []
    for i in range(n_pop):
        population.append(greed.greedy_solution(False))
    return population


def best_individual(pop: list[Chromosome]) -> (Chromosome, float):
    current_best = (None, -9999)
    for chromosome in pop:
        score = chromosome.update_internal()
        if score > current_best[1]:
            current_best = chromosome, score
    return current_best


# tournament selection
def selection(pop, scores, k=3) -> Chromosome:
    # first random selection
    selection_ix = random.randint(len(pop))
    for ix in random.randint(0, len(pop), k - 1):
        # check if better (e.g. perform a tournament)
        if scores[ix] > scores[selection_ix]:
            selection_ix = ix
    return pop[selection_ix]


# TODO Fazer o algoritmo de crossover
def crossover(p1: Chromosome, p2: Chromosome, r_cross: float) -> list[Chromosome]:
    if random.random() <= r_cross:
        # ver tamanhos de ambos os cromossomas
        # escolher menor dos 2
        max_length = min(len(p1.genes), len(p2.genes))

        # escolher tamanho de 1 até o valor de cima
        size = random.randint(1, max_length)

        # escolher indice inicial de genes entre ind 0 e len-tamanho de cima
        g1_ind = random.randint(0, len(p1.genes)-size+1)
        g2_ind = random.randint(0, len(p2.genes)-size+1)

        # fazer a troca
        g1_genes = p1.genes[g1_ind:g1_ind+size]
        g2_genes = p2.genes[g2_ind:g2_ind+size]

        g1_drones = [gene.drone_id for gene in g1_genes]
        g2_drones = [gene.drone_id for gene in g2_genes]

        for i in range(g1_ind, g1_ind+size):
            p1.genes[i].drone_id = g2_drones[i - g1_ind]

        for i in range(g2_ind, g2_ind+size):
            p2.genes[i].drone_id = g1_drones[i - g2_ind]

        # To switch genes instead of drones
        # p1.genes[g1_ind:g1_ind+size] = g2_genes
        # p2.genes[g2_ind:g2_ind+size] = g1_genes

        return [p1, p2]
    return [p1, p2]


def mutation(c: Chromosome, r_mut) -> Chromosome:
    if random.random() <= r_mut:
        new_c = c.mutate()
        return new_c
    return c


def genetic_algorithm(n_iter, n_pop, r_cross, r_mut):
    # initial population of random bitstring
    pop = create_population(n_pop)
    # keep track of best solution
    best, best_eval = best_individual(pop)
    # enumerate generations
    for gen in range(n_iter):
        # evaluate all candidates in the population
        scores = [c.update_internal() for c in pop]
        print("GEN ", gen, "OF ", n_iter, "| MAX SCORE: ", str(max(scores)), " MEDIUM: ", mean(scores))
        # check for new best solution
        for i in range(n_pop):
            if scores[i] > best_eval:
                best, best_eval = pop[i], scores[i]
                print(">%d, new best f(%s) = %.3f" % (gen, pop[i], scores[i]))
        # select parents
        selected = [selection(pop, scores) for _ in range(n_pop)]
        # create the next generation
        children = list()
        for i in range(0, n_pop, 2):
            # get selected parents in pairs
            p1, p2 = selected[i], selected[i + 1]
            # crossover and mutation
            for c in crossover(p1, p2, r_cross):
                # mutation
                new_c = mutation(c, r_mut)
                # store for next generation
                children.append(new_c)
        # replace population
        pop = children

    return [best, best_eval]
