import inspect
import math
import sys
import threading
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import random
from typing import List, Any
import matplotlib.pyplot as plt
import numpy
import numpy as np
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
NUMBER_OF_GENERATIONS = 150
POPULATION_SIZE = 100
AVERAGES = []
MAXIMUMS = []
MINIMUMS = []
MEDIANS = []
CURR_GEN = 1
INDV_ID = 0
anomaly_dict = {}
anomaly_dict_v2 = {}
anomaly_map = {}
exp_type = "BP"

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
                   'Fork_Violations': [],
                   'Code': []})


def exp_func(x):
    num = 1 - math.pow(math.e, -x)
    den = 1 - math.pow(math.e, -1)
    return num / den


def exp_func2(x):
    return 2 * math.pow(x, 2)


def results_to_fitness(wins, wins_misses, blocks, block_misses, forks, forks_misses, deadlocks):
    w_win, w_block = 0.3, 0.7
    try:
        win_stat = wins / (wins + wins_misses)
    except:
        win_stat = 0
    try:
        block_stat = blocks / (blocks + block_misses)
    except:
        block_stat = 0
    try:
        fork_stat = forks / (forks + forks_misses)
    except:
        fork_stat = 0
    return 100 * (w_win * exp_func(win_stat) + w_block * exp_func(block_stat)) - deadlocks
    # return 100 * ((win_stat + block_stat * block_weight) / 3) - deadlocks


def document_individual(individual, curr_id, fitness, wins, draws, losses, blocks_v, misses, blocks, deadlocks, forks, forks_violations, code):
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
        df.loc[len(df)] = [CURR_GEN, curr_id, fitness, wins, losses, draws, blocks_v, misses, blocks, deadlocks, forks, forks_violations, code]


def parse_results_lists(result_list):
    sets_layer = list()
    for item in result_list._values:
        threads_layer = list()
        for inner_item in item.foo._values:
            inputs_layer = list()
            for inner_inner_item in inner_item.foo._values:
                inputs_layer.append(inner_inner_item)
            threads_layer.append(inputs_layer)
        sets_layer.append(threads_layer)
    return sets_layer


def map_anomalies(results, func_string):
    anomaly_map[func_string] = {"win_o": parse_results_lists(results.win_o),
                               "win_v": parse_results_lists(results.win_v),
                               "block_o": parse_results_lists(results.block_o),
                               "block_v": parse_results_lists(results.block_v),
                               "fork_o": parse_results_lists(results.fork_o),
                               "fork_v": parse_results_lists(results.fork_v),
                               "requests": parse_results_lists(results.fork_v)}


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
    map_anomalies(results, func_string)
    x = anomaly_map
    anomaly_dict[func_string] = (results.blocks_violations, results.misses, results.forks)
    anomaly_dict_v2[func_string] = (results.block_v, results.win_v, results.fork_v, results.requests)
    fitness = results_to_fitness(results.wins, results.misses, results.blocks, results.blocks_violations, results.forks, results.forks_violations, results.deadlocks)
    document_individual(individual, indv.id, fitness, results.wins, results.draws, results.losses, results.blocks_violations, results.misses, results.blocks, results.deadlocks, results.forks, results.forks_violations, func_string)
    return fitness,


# Grammar Setup
pset = PrimitiveSetTyped("main", [root], root_wrapper)
pset.addPrimitive(root_wrapper_func, [root], root_wrapper)
pset.addPrimitive(root_func, [CTX], root)
pset.addPrimitive(root_func, [CTX, CTX], root)
pset.addPrimitive(root_func, [CTX, CTX, CTX], root)
pset.addPrimitive(root_func, [CTX, CTX, CTX, CTX], root)
pset.addPrimitive(root_func, [CTX, CTX, CTX, CTX, CTX], root)
pset.addPrimitive(root_func, [CTX, CTX, CTX, CTX, CTX, CTX], root)
pset.addPrimitive(root_func, [CTX, CTX, CTX, CTX, CTX, CTX, CTX], root)
pset.addPrimitive(root_func, [CTX, CTX, CTX, CTX, CTX, CTX, CTX, CTX], root)
pset.addPrimitive(root_func, [CTX, CTX, CTX, CTX, CTX, CTX, CTX, CTX, CTX], root)
pset.addPrimitive(root_func, [CTX, CTX, CTX, CTX, CTX, CTX, CTX, CTX, CTX, CTX], root)

