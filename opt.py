import numpy as np

# def getdata
data = [
    ['Roaster F', 530, 950, 'High', 87, 4, 290, 'Premium', True, 5],
    ['Roaster G', 460, 1100, 'Medium', 75, 3, 310, 'Basic', False, 7],
    ['Roaster H', 500, 1050, 'High', 90, 6, 270, 'Premium', True, 12],
    ['Roaster I', 470, 1150, 'Low', 65, 2, 240, 'Standard', True, 7],
    ['Roaster J', 490, 980, 'Medium', 80, 5, 260, 'Standard', False, 8]
]

weights = [0.5, 2, 2, 1]

# Функция для преобразования данных
def transform_data(data):
    # Словари для преобразования строковых значений
    known_map = {'High': 3, 'Medium': 2, 'Low': 1, None: 0}
    service_level_map = {'Premium': 3, 'Standard': 2, 'Basic': 1, None: 0}
    installment_map = {True: 1, False: 0, None: 0}

    transformed_data = []

    for index, row in enumerate(data):
        transformed_row = [
            index + 1,  # Порядковый номер вместо названия
            row[1],     # Цена за 1 кг (₽)
            row[2],     # Размер партии (кг)
            known_map.get(row[3], 0),  # Известность обжарщика
            row[4],     # Репутация обжарщика
            row[5],     # Гарантии обжарщика (годы)
            row[6],     # Затраты на логистику (₽)
            service_level_map.get(row[7], 0),  # Уровень сервисных услуг
            installment_map.get(row[8], 0),    # Возможность оплаты в рассрочку
            row[9]      # Срок годности (мес)
        ]
        transformed_data.append(transformed_row)

    return transformed_data

# Функция для расчёта индексов
def calculate_indices(data):
    indices = []
    for row in data:
        price_per_kg = row[1]
        batch_size = row[2]
        fame = row[3]
        reputation = row[4]
        warranty_years = row[5]
        logistics_cost = row[6]
        service_level = row[7]
        installment = row[8]
        shelf_life = row[9]

        # Индекс финансовый
        financial_index = (price_per_kg * batch_size)/1000 + logistics_cost
        # Индекс качества
        quality_index = (reputation * fame) + service_level
        # Индекс надёжности (не понятно куда рассрочку)
        reliability_index = warranty_years + (2 * installment)
        # Индекс долговечности
        durability_index = shelf_life

        indices.append([
            financial_index,
            quality_index,
            reliability_index,
            durability_index
        ])
    return indices

# Функция для расчёта рейтинга с учётом корректировки для финансового индекса
def calculate_ratings(indices_data, weights = weights):
    ratings = []
    for indices in indices_data:
        # Учитываем, что финансовый индекс должен быть минимизирован и делён на 1000
        adjusted_indices = [-indices[0]] + indices[1:]
        rating = sum(i * w for i, w in zip(adjusted_indices, weights))
        ratings.append(rating)
    return ratings

# Функция для формирования наилучшей строки из лучших значений
def get_best_combination(data):
    # Трансформируем данные для работы
    transformed_data = transform_data(data)

    # Поиск лучших значений для каждого параметра
    best_price = min(row[1] for row in transformed_data)
    best_batch_size = max(row[2] for row in transformed_data)
    best_known = max(row[3] for row in transformed_data)
    best_reputation = max(row[4] for row in transformed_data)
    best_warranty = max(row[5] for row in transformed_data)
    best_logistics_cost = min(row[6] for row in transformed_data)
    best_service_level = max(row[7] for row in transformed_data)
    best_installment = max(row[8] for row in transformed_data)
    best_shelf_life = max(row[9] for row in transformed_data)

    best_combination = [
        'Best Combination',
        best_price,
        best_batch_size,
        best_known,
        best_reputation,
        best_warranty,
        best_logistics_cost,
        best_service_level,
        best_installment,
        best_shelf_life
    ]
    return best_combination

# Преобразование данных
transformed_data = transform_data(data)

# Рассчитываем индексы для данных
indices_data = calculate_indices(transformed_data)

# Определение количества линейно-независимых векторов для массива по индексам
indices_array = np.array(indices_data)
rank = np.linalg.matrix_rank(indices_array)

# Нахождение линейно-независимых векторов с использованием QR-разложения
q, r = np.linalg.qr(indices_array.T)
independent_indices = np.where(np.abs(np.diag(r)) > 1e-10)[0]
independent_vectors = indices_array[independent_indices]

# Рассчитываем рейтинги для данных
ratings = calculate_ratings(indices_data)

# Получение наилучшей комбинации
best_combination = get_best_combination(data)

# Рассчитываем рейтинг для наилучшей комбинации
best_combination_indices = calculate_indices([best_combination])[0]
best_combination_rating = calculate_ratings([best_combination_indices])[0]

# Сортировка исходных данных по рейтингу (от лучшего к худшему)
sorted_data_with_ratings = sorted(zip(ratings, data), key=lambda pair: pair[0], reverse=True)

# Вывод результатов
print(f"Количество линейно-независимых векторов: {rank}")
print("\nЛинейно-независимые векторы:")
for vec in independent_vectors:
    print(vec)

print("\nМассив по индексам:")
for idx in indices_data:
    print(idx)

print("\nРейтинги для каждой записи:")
for rating in ratings:
    print(rating)

print("\nНаилучшая комбинация из лучших значений:")
print(best_combination)

print("\nРейтинг наилучшей комбинации:")
print(best_combination_rating)

print("\nИсходные данные, отсортированные по рейтингу (от лучшего к худшему):")
for rating, entry in sorted_data_with_ratings:
    print(f"Рейтинг: {rating}, Данные: {entry}")
