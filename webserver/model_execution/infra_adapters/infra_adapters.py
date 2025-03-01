from django.shortcuts import  get_object_or_404
from organization_settings.models import Model
from ..use_cases.use_cases import CupRepositoryInterface
from organization_settings.models import Variant




class CupsDataSQLRepository(CupRepositoryInterface):

    def __init__(self,model_id):
        self.model_id = model_id

    def get_transformed_data(self):
        variants = Variant.objects.filter(model=1)
        vectors = []
        for v in variants:
            supplier_name = v.name  
            row = [
                v.vector["Цена за один стаканчик"],
                v.vector["Размер партии стаканчиков"],
                1 if v.vector["Наличие логотипа бренда"] else 0,
                v.vector["Удобство пользования"],
                v.vector["Затраты на логистику"],
                v.vector["Репутация поставщика"],
                v.vector["Срок доставки"],
                supplier_name
            ]
            vectors.append(row)
        return vectors

    def get_list_of_weights(self):
        params_dict = get_object_or_404(Model, id=self.model_id).parameters
        
        base_weights = [item["weight"] for item in params_dict["base"]]
        advanced_weights = [item["weight"] for item in params_dict["advanced"]]
    
        list_of_weights = base_weights + advanced_weights
        return list_of_weights
    
    def get_dict_of_limits(self):
        limits = get_object_or_404(Model, id=self.model_id).limits
        dict_of_limits = {}
        for i in limits:
           dict_of_limits[i["id"]] = i["value"]
        return dict_of_limits


# class GetWeightsAndLimits():

#     def __init__(self,model_id):
#         self.model_id = model_id

#     def get_list_of_weights(self):
#         params_dict = get_object_or_404(Model, id=self.model_id).parameters
        
#         base_weights = [item["weight"] for item in params_dict["base"]]
#         advanced_weights = [item["weight"] for item in params_dict["advanced"]]
    
#         list_of_weights = base_weights + advanced_weights
#         return list_of_weights
    
#     def get_dict_of_limits(self):
#         limits = get_object_or_404(Model, id=self.model_id).limits
#         dict_of_limits = {}
#         for i in limits:
#            dict_of_limits[i["id"]] = i["value"]
#         return dict_of_limits