from pulp import LpMaximize, LpProblem, LpVariable, lpSum
import math

def optimal_alternative(vectors, max_budget, min_reputation, min_rent_time, weights):
    # Нормализация альтернатив
    def normalize_alternatives(vectors):
        transposed = list(zip(*vectors))
        normalized = []
        for crit_values in transposed:
            sum_of_squares = sum(v ** 2 for v in crit_values)
            sqrt_sum = math.sqrt(sum_of_squares)
            normalized.append([v / sqrt_sum for v in crit_values])
        return list(zip(*normalized))

    normalized_alternatives = normalize_alternatives(vectors)

    # Создаём MILP задачу
    problem = LpProblem("Optimal_Alternative", LpMaximize)

    # Бинарные переменные
    y = [LpVariable(f"y_{i}", cat="Binary") for i in range(len(vectors))]

    # Целевая функция
    objective = lpSum(
        y[i] * lpSum(normalized_alternatives[i][j] * weights[j] for j in range(len(weights)))
        for i in range(len(vectors))
    )
    problem += objective

    # Ограничения
    problem += lpSum(y) == 1, "Only_One_Alternative"

    for i, alt in enumerate(vectors):
        budget_constraint = alt[4] + alt[5] + alt[6]
        if alt[2] < min_reputation or budget_constraint > max_budget or alt[7] < min_rent_time:
            problem += y[i] == 0, f"Exclude_Alternative_{i}"

    # Решаем задачу
    problem.solve()

    # Возвращаем результат
    if problem.status == 1:  # 1 = Optimal
        for i, var in enumerate(y):
            if var.value() == 1:
                return i, vectors[i], problem.objective.value()
    return None, None, None
