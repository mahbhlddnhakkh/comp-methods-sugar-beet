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
        }
    ))()

if __name__ == "__main__":
    main()
