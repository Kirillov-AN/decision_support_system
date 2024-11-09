import math

alternatives = [[95, 0.8, 5, 35, 180, 90, 180, 12],
 [65, 0.5, 4, 25, 120, 60, 240, 6],
 [20, 0.15, 1, 10, 40, 20, 40, 1],
 [85, 0.3, 3, 30, 160, 50, 160, 10],
 [40, 0.7, 2, 15, 80, 30, 160, 3],
 [50, 0.4, 3, 20, 100, 45, 200, 5],
 [100, 0.95, 5, 40, 200, 100, 200, 12],
 [60, 0.6, 4, 20, 110, 50, 55, 6],
 [10, 0.05, 1, 8, 30, 10, 30, 2],
 [75, 0.65, 3, 28, 140, 70, 70, 8],
 [55, 0.85, 4, 12, 90, 55, 90, 4],
 [30, 0.5, 2, 10, 50, 25, 50, 3]]

# Ограничения
max_budget = 300  # Общий бюджет на аренду, инфраструктуру и залог (в тысячах руб)
min_reputation = 3  # Минимальная допустимая репутация
min_rent_time = 6  # Минимальный срок аренды (в месяцах)
budget_constraint = rent + infra_costs + deposit

def apply_constraints(alternatives):
    filtered = []
    for alt in alternatives:
        budget_constraint = alt[4] +   alt[5]  + alt[6]
        if alt[2] >= min_reputation and budget_constraint <= max_budget and  min_rent_time >= alt[7] :
            filtered.append(alt)
    return filtered

alternatives = apply_constraints(alternatives)



normalized_matrix = []
matrix_line_len = len(alternatives[0])
matrix_len = len(alternatives)

def normaling_matrix():
    sum_x = 0
    for v in alternatives:
      normalized_matrix.append([])
    for variant in range(matrix_len):
       for crit in range(matrix_line_len):
        sum_x = 0
        for variant_for_sum in range(matrix_len):
           sum_x+= alternatives[variant_for_sum][crit]**2
        
        x = alternatives[variant][crit]
        sqrt_x = math.sqrt(sum_x)
        x_normalized = x / sqrt_x
        normalized_matrix[variant].append(x_normalized)

        
normaling_matrix()

weights = {
    "0": 0.3,
    "1": 0.2,
    "2": 0.1,
    "3": 0.1,
    "4": 0.1,
    "5": 0.1,
    "6": 0.05,
    "7": 0.05
}

criteria_types = [True, True, True, True, True, False, False, False]  # True для пользы, False для затрат



def create_weighted_matrix():
    for variant in range(matrix_len):
       for crit in range(matrix_line_len):   
        normalized_matrix[variant][crit] = normalized_matrix[variant][crit] * weights[str(crit)]


create_weighted_matrix()


positive_ideal = []
negative_ideal = []

def calculate_ideal(): 
    for crit in range(matrix_line_len):
        if criteria_types[crit]:  # Критерий пользы
            positive = max(x[crit] for x in normalized_matrix)
            negative = min(x[crit] for x in normalized_matrix)
        else:  # Затратный критерий
            positive = min(x[crit] for x in normalized_matrix)
            negative = max(x[crit] for x in normalized_matrix)
        positive_ideal.append(positive)
        negative_ideal.append(negative)

calculate_ideal()


range_from_positive_ideal = []
range_from_negative_ideal = []


def calculate_range():
    range_positive_var=0
    range_negative_var=0
    for variant in range(matrix_len):
        for crit in range(matrix_line_len):
         range_positive_var += ( positive_ideal[crit] - normalized_matrix[variant][crit] ) **2
         range_negative_var += ( negative_ideal[crit] - normalized_matrix[variant][crit] ) **2
        range_positive_sqrt = math.sqrt(range_positive_var)
        range_negative_sqrt = math.sqrt(range_negative_var)
        range_from_positive_ideal.append(range_positive_sqrt)
        range_from_negative_ideal.append(range_negative_sqrt)
        range_positive_var = 0
        range_negative_var = 0

calculate_range()

print(range_from_positive_ideal,range_from_negative_ideal)


def calculate_closeness(range_from_positive_ideal, range_from_negative_ideal):
    closeness = []
    for d_positive, d_negative in zip(range_from_positive_ideal, range_from_negative_ideal):
        if (d_positive + d_negative) == 0:
            closeness.append(0)
        else:
            closeness.append(d_negative / (d_positive + d_negative))
    return closeness

closeness = calculate_closeness(range_from_positive_ideal, range_from_negative_ideal)

# Ранжирование альтернатив
ranked_alternatives = sorted(range(len(closeness)), key=lambda k: closeness[k], reverse=True)

print("Коэффициенты близости:", closeness)
print("Ранжирование альтернатив:", ranked_alternatives)