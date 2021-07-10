import threading
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import random
from typing import List, Any
import matplotlib.pyplot as plt
import numpy
from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp
from deap.gp import PrimitiveSetTyped
from Client import send_proto_request
from Client import send_request
from TTTclasses import *
import bp_pb2
import socket
import pandas as pd

# Define global arguments
NUMBER_OF_GENERATIONS = 100
POPULATION_SIZE = 100
AVERAGES = []
MAXIMUMS = []
MINIMUMS = []
MEDIANS = []
CURR_GEN = 1
INDV_ID = 0
anomaly_dict = {}
anomaly_dict_v2 = {}

lock = threading.Lock()
prev_time = 0


df = pd.DataFrame({'Generation': [],
                   'Individual': [],
                   'Fitness': [],
                   'Wins': [],
                   'Losses': [],
                   'Draws': [],
                   'Block_Violations': [],
                   'Misses': [],
                   'Blocks': [],
                   'Deadlocks': [],
                   'Forks': [],
                   'Code': []})


def results_to_fitness(wins, wins_misses, blocks, block_misses, deadlocks):
    try:
        win_stat = wins / (wins + wins_misses)
    except:
        win_stat = 1
    try:
        block_stat = blocks / (blocks + block_misses)
    except:
        block_stat = 1
    return 50 * win_stat + 50 * block_stat - deadlocks


def document_individual(individual, curr_id, fitness, wins, draws, losses, blocks_v, misses, blocks, deadlocks, forks, code):
    # tree
    #nodes, edges, labels = gp.graph(individual)
    #g = pgv.AGraph()
    #g.add_nodes_from(nodes)
    #g.add_edges_from(edges)
    #g.layout(prog="dot")
    #for i in nodes:
    #    n = g.get_node(i)
    #    n.attr["label"] = labels[i]
    #img_name = "gen_" + str(CURR_GEN) + ".png"
    #folder_name = "../trees/Individual" + str(curr_id)
    #if not os.path.exists(folder_name):
    #    os.makedirs(folder_name)
    #g.draw(folder_name + "/" + img_name)
    # stats
    with lock:
        df.loc[len(df)] = [CURR_GEN, curr_id, fitness, wins, draws, losses, blocks_v, misses, blocks, deadlocks, forks, code]


# Send to BPServer to evaluate
def eval_generator(individual):
    global INDV_ID
    func = toolbox.compile(expr=individual)
    func_string = str(func(0).root)
    indv = bp_pb2.Individual()
    indv.generation = CURR_GEN
    with lock:
        INDV_ID += 1
        indv.id = INDV_ID
    indv.code.code = func_string
    results = send_proto_request(indv)
    anomaly_dict[func_string] = (results.blocks_violations, results.misses, results.forks)
    anomaly_dict_v2[func_string] = (results.block_v, results.win_v, results.fork_v, results.requests)
    fitness = results_to_fitness(results.wins, results.misses, results.blocks, results.blocks_violations, results.deadlocks)
    document_individual(individual, indv.id, fitness, results.wins, results.draws, results.losses, results.blocks_violations, results.misses, results.blocks, results.deadlocks, results.forks, func_string)
    return fitness,


# Grammar Setup
pset = PrimitiveSetTyped("main", [root], root_wrapper)
pset.addPrimitive(root_wrapperFunc, [root], root_wrapper)
pset.addPrimitive(rootFunc, [btA, btA, btB, btB, btB, btB, btB, btC, btC, btC], root)

# BThreads
pset.addPrimitive(btAFunc, [while_trueA], btA)
pset.addPrimitive(btBFunc, [while_trueB], btB)
pset.addPrimitive(btCFunc, [while_trueC], btC)

