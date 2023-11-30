from typing import Tuple, Dict, List
from timeit import default_timer as timer
from datetime import timedelta
import numpy as np
from src.config import *

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

def measure_time(func, *args, **kwargs) -> tuple:
    '''
    measures time
    do func(*args, **kwargs)
    return tuple(res, time_passed)
    '''
    start = timer()
    res = func(*args, **kwargs)
    end = timer()
    return (res, end - start)

def print_result_simple(header: str, res: tuple, m: np.ndarray) -> None:
    '''
    Prints the result graphically
    '''
    print(header, "за", "%.3f" % res[1], "секунд", ": S = " + round_decimals_s % res[0][1], ", выбор этапов:", res[0][0] + 1)
    n = m.shape[0]
    for i in range(n):
        for j in range(n):
            if (res[0][0][i] == j):
                print("[", round_decimals_s % m[i][j], "]", sep='', end='\t')
            else:
                print(round_decimals_s % m[i][j], end='\t')
        print()

def print_result(header: str, res) -> None:
    '''
    Same as print_result_simple, but prints only time measure and S
    '''
    print(header, "за", "%.3f" % res[1], "секунд", ": S = " + round_decimals_s % res[0][1])

def test_file_write(file_path: str) -> bool:
    '''
    Tests if able to write to file
    '''
    f = open(file_path, "a")
    res: bool = f.writable()
    f.close()
    return res

def write_exp_results_to_file(file_path: str, res: List[tuple]) -> None:
    '''
    Writes experiments results to file file_path
    res is a list of experiments results
    '''
    with open(file_path, "w") as f:
        for exp in res:
            f.write(str(exp[0]))
            f.write(' ' + str(exp[1]))
            for i in range(2, len(exp)):
                format_str = "%.3f" if i % 2 == 0 else round_decimals_s
                f.write(' ' + format_str % exp[i])
            f.write('\n')
