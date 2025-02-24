import numpy as np
from pulp import LpMaximize, LpProblem, LpVariable, lpSum

# Домены (топсис, милп)
# Прикладной слой (юзкейсы)
# Адаптеры (интерфейсы)

# Ограничения
MAX_BUDGET_INDEX = 1.0            # Ограничение по финансовому индексу
MIN_SOCIAL_RATING_INDEX = 0.5     # Минимальный социальный рейтинг
MIN_QUALITY_INDEX = 0.5           # Минимальный индекс качества

# ПРИНИМАЕТ НА ВХОД COFFEE_DATA И WEIGHT
# НА ВЫХОДЕ ДАЕТ ТАБЛИЦУ : Столб 1 РЕЙТИНГ, дальше - СТРОКА ПОСТАВЩИКА

# def getdata
coffee_data = [
    ['Roaster F', 530, 950, 'High', 87, 4, 290, 'Premium', 5],
    ['Roaster G', 460, 1100, 'Medium', 75, 3, 310, 'Basic', 7],
    ['Roaster H', 500, 1050, 'High', 90, 6, 270, 'Premium', 12],
    ['Roaster I', 470, 1150, 'Low', 65, 2, 240, 'Standard', 7],
    ['Roaster J', 490, 980, 'Medium', 80, 5, 260, 'Standard', 8]
]

weight_factors = [3, 2, 3, 2, 1, 2, 3, 2]

# Функция для преобразования данных
def transform_data(input_data):
    known_map = {'High': 3, 'Medium': 2, 'Low': 1, None: 0}
    service_level_map = {'Premium': 3, 'Standard': 2, 'Basic': 1, None: 0}

    transformed = []
    for index, row in enumerate(input_data):
        transformed_row = [
            index + 1,
            row[1],
            row[2],
            known_map.get(row[3], 0),
            row[4],
            row[5],
            row[6],
            service_level_map.get(row[7], 0),
            row[8]
        ]
        transformed.append(transformed_row)

    return transformed

# Функция для нормализации индексов на этапе их расчёта
def calculate_indices(processed_data, weights):
    temp_indices = []
    for row in processed_data:
        weighted_row = [val * w for val, w in zip(row[1:], weights)]

        price_per_kg = weighted_row[0]
        batch_size = weighted_row[1]
        fame = weighted_row[2]
        reputation = weighted_row[3]
        warranty_years = weighted_row[4]
        logistics_cost = weighted_row[5]
        service_level = weighted_row[6]
        shelf_life = weighted_row[7]

        financial_index = (price_per_kg * batch_size) + logistics_cost
        social_rating = reputation * fame
        quality_index = service_level + warranty_years + shelf_life

        temp_indices.append([
            round(-financial_index, 2),
            round(social_rating, 2),
            round(quality_index, 2)
        ])

    indices_array = np.array(temp_indices)
    max_values = np.max(indices_array, axis=0)
    normalized_indices = np.round(indices_array / max_values, 2)

    return normalized_indices.tolist(), indices_array

# Функция для расчёта рейтинга
def calculate_ratings(index_matrix):
    ratings = []
    for indices in index_matrix:
        rating = round(indices[1] + indices[2] - indices[0], 2)
        ratings.append(rating)
    return ratings

# Функция для получения идеальной комбинации
def get_best_combination(input_data):
    processed_data = transform_data(input_data)

    best_price = min(row[1] for row in processed_data)
    best_batch_size = max(row[2] for row in processed_data)
    best_known = max(row[3] for row in processed_data)
    best_reputation = max(row[4] for row in processed_data)
    best_warranty = max(row[5] for row in processed_data)
    best_logistics_cost = min(row[6] for row in processed_data)
    best_service_level = max(row[7] for row in processed_data)
    best_shelf_life = max(row[8] for row in processed_data)

    best_combination = [
        'Best Combination',
        best_price,
        best_batch_size,
        best_known,
        best_reputation,
        best_warranty,
        best_logistics_cost,
        best_service_level,
        best_shelf_life
    ]
    return best_combination

# MILP оптимизация

def milp_optimization(indices, ratings):
    problem = LpProblem("Optimize_Rating", LpMaximize)

    # Бинарные переменные для выбора альтернатив
    y = [LpVariable(f"y_{i}", cat="Binary") for i in range(len(indices))]

    # Целевая функция - максимизация рейтинга
    problem += lpSum(y[i] * ratings[i] for i in range(len(indices))), "Maximize_Rating"

    # Ограничение на выбор только одной альтернативы
    problem += lpSum(y) == 1, "Only_One_Alternative"

    # Ограничения на индексы
    problem += lpSum(y[i] * indices[i][0] for i in range(len(indices))) <= MAX_BUDGET_INDEX, "Budget_Index_Constraint"
    problem += lpSum(y[i] * indices[i][1] for i in range(len(indices))) >= MIN_SOCIAL_RATING_INDEX, "Social_Rating_Constraint"
    problem += lpSum(y[i] * indices[i][2] for i in range(len(indices))) >= MIN_QUALITY_INDEX, "Quality_Index_Constraint"

    problem.solve()

    # Поиск выбранной альтернативы
    selected_index = next((i for i, var in enumerate(y) if var.value() == 1), None)

    return selected_index, ratings[selected_index] if selected_index is not None else None

# Main
# Преобразование данных
processed_data = transform_data(coffee_data)

# Рассчитываем индексы для данных
normalized_indices, raw_indices = calculate_indices(processed_data, weight_factors)

# Проверка линейной независимости
indices_array = np.array(normalized_indices)
rank = np.linalg.matrix_rank(indices_array)

# Определение метода оптимизации
if rank / len(indices_array) <= 0.3:
    print("Применяется MILP оптимизация")
    ratings_list = calculate_ratings(normalized_indices)
    selected_index, optimal_rating = milp_optimization(normalized_indices, ratings_list)

    if selected_index is not None:
        print(f"Выбрана альтернатива: {coffee_data[selected_index]}")
        print(f"Оптимальный рейтинг: {optimal_rating}")
    else:
        print("Оптимальное решение не найдено")
else:
    print("Применяется TOPSIS методика анализа")

    ratings_list = calculate_ratings(normalized_indices)
    ideal_combination = get_best_combination(coffee_data)
    ideal_indices, _ = calculate_indices([ideal_combination], weight_factors)
    ideal_indices = ideal_indices[0]
    ideal_rating = calculate_ratings([ideal_indices])[0]

    sorted_results = sorted(zip(ratings_list, coffee_data), key=lambda pair: abs(pair[0] - ideal_rating))

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
