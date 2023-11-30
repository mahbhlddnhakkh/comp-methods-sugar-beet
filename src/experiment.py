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
    print_result_simple("Венгерский алгоритм (максимум)", measure_time(hungarian, m, True), m)
    print_result_simple("Венгерский алгоритм (минимум)", measure_time(hungarian, m, False), m)
    print_result_simple("Жадный алгоритм", measure_time(greedy, m), m)
    print_result_simple("Бережливый алгоритм", measure_time(lean, m), m)
    theta: int = int(input("Введите theta для бережливо-жадного и жадно-бережливого алгоритмов (от 1 до n): ") or math.floor(m.shape[0] / mu_div))
    print_result_simple("Бережливо-жадный алгоритм, theta = " + str(theta), measure_time(lean_greedy, m, theta), m)
    print_result_simple("Жадно-бережливый алгоритм, theta = " + str(theta), measure_time(greedy_lean, m, theta), m)

def advanced_experiment(m: np.ndarray, theta: int) -> tuple:
    '''
    Performs advanced experiment (or iteration from experiments series)
    return list in following format:
    [n, theta, hungarian_max_time, hungarian_max_s, hungarian_min_time, hungarian_min_s, ...] and so on
    The order will be the same as in simple_experiment
    The list size is 2+6*2
    '''

    def advanced_experiment_iteration(res: list, i: int, *args) -> None:
        '''
        I don't want to repeate this over and over
        '''
        tmp = measure_time(*args)
        res[i] = tmp[1]
        res[i+1] = tmp[0][1]
        # print_result_simple("", tmp, args[1])

    res: list = [None] * (2+6*2)
    n: int = m.shape[0]
    res[0] = n
    res[1] = theta
    i: int = 2

    advanced_experiment_iteration(res, i, hungarian, m, True)
    i+=2
    advanced_experiment_iteration(res, i, hungarian, m, False)
    i+=2
    advanced_experiment_iteration(res, i, greedy, m)
    i+=2
    advanced_experiment_iteration(res, i, lean, m)
    i+=2
    advanced_experiment_iteration(res, i, lean_greedy, m, theta)
    i+=2
    advanced_experiment_iteration(res, i, greedy_lean, m, theta)
    return tuple(res)
