from src.util import *
from src.algorithms import *
from src.config import *
import math
import numpy as np

def simple_experiment(m: np.ndarray) -> None:
    '''
    Performs really simple experiment
    Should use with small matrices and manually (like from file)
    '''
    print_result_simple(algs_names[0], hungarian(m, True), m)
    print_result_simple(algs_names[1], hungarian(m, False), m)
    print_result_simple(algs_names[2], greedy(m), m)
    print_result_simple(algs_names[3], lean(m), m)
    theta: int = int(input("Введите theta для бережливо-жадного и жадно-бережливого алгоритмов (от 1 до n): ") or math.floor(m.shape[0] / mu_div))
    print_result_simple(algs_names[4] + ", theta = " + str(theta), lean_greedy(m, theta), m)
    print_result_simple(algs_names[5] + ", theta = " + str(theta), greedy_lean(m, theta), m)

def advanced_experiment(m: np.ndarray, exp_res: exp_res_props, exp_i: int) -> None:
    '''
    Performs advanced experiment (or iteration from experiments series)
    writes result to exp_res on experiment number exp_i
    exp_res should has all it's lits initilized with zeros
    '''

    def advanced_experiment_iteration(exp_res: exp_res_props, exp_i: int, i: int, func, m: np.ndarray, *args) -> None:
        '''
        I don't want to repeate this over and over
        '''
        n: int = m.shape[0]
        tmp: tuple = func(m, *args)
        exp_res.exp_s_res[exp_i][i] = tmp[1]
        phases: list = [None] * n
        phases[0] = m[0][tmp[0][0]] / exp_res.exp_count
        exp_res.phase_avarages[0][i] += phases[0]
        for k in range(1, n):
           phases[k] = phases[k-1] + m[k][tmp[0][k]] / exp_res.exp_count
           exp_res.phase_avarages[k][i] += phases[k]
        # print_result_simple(str(i), tmp, m)

    i: int = 0

    advanced_experiment_iteration(exp_res, exp_i, i, hungarian, m, True)
    i+=1
    advanced_experiment_iteration(exp_res, exp_i, i, hungarian, m, False)
    i+=1
    advanced_experiment_iteration(exp_res, exp_i, i, greedy, m)
    i+=1
    advanced_experiment_iteration(exp_res, exp_i, i, lean, m)
    i+=1
    advanced_experiment_iteration(exp_res, exp_i, i, lean_greedy, m, exp_res.theta)
    i+=1
    advanced_experiment_iteration(exp_res, exp_i, i, greedy_lean, m, exp_res.theta)
