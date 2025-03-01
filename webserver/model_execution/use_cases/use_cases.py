from abc import ABC, abstractmethod
from typing import Any, List
import numpy as np

class CupRepositoryInterface(ABC):
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