# Loop for BT1
# 0 Waits
pset.addPrimitive(while_trueA_0, [request02], while_trueA)
pset.addPrimitive(while_trueA_0, [requestC], while_trueA)
# 1 Waits
pset.addPrimitive(while_trueA_1, [wait02, request02], while_trueA)
pset.addPrimitive(while_trueA_1, [wait02, requestC], while_trueA)
pset.addPrimitive(while_trueA_1, [waitC, request02], while_trueA)
pset.addPrimitive(while_trueA_1, [waitC, requestC], while_trueA)
# 2 Waits
pset.addPrimitive(while_trueA_2, [wait02, wait02, request02], while_trueA)
pset.addPrimitive(while_trueA_2, [wait02, wait02, requestC], while_trueA)
pset.addPrimitive(while_trueA_2, [wait02, waitC, request02], while_trueA)
pset.addPrimitive(while_trueA_2, [wait02, waitC, requestC], while_trueA)
pset.addPrimitive(while_trueA_2, [waitC, wait02, request02], while_trueA)
pset.addPrimitive(while_trueA_2, [waitC, wait02, requestC], while_trueA)
pset.addPrimitive(while_trueA_2, [waitC, waitC, request02], while_trueA)
pset.addPrimitive(while_trueA_2, [waitC, waitC, requestC], while_trueA)

# Loop for BT2
# 0 Waits
pset.addPrimitive(while_trueB_0, [request01], while_trueB)
pset.addPrimitive(while_trueB_0, [requestC], while_trueB)
# 1 Waits
pset.addPrimitive(while_trueB_1, [wait01, request01], while_trueB)
pset.addPrimitive(while_trueB_1, [wait01, requestC], while_trueB)
pset.addPrimitive(while_trueB_1, [waitC, request01], while_trueB)
pset.addPrimitive(while_trueB_1, [waitC, requestC], while_trueB)
# 2 Waits
pset.addPrimitive(while_trueB_2, [wait01, wait01, request01], while_trueB)
pset.addPrimitive(while_trueB_2, [wait01, wait01, requestC], while_trueB)
pset.addPrimitive(while_trueB_2, [wait01, waitC, request01], while_trueB)
pset.addPrimitive(while_trueB_2, [wait01, waitC, requestC], while_trueB)
pset.addPrimitive(while_trueB_2, [waitC, wait01, request01], while_trueB)
pset.addPrimitive(while_trueB_2, [waitC, wait01, requestC], while_trueB)
pset.addPrimitive(while_trueB_2, [waitC, waitC, request01], while_trueB)
pset.addPrimitive(while_trueB_2, [waitC, waitC, requestC], while_trueB)

# Loop for BT3
# 0 Waits
pset.addPrimitive(while_trueC_0, [requestC], while_trueC)
# 1 Waits
pset.addPrimitive(while_trueC_1, [waitC, requestC], while_trueC)
# 2 Waits
pset.addPrimitive(while_trueC_2, [waitC, waitC, requestC], while_trueC)

# Wait Permutation of 0-2:
pset.addPrimitive(wait02_1, [Perm02], wait02)
pset.addPrimitive(wait02_2, [Perm02, Perm02], wait02)
pset.addPrimitive(wait02_3, [Perm02, Perm02, Perm02], wait02)
pset.addPrimitive(wait02_4, [Perm02, Perm02, Perm02, Perm02], wait02)

# Wait Permutation of 0-1
pset.addPrimitive(wait01_1, [Perm01], wait01)
pset.addPrimitive(wait01_2, [Perm01, Perm01], wait01)
pset.addPrimitive(wait01_3, [Perm01, Perm01, Perm01], wait01)
pset.addPrimitive(wait01_4, [Perm01, Perm01, Perm01, Perm01], wait01)

# Wait Concrete
pset.addPrimitive(waitC_1, [Concrete], waitC)
pset.addPrimitive(waitC_2, [Concrete, Concrete], waitC)
pset.addPrimitive(waitC_3, [Concrete, Concrete, Concrete], waitC)
pset.addPrimitive(waitC_4, [Concrete, Concrete, Concrete, Concrete], waitC)

# Request Permutation of 0-2
pset.addPrimitive(request02_1, [Perm02_O, priority], request02)
pset.addPrimitive(request02_2, [Perm02_O, Perm02_O, priority], request02)
pset.addPrimitive(request02_3, [Perm02_O, Perm02_O, Perm02_O, priority], request02)
pset.addPrimitive(request02_4, [Perm02_O, Perm02_O, Perm02_O, Perm02_O, priority], request02)

