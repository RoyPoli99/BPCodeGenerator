import json
from concurrent.futures import thread

import matplotlib.pyplot as plt
import numpy
from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp
from deap.gp import PrimitiveSetTyped
from Client import calculate_fitness
from Client import send_request
from classes import *

# Define global arguments
NUMBER_OF_GENERATIONS = 200
POPULATION_SIZE = 1000
AVERAGES = []
MAXIMUMS = []
MINIMUMS = []


# Send to BPServer to evaluate
def eval_generator(individual):
    func = toolbox.compile(expr=individual)
    json_string = str(func(0).root)
    json_obj = json.loads(json_string)
    fitness = calculate_fitness(json_obj)
    return fitness,


pset = PrimitiveSetTyped("main", [], int)

# Define CFG


# Define Individual and Fitness
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax, pset=pset)

# Define Toolbox
toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=15)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

# Define GP Operators
toolbox.register("evaluate", eval_generator)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)


def real_time_plotter(name, plot):
    global AVERAGES, MAXIMUMS, MINIMUMS
    new_avg = numpy.mean(plot)
    new_max = numpy.max(plot)
    new_min = numpy.min(plot)
    AVERAGES.append(new_avg)
    MAXIMUMS.append(new_max)
    MINIMUMS.append(new_min)
    plt.plot(AVERAGES, label="Average", color="blue")
    plt.plot(MAXIMUMS, label="Max", color="green")
    plt.plot(MINIMUMS, label="Min", color="red")
    plt.ylabel("Fitness")
    plt.suptitle(name)
    plt.legend()
    plt.savefig('real_time_graph.png')
    plt.close()


# Save results
def save_results(log):
    x = 0


def run_experiment(cross_over_p, mutation_p, experiment_name):
    pop = toolbox.population(POPULATION_SIZE)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    stats.register("plot", lambda x: real_time_plotter(experiment_name, x))

    # Run experiment
    bla, log = algorithms.eaSimple(pop, toolbox, cxpb=cross_over_p, mutpb=mutation_p, ngen=NUMBER_OF_GENERATIONS,
                                   stats=stats, halloffame=hof)

    # Save results
    save_results(log)


def thread_check(arg):
    print(send_request("START" + arg))


if __name__ == "__main__":
    # run_experiment(0, 0, "placeholder")
    hotncold = """bp.registerBThread("HotBt", function() {
        bp.sync({request:bp.Event("hotEvent")});
        bp.sync({request:bp.Event("hotEvent")});
        bp.sync({request:bp.Event("hotEvent")});
    });

    bp.registerBThread("ColdBt", function() {
        bp.sync({request:bp.Event("coldEvent")});
        bp.sync({request:bp.Event("coldEvent")});
        bp.sync({request:bp.Event("coldEvent")});
    });

    bp.registerBThread("AlternatorBt", function() {
        for(var i = 0; i < 3; i++) {
            bp.sync({waitFor:bp.Event("coldEvent"), block:bp.Event("hotEvent")});
            bp.sync({waitFor:bp.Event("hotEvent"), block:bp.Event("coldEvent")});
        }
        bp.sync({request:bp.Event("allDone")});
    });"""
    print("start")
    with thread.ThreadPoolExecutor(max_workers=4) as e:
        e.submit(thread_check, hotncold)
        e.submit(thread_check, hotncold)
        e.submit(thread_check, hotncold)
        e.submit(thread_check, hotncold)
    print("finish")
