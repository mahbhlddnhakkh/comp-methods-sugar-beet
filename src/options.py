from src.util import *
from src.experiment import *
from src.algorithms import convert_to_p_matrix
import numpy as np
from typing import List
from src.config import *
import sys

def option_manual() -> None:
    '''
    Option when:
        "Выберите:"
    Selected:
        "Вручную ввести матрицу"
    '''
    print("Введите путь к файлу с матрицей формата:")
    print("1-ая строка число n,")
    print("От 2-ой строки до n+1 строки: матрица размером n на n. Формат матрицы: столбцы разделять пробелом, строки - \\n (т.е. новой строкой)")
    filename: str = (input("Введите путь к файлу: ") or "input.txt")
    matrix: np.ndarray = None
    lines: List[str] = None
    with open(filename, "r") as f:
        lines = [e.strip() for e in f.readlines()]
    n: int = int(lines[0])
    if (n <= 0):
        raise Exception("n <= 0")
    lines.pop(0)
    matrix = np.fromstring(string=' '.join(lines), dtype=float, count=n*n, sep=' ').reshape(n, n)
    is_p: bool = create_option("Какая это матрица?", (
        {
            "text": "Это матрица P (преобразований делать не нужно)",
            "value": True
        },
        {
            "text": "Это вектор 'a' и матрица B размером n на (n-1) (нужно преобразовать в P)",
            "value": False
        }
    ))
    if (not is_p):
        convert_to_p_matrix(matrix)
    simple_experiment(matrix)

def option_experiment() -> None:
    '''
    Option when:
        "Выберите:"
    Selected:
        "Эксперименты"
    '''
    create_option("Использовать дозаривание для первых [n/%d] этапов?" % mu_div, (
        {
            "text": "Да, использовать",
            "value": option_experiment_ripening
        },
        {
            "text": "Нет, не использовать",
            "value": option_experiment_no_ripening
        }
    ))()

def option_experiment_ripening() -> None:
    '''
    Option when:
        "Использовать дозаривание для первых [n/%d] этапов?" % mu_div
    Selected:
        "Да, использовать"
    '''
    n: int = int(input("Введите n (n >= 2): "))
    if (n < 2):
        raise Exception("n < 2")
    exp_count: int = int(input("Введите количество экспериментов: "))
    if (exp_count <= 0):
        raise Exception("exp_count <= 0")
    a_i_min: float = float(input("Введите минимальный a_i > 0 (границы можно включить*): "))
    a_i_max: float = float(input("Введите максимальный a_i > 0 (границы можно включить*): "))
    if (a_i_min == 0.0):
        a_i_min = sys.float_info.epsilon
    if (a_i_max == 0.0):
        a_i_max = sys.float_info.epsilon
    if (a_i_min <= 0.0 or a_i_max <= 0.0):
        raise Exception("a_i must be greater than 0")
    if (a_i_min > a_i_max):
        raise Exception("a_i_min > a_i_max")
    b_i_j_min_1: float = float(input("Введите минимальный b_i_j > 1 во время дозаривания (границы можно включить*): "))
    b_i_j_max_1: float = float(input("Введите максимальный b_i_j > 1 во время дозаривания (границы можно включить*): "))
    if (b_i_j_min_1 == 1.0):
        b_i_j_min_1 += sys.float_info.epsilon
    if (b_i_j_max_1 == 1.0):
        b_i_j_max_1 += sys.float_info.epsilon
    if (b_i_j_min_1 <= 1.0 or b_i_j_max_1 <= 1.0):
        raise Exception("b_i_j while ripening must be greater than 1")
    if (b_i_j_min_1 > b_i_j_max_1):
        raise Exception("b_i_j_min_1 > b_i_j_max_1")
    b_i_j_min_2: float = float(input("Введите минимальный 0 < b_i_j < 1 после дозаривания (границы можно включить*): "))
    b_i_j_max_2: float = float(input("Введите максимальный 0 < b_i_j < 1 после дозаривания (границы можно включить*): "))
    if (b_i_j_max_2 == 1.0):
        b_i_j_max_2 -= sys.float_info.epsilon
    if (b_i_j_min_2 == 1.0):
        b_i_j_min_2 -= sys.float_info.epsilon
    if (b_i_j_min_2 == 0.0):
        b_i_j_min_2 = sys.float_info.epsilon
    if (b_i_j_max_2 == 0.0):
        b_i_j_max_2 = sys.float_info.epsilon
    if (b_i_j_min_2 >= 1.0 or b_i_j_min_2 <= 0.0 or b_i_j_max_2 >= 1.0 or b_i_j_max_2 <= 0.0):
        raise Exception("b_i_j after ripening must be between 0 and 1")
    if (b_i_j_min_2 > b_i_j_max_2):
        raise Exception("b_i_j_min_2 > b_i_j_max_2")
    theta: int = int(input("Введите theta для бережливо-жадного и жадно-бережливого алгоритмов (от 1 до n) (по умолчанию [n/%d]): " % mu_div) or math.floor(n / mu_div))
    if (theta < 1 or theta > n):
        raise Exception("theta must be between 1 and n")
    output_path: str = str(input("Введите путь к файлу, куда будет записан результат экспериментов (формат txt, если файл существует, его содержимое будет стёрто) (по умолчанию output.txt): ") or "output.txt")
    if (not test_file_write(output_path)):
        raise Exception("Cannot write to file " + output_path)
    exp_res: exp_res_props = exp_res_props()
    exp_res.n = n
    exp_res.theta = theta
    exp_res.exp_count = exp_count
    exp_res.exp_s_res = [[None] * algs_count for i in range(exp_count)]
    exp_res.phase_avarages = [[0.0] * algs_count for i in range(n)]
    for i in range(exp_count):
        m: np.ndarray = generate_matrix_main_ripening(n, (a_i_min, a_i_max), (b_i_j_min_1, b_i_j_max_1), (b_i_j_min_2, b_i_j_max_2))
        convert_to_p_matrix(m)
        advanced_experiment(m, exp_res, i)
    exp_res.dump_to_file(output_path)
    exp_res.display()