# Request Permutation of 0-1
pset.addPrimitive(request01_1, [Perm01_O, priority], request01)
pset.addPrimitive(request01_2, [Perm01_O, Perm01_O, priority], request01)
pset.addPrimitive(request01_3, [Perm01_O, Perm01_O, Perm01_O, priority], request01)
pset.addPrimitive(request01_4, [Perm01_O, Perm01_O, Perm01_O, Perm01_O, priority], request01)

# Request Concrete
pset.addPrimitive(requestC_1, [Concrete_O, priority], requestC)
pset.addPrimitive(requestC_2, [Concrete_O, Concrete_O, priority], requestC)
pset.addPrimitive(requestC_3, [Concrete_O, Concrete_O, Concrete_O, priority], requestC)
pset.addPrimitive(requestC_4, [Concrete_O, Concrete_O, Concrete_O, Concrete_O, priority], requestC)

# Permutation of 0-2
pset.addPrimitive(Perm02_X_Func, [position], Perm02_X)
pset.addPrimitive(Perm02_O_Func, [position], Perm02_O)
pset.addPrimitive(Perm02_X_Func, [position], Perm02)
pset.addPrimitive(Perm02_O_Func, [position], Perm02)

# Permutation of 0-1
pset.addPrimitive(Perm01_X_Func, [positionf], Perm01_X)
pset.addPrimitive(Perm01_O_Func, [positionf], Perm01_O)
pset.addPrimitive(Perm01_X_Func, [positionf], Perm01)
pset.addPrimitive(Perm01_O_Func, [positionf], Perm01)

# Concrete of 0-2
pset.addPrimitive(Concrete_X_Func, [position, position], Concrete_X)
pset.addPrimitive(Concrete_O_Func, [position, position], Concrete_O)
pset.addPrimitive(Concrete_X_Func, [position, position], Concrete)
pset.addPrimitive(Concrete_O_Func, [position, position], Concrete)


pset.addPrimitive(posFunc, [position], position)
pset.addPrimitive(posfFunc, [positionf], positionf)
pset.addPrimitive(priorityFunc, [priority], priority)

pset.addTerminal(0, position)
pset.addTerminal(1, position)
pset.addTerminal(2, position)

pset.addTerminal(0, positionf)
pset.addTerminal(1, positionf)

pset.addTerminal(1, priority)
pset.addTerminal(2, priority)
pset.addTerminal(3, priority)
pset.addTerminal(4, priority)
pset.addTerminal(5, priority)
pset.addTerminal(6, priority)
pset.addTerminal(7, priority)
pset.addTerminal(8, priority)
pset.addTerminal(9, priority)
pset.addTerminal(10, priority)
pset.addTerminal(11, priority)


def cxOnePointBP(ind1, ind2):
    """Randomly select crossover point in each individual and exchange each
    subtree with the point as root between each individual.
    :param ind1: First tree participating in the crossover.
    :param ind2: Second tree participating in the crossover.
    :returns: A tuple of two trees.
    """
    if len(ind1) < 2 or len(ind2) < 2:
        # No crossover on single node tree
        return ind1, ind2

    # List all available primitive types in each individual
    types1 = defaultdict(list)
    types2 = defaultdict(list)

    for idx, node in enumerate(ind1[1:], 1):
        types1[node.ret].append(idx)
    for idx, node in enumerate(ind2[1:], 1):
        types2[node.ret].append(idx)
    # common_types = set(types1.keys()).intersection(set(types2.keys()))
    common_types = [btA, btB, btC]

    if len(common_types) > 0:
        func1 = toolbox.compile(expr=ind1)
        func_string1 = str(func1(0).root)
        func2 = toolbox.compile(expr=ind2)
        func_string2 = str(func2(0).root)
        try:
            anomalies1 = anomaly_dict[func_string1]
            anomalies2 = anomaly_dict[func_string2]
            prob_weights1 = [50 - (anomalies1[0] + anomalies1[1]) / 4, 50 - anomalies1[2], 40]
            prob_weights2 = [50 - (anomalies2[0] + anomalies2[1]) / 4, 50 - anomalies2[2], 40]
            type1_ = random.choices(list(common_types), weights=prob_weights1)
            type2_ = random.choices(list(common_types), weights=prob_weights2)

            index1_1 = random.choice(types1[type1_])
            index2_1 = random.choice(types2[type1_])
            slice1_1 = ind1.searchSubtree(index1_1)
            slice2_1 = ind2.searchSubtree(index2_1)

            index1_2 = random.choice(types1[type2_])
            index2_2 = random.choice(types2[type2_])
            slice1_2 = ind1.searchSubtree(index1_2)
            slice2_2 = ind2.searchSubtree(index2_2)

            ind2[slice2_1], ind1[slice1_2] = ind1[slice1_1], ind2[slice2_2]
            # ind1[slice1_2] = ind2[slice2_2]
        except:
            return ind1, ind2
            # type_ = random.choice(list(common_types))
            # type_ = btC

            # index1 = random.choice(types1[type_])
            # index2 = random.choice(types2[type_])

            # slice1 = ind1.searchSubtree(index1)
            # slice2 = ind2.searchSubtree(index2)
            # ind1[slice1], ind2[slice2] = ind2[slice2], ind1[slice1]

    return ind1, ind2


