import objects.data as dat
import objects.mutations as mut
import objects.primitives as prim
import search.heuristics as heur
import search.greedy_solution as greed
import search.genetic_algorithm as genet

if __name__ == "__main__":
    prim.Problem.read_file("./input_data/mother_of_all_warehouses.in")

    best, best_score = genet.genetic_algorithm(50, 10, 0.1, 0.1)

    # chrom1 = greed.greedy_solution(False)
    # chrom2 = greed.greedy_solution(False)
    #
    # print(chrom1)
    # print("----")
    # print(chrom2)

    # solution = heur.hill_climbing(chromosome, 3000)
    # solution = heur.iterative_simulated_annealing(chromosome, heur.CoolingFunctions.linear, 5, 5)
    #
    # print(solution)
    # print("SCORE:", solution.update_internal(), "| PENALTY:", solution.penalty)

    pass
