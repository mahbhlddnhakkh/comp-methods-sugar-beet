# mu = [n / mu_div] = [n / 3]
mu_div: int = 3
# Show only first X decimals for the results
round_decimals_s_int: int = 7
# same as round_decimals_s_int but for the strings
round_decimals_s: str = "%." + str(round_decimals_s_int) + "f"
# Algorithms count instead of using 'magical number'
algs_count = 6
# Algorithms names so I don't have to type them again and again
algs_names = ("Венгерский алгоритм (максимум)", "Венгерский алгоритм (минимум)", "Жадный алгоритм", "Бережливый алгоритм", "Бережливо-жадный алгоритм", "Жадно-бережливый алгоритм")
