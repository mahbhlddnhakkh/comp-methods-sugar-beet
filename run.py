from src.util import *
from src.options import *

def main() -> None:
    create_option("Выберите:", (
        {
            "text": "Вручную ввести матрицу",
            "value": option_manual
        },
        {
            "text": "Эксперименты",
            "value": option_experiment
        },
        {
            "text": "Проанализировать эксперименты из файла",
            "value": option_show_graph
        },
        {
            "text": "Проанализировать относительную погрешность из файлов экспериментов",
            "value": option_analyze_average_errors
        }
    ))()

if __name__ == "__main__":
    main()