# Define lists of classes
single_input_arrays = [SingleInput1, SingleInput2, SingleInput3, SingleInput4, SingleInput5, SingleInput6, SingleInput7, SingleInput8, SingleInput9]
behaviors_set = [BehaviorSet1, BehaviorSet2, BehaviorSet3, BehaviorSet4, BehaviorSet5, BehaviorSet6, BehaviorSet7, BehaviorSet8, BehaviorSet9]
behaviors = [Behavior1, Behavior2, Behavior3, Behavior4, Behavior5, Behavior6, Behavior7, Behavior8, Behavior9]
events = [Event1, Event2, Event3, Event4, Event5, Event6, Event7, Event8, Event9]
Xevents = [XEvent1, XEvent2, XEvent3, XEvent4, XEvent5, XEvent6, XEvent7, XEvent8, XEvent9]
Oevents = [OEvent1, OEvent2, OEvent3, OEvent4, OEvent5, OEvent6, OEvent7, OEvent8, OEvent9]
requests = [Request1, Request2, Request3, Request4, Request5, Request6, Request7, Request8, Request9]
waits = [Wait1, Wait2, Wait3, Wait4, Wait5, Wait6, Wait7, Wait8, Wait9]
indexes = [Index1, Index2, Index3, Index4, Index5, Index6, Index7, Index8, Index9]
behavior_set_funcs = [behavior_set_func1, behavior_set_func2, behavior_set_func3, behavior_set_func4, behavior_set_func5, behavior_set_func6, behavior_set_func7, behavior_set_func8, behavior_set_func9]
behavior_funcs = [behavior_func1, behavior_func2, behavior_func3, behavior_func4, behavior_func5, behavior_func6, behavior_func7, behavior_func8, behavior_func9]
request_funcs = [request_func1, request_func2, request_func3, request_func4, request_func5, request_func6, request_func7, request_func8, request_func9]
wait_funcs = [wait_func1, wait_func2, wait_func3, wait_func4, wait_func5, wait_func6, wait_func7, wait_func8, wait_func9]
event_funcs = [event_func1, event_func2, event_func3, event_func4, event_func5, event_func6, event_func7, event_func8, event_func9]
x_event_funcs = [x_event_func1, x_event_func2, x_event_func3, x_event_func4, x_event_func5, x_event_func6, x_event_func7, x_event_func8, x_event_func9]
o_event_funcs = [o_event_func1, o_event_func2, o_event_func3, o_event_func4, o_event_func5, o_event_func6, o_event_func7, o_event_func8, o_event_func9]

# Define contexts
# 1-9 arrays of cells and a behavior groups corresponding to the number of cells and arrays
for single_input_array, behavior_set in zip(single_input_arrays, behaviors_set):
    pset.addPrimitive(ctx_func, [behavior_set, single_input_array], CTX)
    pset.addPrimitive(ctx_func, [behavior_set, single_input_array, single_input_array], CTX)
    pset.addPrimitive(ctx_func, [behavior_set, single_input_array, single_input_array, single_input_array], CTX)
    pset.addPrimitive(ctx_func, [behavior_set, single_input_array, single_input_array, single_input_array, single_input_array], CTX)
    pset.addPrimitive(ctx_func, [behavior_set, single_input_array, single_input_array, single_input_array, single_input_array, single_input_array], CTX)
    pset.addPrimitive(ctx_func, [behavior_set, single_input_array, single_input_array, single_input_array, single_input_array, single_input_array, single_input_array], CTX)
    pset.addPrimitive(ctx_func, [behavior_set, single_input_array, single_input_array, single_input_array, single_input_array, single_input_array, single_input_array, single_input_array], CTX)
    pset.addPrimitive(ctx_func, [behavior_set, single_input_array, single_input_array, single_input_array, single_input_array, single_input_array, single_input_array, single_input_array, single_input_array], CTX)
    pset.addPrimitive(ctx_func, [behavior_set, single_input_array, single_input_array, single_input_array, single_input_array, single_input_array, single_input_array, single_input_array, single_input_array, single_input_array], CTX)


# Define input arrays
# 1-9 cells in every array
pset.addPrimitive(single_input_func1, [Cell], SingleInput1)
pset.addPrimitive(single_input_func2, [Cell, Cell], SingleInput2)
pset.addPrimitive(single_input_func3, [Cell, Cell, Cell], SingleInput3)
pset.addPrimitive(single_input_func4, [Cell, Cell, Cell, Cell], SingleInput4)
pset.addPrimitive(single_input_func5, [Cell, Cell, Cell, Cell, Cell], SingleInput5)
pset.addPrimitive(single_input_func6, [Cell, Cell, Cell, Cell, Cell, Cell], SingleInput6)
pset.addPrimitive(single_input_func7, [Cell, Cell, Cell, Cell, Cell, Cell, Cell], SingleInput7)
pset.addPrimitive(single_input_func8, [Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell], SingleInput8)
pset.addPrimitive(single_input_func9, [Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell], SingleInput9)

