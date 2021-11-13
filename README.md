# BPCodeGenerator
Generates BP Code using Genetic Programming

To run TicTacToe example, first run BPServerProto.java, and then run TicTacToe.py
The running of game and recording of stats is performed in RunnerEvaluatorOrg.java.

In TicTacToe.py, call on run_experiment(crossover_rate, mutation_rate, expirement_name) with proper arguments to run an experiment.

To change number of generations or population size change the parameters 'NUMBER_OF_GENERATIONS' and 'POPULATION_SIZE' accordingly.

To change fitness function and its weights, look at results_to_fitness() method.

The crossover and mutation is performed in cxAnomalyDetection() and mutAnomalyDetection accordingly. To use the regular operators (not smart) simply uncomment the first
line in each operator (starts with "return...").

TicTacToe.py produces a csv file only when the experiment finishes or an error occurs, you can simply shut down the server to force an exception and a csv file to be created mid-run.

To run in cluster:
All proper python libraries must be installed, additionally a jar file with dependencies must be compiled, and resources folder added seperatly with the jar file.
-run serverscript
-wait for a few seconds, and check serverscript output to get the server's ip
-enter the ip into ProtoClient.py
-run clientscript
