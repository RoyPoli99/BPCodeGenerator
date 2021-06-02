import inspect
import itertools
import random
import sys
import threading
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
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
NUMBER_OF_GENERATIONS = 200
POPULATION_SIZE = 100
AVERAGES = []
MAXIMUMS = []
MINIMUMS = []
MEDIANS = []
CURR_GEN = 1
INDV_ID = 0

lock = threading.Lock()
prev_time = 0


df = pd.DataFrame({'Generation': [],
                   'Individual': [],
                   'BThreads_Number': [],
                   'Fitness': [],
                   'Wins': [],
                   'Losses': [],
                   'Draws': [],
                   'Block_Violations': [],
                   'Misses': [],
                   'Blocks': [],
                   'Deadlocks': [],
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


def document_individual(individual, curr_id, bthreads_num, fitness, wins, draws, losses, blocks_v, misses, blocks, deadlocks, code):
    # tree
    # nodes, edges, labels = gp.graph(individual)
    # g = pgv.AGraph()
    # g.add_nodes_from(nodes)
    # g.add_edges_from(edges)
    # g.layout(prog="dot")
    # for i in nodes:
    #    n = g.get_node(i)
    #    n.attr["label"] = labels[i]
    # img_name = "gen_" + str(CURR_GEN) + ".png"
    # folder_name = "../trees/Individual" + str(curr_id)
    # if not os.path.exists(folder_name):
    #    os.makedirs(folder_name)
    # g.draw(folder_name + "/" + img_name)
    # stats
    with lock:
        df.loc[len(df)] = [CURR_GEN, curr_id, bthreads_num, fitness, wins, draws, losses, blocks_v, misses, blocks, deadlocks, code]


# Send to BPServer to evaluate
def eval_generator(individual):
    global INDV_ID
    func = toolbox.compile(expr=individual)
    func_string = str(func(0).root)
    indv = bp_pb2.Individual()
    indv.generation = CURR_GEN
    bthread_num = func(0).root.num_of_bthreads
    with lock:
        INDV_ID += 1
        indv.id = INDV_ID
    indv.code.code = func_string
    results = send_proto_request(indv)
    fitness = results_to_fitness(results.wins, results.misses, results.blocks, results.blocks_violations, results.deadlocks)
    document_individual(individual, indv.id, bthread_num, fitness, results.wins, results.draws, results.losses, results.blocks_violations, results.misses, results.blocks, results.deadlocks, func_string)
    return fitness,


def generate_safe(pset, min_, max_, terminal_types, type_=None):
    if type_ is None:
        type_ = pset.ret
    expr = []
    height = random.randint(min_, max_)
    stack = [(0, type_)]
    while len(stack) != 0:
        depth, type_ = stack.pop()

        if type_ in terminal_types:
            try:
                term = random.choice(pset.terminals[type_])
            except IndexError:
                _, _, traceback = sys.exc_info()
                raise IndexError("The gp.generate function tried to add "
                                 "a terminal of type '%s', but there is "
                                 "none available." % (type_,)).with_traceback(traceback)
            if inspect.isclass(term):
                term = term()
            expr.append(term)
        else:
            try:
                # Might not be respected if there is a type without terminal args
                if height <= depth or (depth >= min_ and random.random() < pset.terminalRatio):
                    primitives_with_only_terminal_args = [p for p in pset.primitives[type_] if
                                                          all([arg in terminal_types for arg in p.args])]

                    if len(primitives_with_only_terminal_args) == 0:
                        prim = random.choice(pset.primitives[type_])
                    else:
                        prim = random.choice(primitives_with_only_terminal_args)
                else:
                    prim = random.choice(pset.primitives[type_])
            except IndexError:
                _, _, traceback = sys.exc_info()
                raise IndexError("The gp.generate function tried to add "
                                 "a primitive of type '%s', but there is "
                                 "none available." % (type_,)).with_traceback(traceback)
            expr.append(prim)
            for arg in reversed(prim.args):
                stack.append((depth + 1, arg))
    return expr


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
    #if ind1.root.ret == __type__:
        # Not STGP optimization
     #   types1[__type__] = xrange(1, len(ind1))
     #   types2[__type__] = xrange(1, len(ind2))
     #   common_types = [__type__]
    #else:
    for idx, node in enumerate(ind1[1:], 1):
        types1[node.ret].append(idx)
    for idx, node in enumerate(ind2[1:], 1):
        types2[node.ret].append(idx)
    common_types = set(types1.keys()).intersection(set(types2.keys()))

    if len(common_types) > 0:
        # type_ = random.choice(list(common_types))
        type_ = btC

        index1 = random.choice(types1[type_])
        index2 = random.choice(types2[type_])

        slice1 = ind1.searchSubtree(index1)
        slice2 = ind2.searchSubtree(index2)
        ind1[slice1], ind2[slice2] = ind2[slice2], ind1[slice1]

    return ind1, ind2


def mutUniformBP(individual, expr, pset):
    """Randomly select a point in the tree *individual*, then replace the
    subtree at that point as a root by the expression generated using method
    :func:`expr`.
    :param individual: The tree to be mutated.
    :param expr: A function object that can generate an expression when
                 called.
    :returns: A tuple of one tree.
    """
    index = random.randrange(len(individual))
    slice_ = individual.searchSubtree(index)
    type_ = individual[index].ret
    individual[slice_] = expr(pset=pset, type_=type_)
    return individual,


# Grammar Setup
pset = PrimitiveSetTyped("main", [root], root_wrapper)
pset.addPrimitive(root_wrapperFunc, [root], root_wrapper)
pset.addPrimitive(rootFunc, [btGroup, btGroup, btGroup, btGroup, btGroup, btGroup, btGroup, btGroup, btGroup, btGroup], root)

# bt Group
#pset.addPrimitive(btGroupExpand, [btGroup, btGroup], btGroup)
pset.addPrimitive(btGroupExpand, [btGroup, btGroup], btGroup)
pset.addPrimitive(btGroupFunc, [btC], btGroup)
pset.addPrimitive(btGroupFunc, [btC, btC, btC], btGroup)
pset.addPrimitive(btGroupFunc, [btC, btC, btC, btC, btC], btGroup)
#pset.addPrimitive(btGroupFunc, [btC, btC, btC, btC, btC, btC, btC, btC, btC, btC], btGroup)

# BThreads
pset.addPrimitive(btCFunc, [while_trueC], btC)

# Loop for BT3
# 0 Waits
pset.addPrimitive(while_trueC_0, [requestC], while_trueC)
# 1 Waits
pset.addPrimitive(while_trueC_1, [waitC, requestC], while_trueC)
# 2 Waits
pset.addPrimitive(while_trueC_2, [waitC, waitC, requestC], while_trueC)

# Wait Concrete
pset.addPrimitive(waitC_1, [Concrete], waitC)
pset.addPrimitive(waitC_2, [Concrete, Concrete], waitC)
pset.addPrimitive(waitC_3, [Concrete, Concrete, Concrete], waitC)
pset.addPrimitive(waitC_4, [Concrete, Concrete, Concrete, Concrete], waitC)

# Request Concrete
pset.addPrimitive(requestC_1, [Concrete_O, priority], requestC)
pset.addPrimitive(requestC_2, [Concrete_O, Concrete_O, priority], requestC)
pset.addPrimitive(requestC_3, [Concrete_O, Concrete_O, Concrete_O, priority], requestC)
pset.addPrimitive(requestC_4, [Concrete_O, Concrete_O, Concrete_O, Concrete_O, priority], requestC)


# Concrete
pset.addPrimitive(Concrete_X_Func, [position, position], Concrete_X)
pset.addPrimitive(Concrete_O_Func, [position, position], Concrete_O)
pset.addPrimitive(Concrete_X_Func, [position, position], Concrete)
pset.addPrimitive(Concrete_O_Func, [position, position], Concrete)


pset.addPrimitive(posFunc, [position], position)
pset.addPrimitive(posfFunc, [positionf], positionf)
pset.addPrimitive(priorityFunc, [priority], priority)
pset.addPrimitive(b_numFunc, [b_num], b_num)

pset.addTerminal(0, position)
pset.addTerminal(1, position)
pset.addTerminal(2, position)

pset.addTerminal(0, positionf)
pset.addTerminal(1, positionf)

pset.addEphemeralConstant("rand100", lambda: random.randint(0, 99), priority)
pset.addEphemeralConstant("rand50_150", lambda: random.randint(50, 150), b_num)



# Define Individual and Fitness
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax, pset=pset)

# Define Toolbox
toolbox = base.Toolbox()
terminal_types = [positionf, position, priority]
toolbox.register("expr", generate_safe, pset=pset, min_=4, max_=8, terminal_types=terminal_types)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

# Plotting
# expr = toolbox.individual()
# nodes, edges, labels = gp.graph(expr)


# Define GP Operators
toolbox.register("evaluate", eval_generator)
# toolbox.register("select", tools.selRoulette)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", cxOnePointBP)
toolbox.register("expr_mut", generate_safe, min_=4, max_=8, terminal_types=terminal_types)
toolbox.register("mutate", mutUniformBP, expr=toolbox.expr_mut, pset=pset)

#executor = ThreadPoolExecutor()
#toolbox.register("map", executor.map)


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
    hof = tools.HallOfFame(3)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    prev_time = time.time()
    stats.register("time", time_stat)
    stats.register("plot", lambda x: real_time_plotter(experiment_name, x))

    # Run experiment
    #bla, log = algorithms.eaSimple(pop, toolbox, cxpb=cross_over_p, mutpb=mutation_p, ngen=NUMBER_OF_GENERATIONS,
    #                               stats=stats)

    bla, log = eaSimpleWithElitism(pop, toolbox, cxpb=cross_over_p, mutpb=mutation_p, ngen=NUMBER_OF_GENERATIONS,
                                   stats=stats, halloffame=hof)

    # Save results
    # save_results(log)
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


def eaSimpleWithElitism(population, toolbox, cxpb, mutpb, ngen, stats=None,
             halloffame=None, verbose=__debug__):
    """This algorithm is similar to DEAP eaSimple() algorithm, with the modification that
    halloffame is used to implement an elitism mechanism. The individuals contained in the
    halloffame are directly injected into the next generation and are not subject to the
    genetic operators of selection, crossover and mutation.
    """
    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    if halloffame is None:
        raise ValueError("halloffame parameter must not be empty!")

    halloffame.update(population)
    hof_size = len(halloffame.items) if halloffame.items else 0

    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, nevals=len(invalid_ind), **record)
    if verbose:
        print(logbook.stream)

    # Begin the generational process
    for gen in range(1, ngen + 1):

        # Select the next generation individuals
        offspring = toolbox.select(population, len(population) - hof_size)

        # Vary the pool of individuals
        offspring = algorithms.varAnd(offspring, toolbox, cxpb, mutpb)

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # add the best back to population:
        offspring.extend(halloffame.items)

        # Update the hall of fame with the generated individuals
        halloffame.update(offspring)

        # Replace the current population by the offspring
        population[:] = offspring

        # Append the current generation statistics to the logbook
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)
        if verbose:
            print(logbook.stream)

    return population, logbook


if __name__ == "__main__":
    print("start")
    ip = socket.gethostbyname(socket.gethostname())
    print("Python IP - " + ip)

    bla, log = run_experiment(0.7, 0.001, "TTT SimulationRunOrg14")
    df.to_csv("log14.csv")

