import numpy as np

# Параметры задачи
flow = np.array([95, 65, 20, 85, 40, 50, 100, 60, 10, 75, 55, 30])  # Поток прохожих
conversion = np.array([0.80, 0.50, 0.15, 0.30, 0.70, 0.40, 0.95, 0.60, 0.05, 0.65, 0.85, 0.50])  # Конверсия
retention = np.array([90, 60, 30, 70, 50, 55, 110, 65, 20, 75, 60, 45])  # Время удержания
reputation = np.array([5, 4, 1, 3, 2, 3, 5, 4, 1, 3, 4, 2])  # Репутация
size = np.array([35, 25, 10, 30, 15, 20, 40, 20, 8, 28, 12, 10])  # Площадь
rent = np.array([180, 120, 40, 160, 80, 100, 200, 110, 30, 140, 90, 50])  # Арендная плата
infra_costs = np.array([90, 60, 20, 50, 30, 45, 100, 50, 10, 70, 55, 25])  # Затраты на инфраструктуру
deposit = np.array([180, 240, 40, 160, 160, 200, 200, 55, 30, 70, 90, 50])  # Залог

# Весовые коэффициенты для каждого параметра
weights = {
    "flow": 0.3,
    "conversion": 0.2,
    "retention": 0.1,
    "reputation": 0.1,
    "size": 0.1,
    "rent": -0.1,
    "infra_costs": -0.05,
    "deposit": -0.05
}

# Рейтинговая функция для каждого места
rating = (
    weights["flow"] * flow +
    weights["conversion"] * conversion * 100 +  # Масштабируем конверсию
    weights["retention"] * retention +
    weights["reputation"] * reputation +
    weights["size"] * size +
    weights["rent"] * rent +
    weights["infra_costs"] * infra_costs +
    weights["deposit"] * deposit
)

# Ограничения
max_budget = 300  # Общий бюджет на аренду, инфраструктуру и залог (в тысячах руб)
min_reputation = 3  # Минимальная допустимая репутация
min_rent_time = 6  # Минимальный срок аренды (в месяцах)

# Создаем массивы ограничений
budget_constraint = rent + infra_costs + deposit  # Общие затраты
reputation_constraint = reputation  # Репутация
rent_time_constraint = np.array([12, 6, 1, 10, 3, 5, 12, 6, 2, 8, 4, 3])  # Срок аренды

# Проверка на выполнение всех ограничений
feasible_indices = np.where(
    (budget_constraint <= max_budget) &
    (reputation_constraint >= min_reputation) &
    (rent_time_constraint >= min_rent_time)
)[0]

# Выбор максимального рейтинга среди допустимых мест
if len(feasible_indices) > 0:
    best_place_index = feasible_indices[np.argmax(rating[feasible_indices])]
    best_rating = rating[best_place_index]
    best_place_info = {
        "Поток прохожих": flow[best_place_index],
        "Конверсия": conversion[best_place_index],
        "Время удержания": retention[best_place_index],
        "Репутация": reputation[best_place_index],
        "Площадь": size[best_place_index],
        "Арендная плата": rent[best_place_index],
        "Затраты на инфраструктуру": infra_costs[best_place_index],
        "Залог": deposit[best_place_index],
        "Рейтинг": best_rating
    }
else:
    best_place_info = "Нет доступных мест, которые удовлетворяют всем ограничениям."

print(best_place_info)
