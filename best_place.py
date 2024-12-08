from scipy.optimize import linprog
import numpy as np

# Параметры задачи
flow = np.array([95, 65, 20, 85, 40, 50, 100, 60, 10, 75, 55, 30])
conversion = np.array([0.80, 0.50, 0.15, 0.30, 0.70, 0.40, 0.95, 0.60, 0.05, 0.65, 0.85, 0.50])
reputation = np.array([5, 4, 1, 3, 2, 3, 5, 4, 1, 3, 4, 2])
size = np.array([35, 25, 10, 30, 15, 20, 40, 20, 8, 28, 12, 10])
rent = np.array([180, 120, 40, 160, 80, 100, 200, 110, 30, 140, 90, 50])
infra_costs = np.array([90, 60, 20, 50, 30, 45, 100, 50, 10, 70, 55, 25])
deposit = np.array([180, 240, 40, 160, 160, 200, 200, 55, 30, 70, 90, 50])
time_rent = np.array([12, 6, 1, 10, 3, 5, 12, 6, 2, 8, 4, 3])

# Создание целевой функции (коэффициенты)
c = -flow - conversion * 100 - reputation - size + rent + infra_costs + deposit
print("Коэффициенты целевой функции:", c)

# Ограничения
max_budget = 300  # Общий бюджет на аренду, инфраструктуру и залог (в тысячах руб)
min_reputation = 3  # Минимальная допустимая репутация
min_rent_time = 6  # Минимальный срок аренды (в месяцах)

# Ограничения бюджета, репутации и времени аренды
budget_constraint = rent + infra_costs + deposit
A_ub = np.vstack([
    budget_constraint,  # Ограничение бюджета
    -reputation,        # Ограничение на минимальную репутацию
    -time_rent          # Ограничение на минимальное время аренды
])

# Исправленный b_ub
b_ub = [
    max_budget,         # Ограничение по бюджету
    -min_reputation,    # Ограничение по минимальной репутации (инверсия для <=)
    -min_rent_time      # Ограничение по минимальному сроку аренды (инверсия для <=)
]

x_bounds = [(0, 1) for _ in range(len(flow))]

# Запуск линейного программирования
result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=x_bounds, method="highs")

# Результаты
if result.success:
    best_place_index = np.argmax(result.x)
    best_rating = -result.fun  # Умножаем на -1, чтобы получить максимальный рейтинг
    print(f"Лучшее место с индексом {best_place_index} имеет рейтинг {best_rating}")
    print(f"Характеристики: Поток прохожих: {flow[best_place_index]}, Конверсия: {conversion[best_place_index]}, ... и т.д.")
else:
    print("Не удалось найти решение, удовлетворяющее всем ограничениям.")