# Define cell
# Made out of 2 positions
pset.addPrimitive(cell_func, [Position, Position], Cell)

# Define positions
# 0-2 positions on the board
pset.addPrimitive(position_func, [Position], Position)
pset.addTerminal(0, Position)
pset.addTerminal(1, Position)
pset.addTerminal(2, Position)

# Define behavior sets
# Each set contains 1-5 behaviors:
for behavior_set, behavior, behavior_set_func in zip(behaviors_set, behaviors, behavior_set_funcs):
    pset.addPrimitive(behavior_set_func, [behavior], behavior_set)
    pset.addPrimitive(behavior_set_func, [behavior, behavior], behavior_set)
    pset.addPrimitive(behavior_set_func, [behavior, behavior, behavior], behavior_set)
    pset.addPrimitive(behavior_set_func, [behavior, behavior, behavior, behavior], behavior_set)
    pset.addPrimitive(behavior_set_func, [behavior, behavior, behavior, behavior, behavior], behavior_set)

# Define behaviors
# Each behavior has access to only its number of cells
# 0-2 Waits - 1 Request
for request, wait, behavior, behavior_func in zip(requests, waits, behaviors, behavior_funcs):
    pset.addPrimitive(behavior_func, [request], behavior)
    pset.addPrimitive(behavior_func, [request, wait], behavior)
    pset.addPrimitive(behavior_func, [request, wait, wait], behavior)

# Define statements
# Each statement can only use 1-4 events
for request, Oevent, request_func in zip(requests, Oevents, request_funcs):
    pset.addPrimitive(request_func, [Priority, Oevent], request)
    pset.addPrimitive(request_func, [Priority, Oevent, Oevent], request)
    pset.addPrimitive(request_func, [Priority, Oevent, Oevent, Oevent], request)
    pset.addPrimitive(request_func, [Priority, Oevent, Oevent, Oevent, Oevent], request)
for wait, event, wait_func in zip(waits, events, wait_funcs):
    pset.addPrimitive(wait_func, [event], wait)
    pset.addPrimitive(wait_func, [event, event], wait)
    pset.addPrimitive(wait_func, [event, event, event], wait)
    pset.addPrimitive(wait_func, [event, event, event, event], wait)

# Define events
for event, Xevent, Oevent, event_func in zip(events, Xevents, Oevents, event_funcs):
    pset.addPrimitive(event_func, [Xevent], event)
    pset.addPrimitive(event_func, [Oevent], event)
for indx, Xevent, Oevent, x_event_func, o_event_func in zip(indexes, Xevents, Oevents, x_event_funcs, o_event_funcs):
    pset.addPrimitive(x_event_func, [indx], Xevent)
    pset.addPrimitive(o_event_func, [indx], Oevent)
    pset.addPrimitive(index_func, [indx], indx)

# Define indexes for behavior statements
# Each statement can only use its available number of inputs
pset.addTerminal(0, Index1)

pset.addTerminal(0, Index2)
pset.addTerminal(1, Index2)

pset.addTerminal(0, Index3)
pset.addTerminal(1, Index3)
pset.addTerminal(2, Index3)

pset.addTerminal(0, Index4)
pset.addTerminal(1, Index4)
pset.addTerminal(2, Index4)
pset.addTerminal(3, Index4)

pset.addTerminal(0, Index5)
pset.addTerminal(1, Index5)
pset.addTerminal(2, Index5)
pset.addTerminal(3, Index5)
pset.addTerminal(4, Index5)

pset.addTerminal(0, Index6)
pset.addTerminal(1, Index6)
pset.addTerminal(2, Index6)
pset.addTerminal(3, Index6)
pset.addTerminal(4, Index6)
pset.addTerminal(5, Index6)

pset.addTerminal(0, Index7)
pset.addTerminal(1, Index7)
pset.addTerminal(2, Index7)
pset.addTerminal(3, Index7)
pset.addTerminal(4, Index7)
pset.addTerminal(5, Index7)
pset.addTerminal(6, Index7)

pset.addTerminal(0, Index8)
pset.addTerminal(1, Index8)
pset.addTerminal(2, Index8)
pset.addTerminal(3, Index8)
pset.addTerminal(4, Index8)
pset.addTerminal(5, Index8)
pset.addTerminal(6, Index8)
pset.addTerminal(7, Index8)

pset.addTerminal(0, Index9)
pset.addTerminal(1, Index9)
pset.addTerminal(2, Index9)
pset.addTerminal(3, Index9)
pset.addTerminal(4, Index9)
pset.addTerminal(5, Index9)
pset.addTerminal(6, Index9)
pset.addTerminal(7, Index9)
pset.addTerminal(8, Index9)