def option_experiment_no_ripening() -> None:
    '''
    Option when:
        "Использовать дозаривание для первых [n/%d] этапов?" % mu_div
    Selected:
        "Нет, не использовать"
    '''
    n: int = int(input("Введите n (n >= 2): "))
    if (n < 2):
        raise Exception("n < 2")
    exp_count: int = int(input("Введите количество экспериментов: "))
    if (exp_count <= 0):
        raise Exception("exp_count <= 0")
    a_i_min: float = float(input("Введите минимальный a_i > 0 (границы можно включить*): "))
    a_i_max: float = float(input("Введите максимальный a_i > 0 (границы можно включить*): "))
    if (a_i_min == 0.0):
        a_i_min = sys.float_info.epsilon
    if (a_i_max == 0.0):
        a_i_max = sys.float_info.epsilon
    if (a_i_min <= 0.0 or a_i_max <= 0.0):
        raise Exception("a_i must be greater than 0")
    if (a_i_min > a_i_max):
        raise Exception("a_i_min > a_i_max")
    b_i_j_min: float = float(input("Введите минимальный 0 < b_i_j < 1 (границы можно включить*): "))
    b_i_j_max: float = float(input("Введите максимальный 0 < b_i_j < 1 (границы можно включить*): "))
    if (b_i_j_max == 1.0):
        b_i_j_max -= sys.float_info.epsilon
    if (b_i_j_min == 1.0):
        b_i_j_min -= sys.float_info.epsilon
    if (b_i_j_min == 0.0):
        b_i_j_min = sys.float_info.epsilon
    if (b_i_j_max == 0.0):
        b_i_j_max = sys.float_info.epsilon
    if (b_i_j_min >= 1.0 or b_i_j_min <= 0.0 or b_i_j_max >= 1.0 or b_i_j_max <= 0.0):
        raise Exception("b_i_j must be between 0 and 1")
    if (b_i_j_min > b_i_j_max):
        raise Exception("b_i_j_min > b_i_j_max")
    theta: int = int(input("Введите theta для бережливо-жадного и жадно-бережливого алгоритмов (от 1 до n) (по умолчанию [n/%d]): " % mu_div) or math.floor(n / mu_div))
    if (theta < 1 or theta > n):
        raise Exception("theta must be between 1 and n")
    output_path: str = str(input("Введите путь к файлу, куда будет записан результат экспериментов (формат txt, если файл существует, его содержимое будет стёрто) (по умолчанию output.txt): ") or "output.txt")
    if (not test_file_write(output_path)):
        raise Exception("Cannot write to file " + output_path)
    exp_res: exp_res_props = exp_res_props()
    exp_res.n = n
    exp_res.theta = theta
    exp_res.exp_count = exp_count
    exp_res.exp_s_res = [[None] * algs_count for i in range(exp_count)]
    exp_res.phase_avarages = [[0.0] * algs_count for i in range(n)]
    for i in range(exp_count):
        m: np.ndarray = generate_matrix_main(n, (a_i_min, a_i_max), (b_i_j_min, b_i_j_max))
        convert_to_p_matrix(m)
        advanced_experiment(m, exp_res, i)
    exp_res.dump_to_file(output_path)
    exp_res.display()

def option_show_graph() -> None:
    '''
    Option when:
        "Выберите:"
    Selected:
        "Проанализировать эксперименты из файла"
    '''
    file_path: str = str(input("Введите путь к файлу с экспериментами (по умолчанию output.txt): ") or "output.txt")
    exp_res: exp_res_props = exp_res_props()
    exp_res.get_from_file(file_path)
    exp_res.display()

def option_analyze_average_errors() -> None:
    '''
    Option when:
        "Выберите:"
    Selected:
        "Проанализировать относительную погрешность из файлов экспериментов"
    '''
    files_count: int = int(input("Введите количество файлов с экспериментами (по умолчанию 1): ") or 1)
    result: List[List[str]] = [None] * (files_count + 1)
    result[0] = algs_names
    if (files_count < 1):
        raise Exception("files_count < 1")
    files: List[str] = [None] * files_count
    for i in range(files_count):
        files[i] = str(input("Введите файл с экспериментом " + str(i+1) + " (по умолчанию output" + str(i+1) + ".txt): ") or "output" + str(i+1) + ".txt")
        exp_res: exp_res_props = exp_res_props()
        exp_res.get_from_file(files[i])
        result[i+1] = list(map(str, exp_res.get_avarage_error()))
    output_path: str = str(input("Введите путь к файлу, куда будет записан результат анализа (формат txt, если файл существует, его содержимое будет стёрто) (по умолчанию output.txt): ") or "output.txt")
    if (not test_file_write(output_path)):
        raise Exception("Cannot write to file " + output_path)
    result_str = pretty_2d_table(result)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result_str)
    print(result_str)
