class CupsCalculateIndices():

    def __init__(self,processed_data,weights):
        self.processed_data = processed_data
        self.weights = weights

    def calculate_indices(self):
        temp_indices = []
        self.processed_data = [row for row in self.processed_data if isinstance(row[0], (int, float))]
        batch_sizes = np.array([row[1] for row in self.processed_data], dtype=np.float64)
        average_batch_size = np.average(batch_sizes)*self.weights[1]
    
        financial_indices = []
    
        for row in self.processed_data:
    
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
            delivery_index = round(delivery_time / max([r[6] for r in self.processed_data]), 2)
    
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


class CalculateReiting():

    def __init__(self,processed_data,weights):
        self.processed_data = processed_data
        self.weights = weights




