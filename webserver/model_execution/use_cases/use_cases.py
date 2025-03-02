from abc import ABC, abstractmethod
from typing import Any, List
import numpy as np
from pulp import LpMaximize, LpProblem, LpVariable, lpSum

class CupRepositoryInterface(ABC):
    @abstractmethod

# К интерфейсу обращается юзкейс, будет релизован в infra_adapters

    def get_transformed_data(self) -> list[Any]:
       pass
    def get_list_of_weights(self) -> list[Any]:
       pass
    def get_dict_of_limits(self) -> dict:
       pass

class CoffeRepositoryInterface(ABC):
    @abstractmethod

# К интерфейсу обращается юзкейс, будет релизован в infra_adapters

    def get_transformed_data(self) -> list[Any]:
       pass
    def get_list_of_weights(self) -> list[Any]:
       pass
    def get_dict_of_limits(self) -> dict:
       pass

class CupOptimizationPreparation():
    def __init__(self,data_provider: CupRepositoryInterface ):
        self.data_provider = data_provider
        # Получаем все данные, лимиты, веса 
        self.processed_data = data_provider.get_transformed_data()
        self.weights = data_provider.get_list_of_weights()
        self.limits = data_provider.get_dict_of_limits()
        self.MAX_BUDGET_INDEX = self.limits[1]           # Ограничение по финансовому индексу
        self.MIN_SOCIAL_RATING_INDEX = self.limits[2]    # Минимальный социальный рейтинг
        self.MIN_DELIVERY_INDEX = self.limits[3]          # Минимальный индекс доставки

    def calculate_indices(self,processed_data):
        temp_indices = []
        processed_data = [row for row in processed_data if isinstance(row[0], (int, float))]
        batch_sizes = np.array([row[1] for row in processed_data], dtype=np.float64)
        average_batch_size = np.average(batch_sizes)*self.weights[1]
    
        financial_indices = []
    
        for row in processed_data:
    
            price_per_cup = row[0]
            batch_size = row[1]
            logo = row[2]*self.weights[2]
            usability = row[3]*self.weights[3]
            logistics_cost = row[4]
            reputation = row[5]*self.weights[5]
            delivery_time = row[6]*self.weights[6]
    
            # Расчет стоимости покупки и доставки
            price_cost = price_per_cup * average_batch_size
            logistics_cost_normalized = (logistics_cost * average_batch_size) / batch_size
    
            # Финансовый индекс как сумма стоимости покупки и доставки
            financial_index = (price_cost*self.weights[0] + logistics_cost_normalized*self.weights[4])/(self.weights[0]+self.weights[4])
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

        indices_array = np.array(normalized_indices)
        rank = np.linalg.matrix_rank(indices_array)
        return normalized_indices.tolist(), indices_array, rank


    # Функция для расчёта рейтинга
    def calculate_ratings(self,normalized_indices):
        ratings = []
        for indices in normalized_indices:
            rating = round(indices[1] + indices[2] - indices[0], 6)
            ratings.append(rating)
        return ratings

class CupOptimizationTOPSIS():

    
    # Функция для получения идеальной комбинации
    def get_best_combination(self,input_data):
        best_price = min(row[0] for row in input_data)
        best_batch_size = max(row[1] for row in input_data)
        best_logo = max(1 if row[2] else 0 for row in input_data)
        best_usability = max(row[3] for row in input_data)
        best_logistics_cost = min(row[4] for row in input_data)
        best_reputation = max(row[5] for row in input_data)
        best_delivery_time = min(row[6] for row in input_data)
    
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

class CupOptimizationMILP():

    # MILP оптимизация
    def milp_optimization(self,indices, ratings):
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





class CoffeOptimizationPreparation():
    def __init__(self,data_provider: CupRepositoryInterface ):
        self.data_provider = data_provider
        # Получаем все данные, лимиты, веса 
        self.processed_data = data_provider.get_transformed_data()
        self.weights = data_provider.get_list_of_weights()
        self.limits = data_provider.get_dict_of_limits()
        self.MAX_BUDGET_INDEX = self.limits[1]           # Ограничение по финансовому индексу
        self.MIN_SOCIAL_RATING_INDEX = self.limits[2]    # Минимальный социальный рейтинг
        self.MIN_QUALITY_INDEX  = self.limits[3]          # Минимальный индекс доставки

    def calculate_indices(self,processed_data):
        temp_indices = []
        processed_data = [row for row in processed_data if isinstance(row[0], (int, float))]
        known_map = {'High': 3, 'Medium': 2, 'Low': 1, None: 0}
        service_level_map = {'Premium': 3, 'Standard': 2, 'Basic': 1, None: 0}
        financial_indices = []
    
        for row in processed_data:
    
            price_per_kg    = row[0]                       # 530
            batch_size      = row[1]                       # 950
            fame            = known_map.get(row[2], 0)     # 'High' -> 3
            reputation      = row[3]                       # 87
            warranty_years = row[4]
            logistics_cost  = row[5]                       # 290
            service_level   = service_level_map.get(row[6], 0)  # 'Premium' -> 3
            shelf_life      = row[7]                       # 5
            roaster_name    = row[8]                       # 'Roaster F'

    
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
        rank = np.linalg.matrix_rank(indices_array)


        return normalized_indices.tolist(), indices_array , rank
    
    # Функция для расчёта рейтинга
    def calculate_ratings(self,index_matrix):
        ratings = []
        for indices in index_matrix:
            rating = round(indices[1] + indices[2] - indices[0], 2)
            ratings.append(rating)
        return ratings

class CoffeOptimizationTOPSIS():

    # Функция для получения идеальной комбинации
    def get_best_combination(self,input_data):
    
        best_price = min(row[0] for row in input_data)
        best_batch_size = max(row[1] for row in input_data)
        best_known = max(row[2] for row in input_data)
        best_reputation = max(row[3] for row in input_data)
        best_warranty = max(row[4] for row in input_data)
        best_logistics_cost = min(row[5] for row in input_data)
        best_service_level = max(row[6] for row in input_data)
        best_shelf_life = max(row[7] for row in input_data)
    
        best_combination = [
            best_price,
            best_batch_size,
            best_known,
            best_reputation,
            best_warranty,
            best_logistics_cost,
            best_service_level,
            best_shelf_life,
            'Best Combination',
        ]
        return best_combination

class CoffeOptimizationMILP():

    # MILP оптимизация
    def milp_optimization(self, indices, ratings, MAX_BUDGET_INDEX, MIN_SOCIAL_RATING_INDEX, MIN_QUALITY_INDEX):
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