def mutUniformAnomaly(individual, expr, pset):
    func = toolbox.compile(expr=individual)
    func_string = str(func(0).root)
    try:
        anomalies = anomaly_dict[func_string]
        list_indv = list(individual)
        startA_index = 2
        startB_index = [i for i, node in enumerate(list_indv) if node.name == "btBFunc"][0]
        startC_index = [i for i, node in enumerate(list_indv) if node.name == "btCFunc"][0]
        a_range = list(range(startA_index, startB_index))
        b_range = list(range(startB_index, startC_index))
        c_range = list(range(startC_index, len(individual)))
        prob_weights = [(anomalies[0] + anomalies[1]) / 4, anomalies[2], 10]
        index_range = random.choices([a_range, b_range, c_range], weights=prob_weights)
        index = random.choice(index_range[0])
        slice_ = individual.searchSubtree(index)
        type_ = individual[index].ret
        individual[slice_] = expr(pset=pset, type_=type_)
        return individual,
    except:
        return individual,


def thread_score(blocks, misses, forks, requests):
    # high score is bad
    score = blocks / 2 + misses + forks + 50 - requests / 3
    return max(score, 1)


def mutUniformAnomalyV2(individual, expr, pset):
    func = toolbox.compile(expr=individual)
    func_string = str(func(0).root)
    try:
        anomalies = anomaly_dict_v2[func_string]
        list_indv = list(individual)
        index_list = [i for i, node in enumerate(list_indv) if node.name == "btAFunc" or node.name == "btBFunc" or node.name == "btCFunc"]
        index_list.append(len(list_indv))
        ranges_list = [list(range(index_list[i], index_list[i+1])) for i in range(10)]
        bthread_scores = [thread_score(anomalies[0][i], anomalies[1][i], anomalies[2][i], anomalies[3][i]) for i in range(10)]
        index_range = random.choices(ranges_list, weights=bthread_scores)
        index = random.choice(index_range[0])
        slice_ = individual.searchSubtree(index)
        type_ = individual[index].ret
        individual[slice_] = expr(pset=pset, type_=type_)
        return individual,
    except:
        return individual,


# Define Individual and Fitness
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax, pset=pset)

# Define Toolbox
toolbox = base.Toolbox()
toolbox.register("expr", gp.genGrow, pset=pset, min_=6, max_=6)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

# Plotting
# expr = toolbox.individual()
# nodes, edges, labels = gp.graph(expr)


# Define GP Operators
toolbox.register("evaluate", eval_generator)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", cxOnePointBP)
toolbox.register("expr_mut", gp.genGrow, min_=6, max_=6)
toolbox.register("mutate", mutUniformAnomalyV2, expr=toolbox.expr_mut, pset=pset)

executor = ThreadPoolExecutor()
toolbox.register("map", executor.map)


