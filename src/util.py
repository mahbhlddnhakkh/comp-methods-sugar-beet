from typing import Tuple, Dict, List
import numpy as np
from src.config import *
from matplotlib import pyplot as plt
import os

class exp_res_props:
    '''
    Represents props of advanced experiment
    '''
    n: int = 0
    theta: int = 0
    exp_count: int = 0
    # size = (n, algs_count) ; stores avarage S (for every experiment) for each algorightm on each phase
    phase_avarages: List[List[float]] = None
    # size = (exp_count, algs_count) ; stores S of each algorithm for each experiment
    exp_s_res: List[List[float]] = None

    def dump_to_file(self, file_path: str) -> None:
        '''
        Dumps properties to file
        '''
        with open(file_path, "w") as f:
            f.write(str(self.n) + ' ' + str(self.exp_count) + ' ' + str(self.theta) + '\n')
            for i in range(self.n):
                f.write(' '.join(list(map(str, self.phase_avarages[i]))) + '\n')
            for i in range(self.exp_count):
                f.write(' '.join(list(map(str, self.exp_s_res[i]))) + '\n')

    def get_from_file(self, file_path: str) -> None:
        '''
        Gets properties from file
        '''
        with open(file_path, "r") as f:
            line: list = f.readline().strip().split(' ')
            self.n = int(line[0])
            self.exp_count = int(line[1])
            self.theta = int(line[2])
            self.phase_avarages = [None] * self.n
            for i in range(self.n):
                line: list = f.readline().strip().split(' ')
                self.phase_avarages[i] = list(map(float, line))
            self.exp_s_res = [None] * self.exp_count
            for i in range(self.exp_count):
                line: list = f.readline().strip().split(' ')
                self.exp_s_res[i] = list(map(float, line))

    def display(self) -> None:
        '''
        Write some analytics and draws graph
        '''
        def display_iteration(self, label: str, i: int, x_arr, y_arr: np.array):
            plt.plot(x_arr, y_arr[:, i], label=label)

        avg_s: list = self.phase_avarages[-1]
        print("Средние S:")
        for i in range(algs_count):
            print(algs_names[i] + ':', avg_s[i])
        print()
        print("Усреднённая погрешность S:")
        avg_diff: list = self.get_avarage_error()
        for i in range(algs_count):
            print(algs_names[i] + ':', avg_diff[i])
        plt.title("Динамика S по различным планам переработки")
        plt.xlabel("phase")
        plt.ylabel("S")
        x_arr = range(self.n)
        y_arr = np.array(self.phase_avarages)
        for i in range(algs_count):
            display_iteration(self, algs_names[i], i, x_arr, y_arr)
        plt.legend()
        plt.show()
    
    def get_avarage_error(self) -> List[float]:
        '''
        Returns list of avarage errors
        '''
        avg_s: list = self.phase_avarages[-1]
        avg_diff: list = [None] * algs_count
        for i in range(algs_count):
            avg_diff[i] = (avg_s[0] - avg_s[i]) / avg_s[0]
        return avg_diff


def do_rand(shape: tuple, v_min, v_max) -> np.ndarray:
    '''
    Return random ndarray with values from v_min to v_max
    shape is a size tuple. E.g. shape=(2, 3) is matrix with sizes (2, 3)
    '''
    return (np.random.rand(*shape) * (v_max - v_min) + v_min)

def create_option(header: str, d: Tuple[Dict[str, object]]) -> object:
    '''
    Creates option to choose.
    First prints header and after that prints all d["text"]
    'd' must be {"text": "option_text", "value": <value or function>}
    return d[choice - 1]["value"]
    '''
    print(header)
    sz: int = len(d)
    if (sz <= 0):
        return
    for i in range(sz):
        print(i + 1, '.', sep='', end=' ')
        print(d[i]["text"])
    choice_str: str = input("Выбор: ")
    if (len(choice_str) == 0):
        print("Выбор по умолчанию 1")
    choice: int = int(choice_str or 1)
    if (choice >= 1 and choice <= sz):
        return d[choice - 1]["value"]
    else:
        raise Exception("choice must be between 1 and len(d)")

def print_result_simple(header: str, res: tuple, m: np.ndarray) -> None:
    '''
    Prints the result
    '''
    print(header, ": S = " + round_decimals_s % res[1], ", выбор этапов:", res[0] + 1)
    n = m.shape[0]
    for i in range(n):
        for j in range(n):
            if (res[0][i] == j):
                print("[", round_decimals_s % m[i][j], "]", sep='', end='\t')
            else:
                print(round_decimals_s % m[i][j], end='\t')
        print()

def print_result(header: str, res: tuple) -> None:
    '''
    Same as print_result_simple, but prints only S
    '''
    print(header, ": S = " + round_decimals_s % res[1])

def test_file_write(file_path: str) -> bool:
    '''
    Tests if able to write to file
    '''
    f = open(file_path, "a")
    res: bool = f.writable()
    f.close()
    return res

def test_read_file(file_path: str) -> bool:
    '''
    Tests if able to read file
    '''
    return os.access(file_path, os.R_OK)


def pretty_2d_table(arr: List[List[str]]) -> str:
    '''
    https://stackoverflow.com/a/13214945
    Returns string table formatted nicely
    '''
    s = [[str(e) for e in row] for row in arr]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    return '\n'.join(table)
