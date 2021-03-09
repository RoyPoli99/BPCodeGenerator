import threading
import time
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
import numpy
from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp
from deap.gp import PrimitiveSetTyped
from Client import calculate_fitness, send_stop, send_proto_request
from Client import send_request
from TTTclasses import *
import bp_pb2
import socket

# Define global arguments
NUMBER_OF_GENERATIONS = 150
POPULATION_SIZE = 100
AVERAGES = []
MAXIMUMS = []
MINIMUMS = []
MEDIANS = []
CURR_GEN = 0
INDV_ID = 0

lock = threading.Lock()
prev_time = 0

def results_to_fitness(wins, draws, losses, blocks, misses):
    if CURR_GEN >= 100:
        return 10 * draws
    return 10 * (3 * wins + draws - losses - blocks - 2 * misses)

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
    fitness = results_to_fitness(results.wins, results.draws, results.losses, results.blocks, results.misses)
    return fitness,

pset = PrimitiveSetTyped("main", [root], root_wrapper)
pset.addPrimitive(root_wrapperFunc, [root], root_wrapper)
pset.addPrimitive(rootFunc, [btl, btl, btf, btf, btf, btf, btf, bt, bt, bt], root)

pset.addPrimitive(btlFunc3, [while_truel3], btl)

pset.addPrimitive(btfFunc1, [while_truef1], btf)
pset.addPrimitive(btfFunc2, [while_truef2], btf)
pset.addPrimitive(btfFunc3, [while_truef3], btf)

pset.addPrimitive(btFunc, [whiletrue], bt)

pset.addPrimitive(while_truel3Func1, [wait_forl, wait_forl, requestl1], while_truel3)
pset.addPrimitive(while_truel3Func2, [wait_forl, wait_forl, requestl2], while_truel3)
pset.addPrimitive(while_truel3Func3, [wait_forl, wait_forl, requestl3], while_truel3)
pset.addPrimitive(while_truel3Func4, [wait_forl, wait_forl, requestl4], while_truel3)

pset.addPrimitive(while_truef1Func1, [request1], while_truef1)
pset.addPrimitive(while_truef1Func2, [request2], while_truef1)
pset.addPrimitive(while_truef1Func3, [request3], while_truef1)
pset.addPrimitive(while_truef1Func4, [request4], while_truef1)

pset.addPrimitive(while_truef2Func1, [wait_forf, request1], while_truef2)
pset.addPrimitive(while_truef2Func2, [wait_forf, request2], while_truef2)
pset.addPrimitive(while_truef2Func3, [wait_forf, request3], while_truef2)
pset.addPrimitive(while_truef2Func4, [wait_forf, request4], while_truef2)

pset.addPrimitive(while_truef3Func1, [wait_forf, wait_forf, request1], while_truef3)
pset.addPrimitive(while_truef3Func2, [wait_forf, wait_forf, request2], while_truef3)
pset.addPrimitive(while_truef3Func3, [wait_forf, wait_forf, request3], while_truef3)
pset.addPrimitive(while_truef3Func4, [wait_forf, wait_forf, request4], while_truef3)

pset.addPrimitive(while_trueFunc1, [request1], whiletrue)
pset.addPrimitive(while_trueFunc2, [request2], whiletrue)
pset.addPrimitive(while_trueFunc3, [request3], whiletrue)
pset.addPrimitive(while_trueFunc4, [request4], whiletrue)

pset.addPrimitive(wait_forlFuncX, [Xl], wait_forl)
pset.addPrimitive(wait_forlFuncO, [Ol], wait_forl)

pset.addPrimitive(wait_forfFuncX, [Xf], wait_forf)

pset.addPrimitive(request1Func, [O, priority], request1)
pset.addPrimitive(request2Func, [O, O, priority], request2)
pset.addPrimitive(request3Func, [O, O, O, priority], request3)
pset.addPrimitive(request4Func, [O, O, O, O, priority], request4)

pset.addPrimitive(requestl1Func, [Ol, priority], requestl1)
pset.addPrimitive(requestl2Func, [Ol, Ol, priority], requestl2)
pset.addPrimitive(requestl3Func, [Ol, Ol, Ol, priority], requestl3)
pset.addPrimitive(requestl4Func, [Ol, Ol, Ol, Ol, priority], requestl4)

pset.addPrimitive(xlFunc, [position, position], Xl)
pset.addPrimitive(olFunc, [position, position], Ol)

pset.addPrimitive(xfFunc, [positionf, positionf], Xf)

pset.addPrimitive(oFunc, [position, position], O)

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


# Define Individual and Fitness
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax, pset=pset)

# Define Toolbox
toolbox = base.Toolbox()
toolbox.register("expr", gp.genGrow, pset=pset, min_=6, max_=6)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

# Define GP Operators
toolbox.register("evaluate", eval_generator)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genGrow, min_=6, max_=6)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

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


def time_stat():
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
    stats.register("time", lambda x: time.time() - prev_time)
    stats.register("plot", lambda x: real_time_plotter(experiment_name, x))

    # Run experiment
    bla, log = algorithms.eaSimple(pop, toolbox, cxpb=cross_over_p, mutpb=mutation_p, ngen=NUMBER_OF_GENERATIONS,
                                   stats=stats)

    # Save results
    # save_results(log)
    return bla, log


def thread_check(arg):
    print(send_request("START" + arg))


if __name__ == "__main__":
    print("start")
    ip = socket.gethostbyname(socket.gethostname())
    print("Python IP - " + ip)

    bla, log = run_experiment(0.7, 0.001, "TTT SimulationRunOrg")
    # bla, log = run_experiment(0.7, 0.005, "TTT Simulation0.005")
    # bla, log = run_experiment(0.7, 0.01, "TTT Simulation0.01")
    # send_stop()

    # with thread.ThreadPoolExecutor(max_workers=4) as e:
    #     e.submit(thread_check, hotncold)
    #     e.submit(thread_check, hotncold)
    #     e.submit(thread_check, hotncold)
    #     e.submit(thread_check, hotncold)
    #kill server
    # print("finish")