# Define priorities
pset.addPrimitive(priority_func, [Priority], Priority)
pset.addTerminal(1, Priority)
pset.addTerminal(2, Priority)
pset.addTerminal(3, Priority)
pset.addTerminal(4, Priority)
pset.addTerminal(5, Priority)
pset.addTerminal(6, Priority)
pset.addTerminal(7, Priority)
pset.addTerminal(8, Priority)
pset.addTerminal(9, Priority)
pset.addTerminal(10, Priority)
pset.addTerminal(11, Priority)

terminal_types = indexes + [Priority, Position]



def calculate_set_scores(thread_scores):
    x = [sum(set_anomalies) for set_anomalies in thread_scores]
    return [sum(set_anomalies) for set_anomalies in thread_scores]


def calculate_thread_scores(anomalies, weights):
    thread_scores = np.zeros((10, 5))
    for anomaly, weight in zip(anomalies, weights):
        for i, anomaly_set in enumerate(anomaly):
            for j, anomaly_thread in enumerate(anomaly_set):
                thread_scores[i][j] += sum(anomaly_thread) * weight
    return np.where(thread_scores < 0, 1, thread_scores)


def calculate_context_scores(anomalies, weights):
    context_scores = np.zeros((10, 10))
    for anomaly, weight in zip(anomalies, weights):
        for i, anomaly_set in enumerate(anomaly):
            for anomaly_thread in anomaly_set:
                for j, anomaly_context in enumerate(anomaly_thread):
                    context_scores[i][j] += anomaly_context * weight
    return np.where(context_scores < 0, 1, context_scores)


def get_index(individual, func_string, good_index):
    anomalies = anomaly_map[func_string]
    list_indv = list(individual)
    if good_index:
        anomaly_weights = [2, -2, 1, -1, 0.25]
    else:
        anomaly_weights = [-2, 2, -1, 1, -0.25]


    set_indexes = [i for i, node in enumerate(list_indv) if node.name == "ctx_func"] + [len(list_indv)]
    thread_indexes = [i for i, node in enumerate(list_indv) if node.name.startswith("behavior_func")]
    context_indexes = [i for i, node in enumerate(list_indv) if node.name.startswith("single_input_func")]

    thread_scores = calculate_thread_scores(
        [anomalies["win_o"], anomalies["win_v"], anomalies["block_o"], anomalies["block_v"], anomalies["requests"]],
        anomaly_weights)
    context_scores = calculate_context_scores(
        [anomalies["win_o"], anomalies["win_v"], anomalies["block_o"], anomalies["block_v"], anomalies["requests"]],
        anomaly_weights)
    set_scores = calculate_set_scores(thread_scores)

    chosen_set = random.choices(range(10), weights=set_scores)[0]
    chosen_thread = random.choices(range(5), weights=thread_scores[chosen_set])[0]
    chosen_context = random.choices(range(10), weights=context_scores[chosen_set])[0]

    chosen_set_range = list(range(set_indexes[chosen_set], set_indexes[chosen_set + 1]))
    relevant_contexts = [x for x in context_indexes if x in chosen_set_range] + [set_indexes[chosen_set + 1]]
    relevant_threads = [x for x in thread_indexes if x in chosen_set_range] + [relevant_contexts[0]]
    chosen_thread_range = list(range(relevant_threads[chosen_thread], relevant_threads[chosen_thread + 1]))
    chosen_context_range = list(range(relevant_contexts[chosen_context], relevant_contexts[chosen_context + 1]))

    chosen_range = random.choices([chosen_set_range, chosen_thread_range, chosen_context_range],
                                  weights=[0.4, 0.3, 0.3])
    # return random.choice(chosen_range[0])
    chosen_range = random.choices(
        [[chosen_set_range[0]], chosen_context_range, chosen_thread_range[1:], [chosen_thread_range[0]]],
        weights=[0.05, 0.4, 0.4, 0.15])
    index = random.choice(chosen_range[0])
    return index
    # return random.choices([chosen_set_range[0], chosen_thread_range[0], chosen_context_range[0]], weights=[0.4, 0.3, 0.3])


