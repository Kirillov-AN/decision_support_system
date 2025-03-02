import numpy as np
from pulp import LpMaximize, LpProblem, LpVariable, lpSum

# Ограничения
MAX_BUDGET_INDEX = 2.0            # Ограничение по финансовому индексу
MIN_SOCIAL_RATING_INDEX = 0.1     # Минимальный социальный рейтинг
MIN_DELIVERY_INDEX = 0.5          # Минимальный индекс доставки

# ПРИНИМАЕТ НА ВХОД CUPS_DATA И WEIGHT
# НА ВЫХОДЕ ДАЕТ ТАБЛИЦУ : Столб 1 РЕЙТИНГ, дальше - СТРОКА ПОСТАВЩИКА

cups_data = [
    ['Supplier A1', 5, 1000, True, 90, 5000, 85, 7],
    ['Supplier B1', 6, 1500, False, 85, 4500, 80, 8],
    ['Supplier C1', 7, 2000, True, 95, 4000, 90, 5],
    ['Supplier D1', 8, 1200, False, 88, 4700, 82, 6],
    ['Supplier E1', 7, 180, True, 230, 95, 4, 9]
]

weight_factors = [5, 5, 2, 2, 5, 2, 1]  # Обновленные веса

# Функция для преобразования данных
def transform_data(input_data):
    transformed = []
    for row in input_data:
        transformed_row = [
            row[1],  # Цена за один стаканчик
            row[2],  # Размер партии стаканчиков
            1 if row[3] else 0,  # Наличие логотипа бренда (True/False -> 1/0)
            row[4],  # Удобство пользования
            row[5],  # Затраты на логистику
            row[6],  # Репутация поставщика
            row[7]   # Срок доставки
        ]
        transformed.append(transformed_row)
    return transformed

# Функция для нормализации индексов на этапе их расчёта
def calculate_indices(processed_data, weights):
    temp_indices = []
    processed_data = [row for row in processed_data if isinstance(row[0], (int, float))]
    batch_sizes = np.array([row[1] for row in processed_data], dtype=np.float64)
    average_batch_size = np.average(batch_sizes)*weights[1]

    financial_indices = []

    for row in processed_data:

        price_per_cup = row[0]
        batch_size = row[1]
        logo = row[2]*weights[2]
        usability = row[3]*weights[3]
        logistics_cost = row[4]
        reputation = row[5]*weights[5]
        delivery_time = row[6]*weights[6]

        # Расчет стоимости покупки и доставки
        price_cost = price_per_cup * average_batch_size
        logistics_cost_normalized = (logistics_cost * average_batch_size) / batch_size

        # Финансовый индекс как сумма стоимости покупки и доставки
        financial_index = (price_cost*weights[0] + logistics_cost_normalized*weights[4])/(weights[0]+weights[4])
        print(price_per_cup, average_batch_size, logistics_cost, financial_index)
        financial_indices.append(financial_index)

        social_rating = reputation * usability + logo
        delivery_index = round(delivery_time / max([r[6] for r in processed_data]), 2)

        temp_indices.append([
            financial_index,             # Финансовый индекс без нормализации
            round(social_rating, 2),     # Социальный рейтинг
            delivery_index               # Индекс доставки
        ])

    # Нормализация финансового индекса на минимальное значение
    min_financial_index = min(financial_indices)
    for idx in temp_indices:
        idx[0] = round(idx[0] / min_financial_index, 6) * -1  # Нормализуем и делаем отрицательным

    indices_array = np.array(temp_indices)
    max_values = np.max(indices_array, axis=0)
    normalized_indices = np.round(indices_array / max_values, 2)

    return normalized_indices.tolist(), indices_array

# Функция для расчёта рейтинга
def calculate_ratings(index_matrix):
    ratings = []
    for indices in index_matrix:
        rating = round(indices[1] + indices[2] - indices[0], 6)
        ratings.append(rating)
    return ratings

# Функция для получения идеальной комбинации
def get_best_combination(input_data):
    best_price = min(row[1] for row in input_data)
    best_batch_size = max(row[2] for row in input_data)
    best_logo = max(1 if row[3] else 0 for row in input_data)
    best_usability = max(row[4] for row in input_data)
    best_logistics_cost = min(row[5] for row in input_data)
    best_reputation = max(row[6] for row in input_data)
    best_delivery_time = min(row[7] for row in input_data)

    best_combination = [
        best_price,
        best_batch_size,
        best_logo,
        best_usability,
        best_logistics_cost,
        best_reputation,
        best_delivery_time
    ]
    return best_combination

# MILP оптимизация
def milp_optimization(indices, ratings):
    problem = LpProblem("Optimize_Cup_Rating", LpMaximize)

    y = [LpVariable(f"y_{i}", cat="Binary") for i in range(len(indices))]

    problem += lpSum(y[i] * ratings[i] for i in range(len(indices))), "Maximize_Rating"

    problem += lpSum(y) == 1, "Only_One_Alternative"
    problem += lpSum(y[i] * indices[i][0] for i in range(len(indices))) <= MAX_BUDGET_INDEX, "Budget_Index_Constraint"
    problem += lpSum(y[i] * indices[i][1] for i in range(len(indices))) >= MIN_SOCIAL_RATING_INDEX, "Social_Rating_Constraint"
    problem += lpSum(y[i] * indices[i][2] for i in range(len(indices))) >= MIN_DELIVERY_INDEX, "Delivery_Index_Constraint"

    problem.solve()

    selected_index = next((i for i, var in enumerate(y) if var.value() == 1), None)

    return selected_index, ratings[selected_index] if selected_index is not None else None

# Main
processed_data = transform_data(cups_data)
normalized_indices, raw_indices = calculate_indices(processed_data, weight_factors)
indices_array = np.array(normalized_indices)
rank = np.linalg.matrix_rank(indices_array)

if rank / len(indices_array) <= 0.3:
    print("Применяется MILP оптимизация")
    ratings_list = calculate_ratings(normalized_indices)
    selected_index, optimal_rating = milp_optimization(normalized_indices, ratings_list)

    if selected_index is not None:
        print(f"Выбрана альтернатива: {cups_data[selected_index]}")
        print(f"Оптимальный рейтинг: {optimal_rating}")
    else:
        print("Оптимальное решение не найдено")
else:
    print("Применяется TOPSIS методика анализа")

    ratings_list = calculate_ratings(normalized_indices)
    ideal_combination = get_best_combination(cups_data)
    ideal_indices, _ = calculate_indices([ideal_combination], weight_factors)
    ideal_indices = ideal_indices[0]
    ideal_rating = calculate_ratings([ideal_indices])[0]

    sorted_results = sorted(zip(ratings_list, cups_data), key=lambda pair: abs(pair[0] - ideal_rating))

    print("Матрица индексов:")
    for idx in normalized_indices:
        print(idx)

    print("\nИдеальный вариант (по индексам):")
    print(ideal_indices)
    print(f"Рейтинг идеального варианта: {ideal_rating}")

# НЕОБХОДИМЫЙ ВЫВОД
    print("\nИсходные данные, отсортированные по разнице с идеальным рейтингом:")
    for rating, entry in sorted_results:
        print(f"Рейтинг: {rating}, Данные: {entry}")