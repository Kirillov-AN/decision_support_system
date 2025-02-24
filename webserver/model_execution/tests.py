from django.urls import reverse
from django.test import TestCase
from .views import convert_json_to_model_structure , get_list_of_weights, get_dict_of_limits
from django.core.management import call_command

from django.test import TestCase

class ViewTest(TestCase):
    fixtures = ['model_execution/fixtures/cup.json']

    def setUp(self):

        # Подготовка данных, которые нужны каждому тесту
        self.expected = [
            [5, 1000, True, 90, 5000, 85, 7],
            [6, 1500, False, 85, 4500, 80, 8],
            [7, 2000, True, 95, 4000, 90, 5],
            [8, 1200, False, 88, 4700, 82, 6],
            [7, 180, True, 230, 95, 4, 9]]
        self.model_id = 1

        self.expected_weight =  [11, 20, 11, 20, 20, 10]

        self.expected_dict_of_limits = {1:2,2:0.5,3:0.5}


    def test_convert_json_to_model_structure(self):
        print(self.model_id)
        list_of_list = convert_json_to_model_structure(self.model_id)

        self.assertEqual(list_of_list, self.expected)

    def test_get_list_of_weights(self):


        result = get_list_of_weights(self.model_id)

        self.assertEqual(result, self.expected_weight)

    def test_get_dict_of_limits(self):

        result = get_dict_of_limits(self.model_id)

        self.assertEqual(result, self.expected_dict_of_limits)