def cxAnomalyDetection(ind1, ind2):
    # return gp.cxOnePoint(ind1, ind2)
    # List all available primitive types in each individual
    types1 = defaultdict(list)
    types2 = defaultdict(list)

    for idx, node in enumerate(ind1[1:], 1):
        types1[node.ret].append(idx)
    for idx, node in enumerate(ind2[1:], 1):
        types2[node.ret].append(idx)
    common_types = set(types1.keys()).intersection(set(types2.keys()))
    # common_types = []

    if len(common_types) > 0:
        func1 = toolbox.compile(expr=ind1)
        func_string1 = str(func1(0).root)
        func2 = toolbox.compile(expr=ind2)
        func_string2 = str(func2(0).root)
        try:
            index1_1 = get_index(ind1, func_string1, True)[0]
            index2_1 = get_index(ind2, func_string2, True)[0]
            type1_ = ind1[index1_1].ret
            type2_ = ind2[index2_1].ret

            if type1_ not in types2 or type2_ not in types1:
                raise BaseException

            slice1_1 = ind1.searchSubtree(index1_1)
            slice2_1 = ind2.searchSubtree(index2_1)

            index1_2 = random.choice(types1[type2_])
            index2_2 = random.choice(types2[type1_])
            slice1_2 = ind1.searchSubtree(index1_2)
            slice2_2 = ind2.searchSubtree(index2_2)

            ind2[slice2_1], ind1[slice1_1] = ind1[slice1_2], ind2[slice2_2]
        except:
            return ind1, ind2
    return ind1, ind2


def mutAnomalyDetection(individual, expr, pset):
    # return gp.mutUniform(individual=individual, expr=expr, pset=pset)
    func = toolbox.compile(expr=individual)
    func_string = str(func(0).root)
    try:
        anomalies = anomaly_map[func_string]
        list_indv = list(individual)

        set_indexes = [i for i, node in enumerate(list_indv) if node.name == "ctx_func"] + [len(list_indv)]
        thread_indexes = [i for i, node in enumerate(list_indv) if node.name.startswith("behavior_func")]
        context_indexes = [i for i, node in enumerate(list_indv) if node.name.startswith("single_input_func")]

        thread_scores = calculate_thread_scores([anomalies["win_o"], anomalies["win_v"], anomalies["block_o"], anomalies["block_v"], anomalies["requests"]], [-2, 2, -1, 1, -0.25])
        context_scores = calculate_context_scores([anomalies["win_o"], anomalies["win_v"], anomalies["block_o"], anomalies["block_v"], anomalies["requests"]], [-2, 2, -1, 1, -0.25])
        set_scores = calculate_set_scores(thread_scores)


        chosen_set = random.choices(range(10), weights=set_scores)[0]
        chosen_thread = random.choices(range(5), weights=thread_scores[chosen_set])[0]
        chosen_context = random.choices(range(10), weights=context_scores[chosen_set])[0]

        chosen_set_range = list(range(set_indexes[chosen_set], set_indexes[chosen_set + 1]))
        relevant_contexts = [x for x in context_indexes if x in chosen_set_range] + [set_indexes[chosen_set + 1]]
        relevant_threads = [x for x in thread_indexes if x in chosen_set_range] + [relevant_contexts[0]]
        chosen_thread_range = list(range(relevant_threads[chosen_thread], relevant_threads[chosen_thread + 1]))
        chosen_context_range = list(range(relevant_contexts[chosen_context], relevant_contexts[chosen_context + 1]))

        # chosen_range = random.choices([chosen_set_range, chosen_thread_range, chosen_context_range], weights=[0.4, 0.3, 0.3])

        chosen_range = random.choices([[chosen_set_range[0]], chosen_context_range, chosen_thread_range[1:], [chosen_thread_range[0]]], weights=[0.05, 0.4, 0.4, 0.15])
        index = random.choice(chosen_range[0])
        slice_ = individual.searchSubtree(index)
        type_ = individual[index].ret
        individual[slice_] = expr(pset=pset, type_=type_)
        return individual,
    except:
        return individual,


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


# Define Individual and Fitness
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax, pset=pset)

# Define Toolbox
toolbox = base.Toolbox()
toolbox.register("expr", generate_safe, pset=pset, min_=7, max_=14, terminal_types=terminal_types)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

# Plotting
# expr = toolbox.individual()
# nodes, edges, labels = gp.graph(expr)


# Define GP Operators
toolbox.register("evaluate", eval_generator)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", cxAnomalyDetection)
toolbox.register("expr_mut", generate_safe, min_=7, max_=14, terminal_types=terminal_types)
toolbox.register("mutate", mutAnomalyDetection, expr=toolbox.expr_mut, pset=pset)

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
                       'Fork_Violations': [],
                       'Code': []})


if __name__ == "__main__":
    run_experiment(0.0, 0.5, "NO_CX_V1")
    run_experiment(0.0, 0.5, "NO_CX_V2")
    run_experiment(0.0, 0.5, "NO_CX_V3")