def real_time_plotter(name, plot):
    global AVERAGES, MAXIMUMS, MINIMUMS, MEDIANS, CURR_GEN, INDV_ID
    INDV_ID = 0
    # print(CURR_GEN)
    new_avg = numpy.mean(plot)
    new_max = numpy.max(plot)
    new_min = numpy.min(plot)
    new_median = numpy.median(plot)
    AVERAGES.append(new_avg)
    MAXIMUMS.append(new_max)
    MINIMUMS.append(new_min)
    MEDIANS.append(new_median)
    CURR_GEN = CURR_GEN + 1
    plt.plot(AVERAGES, label="Average", color="blue")
    plt.plot(MAXIMUMS, label="Max", color="green")
    plt.plot(MINIMUMS, label="Min", color="red")
    plt.plot(MEDIANS, label="Median", color="purple")
    plt.ylabel("Fitness")
    plt.suptitle(name)
    plt.legend()
    plt.savefig(name + '.png')
    plt.close()


# Save results
def save_results(log):
    x = 0


def time_stat(indv):
    global prev_time
    curr = time.time()
    diff = curr - prev_time
    prev_time = curr
    return diff

def run_experiment(cross_over_p, mutation_p, experiment_name):
    global prev_time
    pop = toolbox.population(n=POPULATION_SIZE)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    prev_time = time.time()
    stats.register("time", time_stat)
    stats.register("plot", lambda x: real_time_plotter(experiment_name, x))

    # Run experiment
    bla, log = algorithms.eaSimple(pop, toolbox, cxpb=cross_over_p, mutpb=mutation_p, ngen=NUMBER_OF_GENERATIONS,
                                   stats=stats)

    # Save results
    # save_results(log)
    df.to_csv(experiment_name + ".csv")
    clear_enviorment()
    return bla, log


def thread_check(arg):
    print(send_request("START" + arg))


def normalize_str(string: str) -> List[str]:
    str_norm = []
    last_c = None
    for c in string:
        if c.isalnum():
            if last_c.isalnum():
                str_norm[-1] += c
            else:
                str_norm.append(c)
        elif not c.isspace():
            str_norm.append(c)
        last_c = c
    return str_norm


# Generate abstract syntax tree from normalized input.
def get_ast(input_norm: List[str]) -> List[Any]:
    ast = []
    # Go through each element in the input:
    # - if it is an open parenthesis, find matching parenthesis and make recursive
    #   call for content in-between. Add the result as an element to the current list.
    # - if it is an atom, just add it to the current list.
    i = 0
    while i < len(input_norm):
        symbol = input_norm[i]
        if symbol == '(':
            list_content = []
            match_ctr = 1 # If 0, parenthesis has been matched.
            while match_ctr != 0:
                i += 1
                if i >= len(input_norm):
                    raise ValueError("Invalid input: Unmatched open parenthesis.")
                symbol = input_norm[i]
                if symbol == '(':
                    match_ctr += 1
                elif symbol == ')':
                    match_ctr -= 1
                if match_ctr != 0:
                    list_content.append(symbol)
            ast.append(get_ast(list_content))
        elif symbol == ')':
                raise ValueError("Invalid input: Unmatched close parenthesis.")
        else:
            try:
                ast.append(int(symbol))
            except ValueError:
                ast.append(symbol)
        i += 1
    return ast


def clear_enviorment():
    global AVERAGES, MAXIMUMS, MINIMUMS, MEDIANS, CURR_GEN, INDV_ID, anomaly_dict, anomaly_dict_v2, df
    AVERAGES = []
    MAXIMUMS = []
    MINIMUMS = []
    MEDIANS = []
    CURR_GEN = 1
    INDV_ID = 0
    anomaly_dict = {}
    anomaly_dict_v2 = {}
    df = pd.DataFrame({'Generation': [],
                       'Individual': [],
                       'Fitness': [],
                       'Wins': [],
                       'Losses': [],
                       'Draws': [],
                       'Block_Violations': [],
                       'Misses': [],
                       'Blocks': [],
                       'Deadlocks': [],
                       'Forks': [],
                       'Code': []})


if __name__ == "__main__":
    run_experiment(0.3, 0.2, "OldCxNewMutV2_1_cx30%_mt20%_V1")
    run_experiment(0.3, 0.2, "OldCxNewMutV2_1_cx30%_mt20%_V2")
    run_experiment(0.3, 0.2, "OldCxNewMutV2_1_cx30%_mt20%_V3")
    run_experiment(0.3, 0.2, "OldCxNewMutV2_1_cx30%_mt20%_V4")


