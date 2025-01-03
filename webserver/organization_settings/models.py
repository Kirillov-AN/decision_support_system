from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Model(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.name}"

class Parameter(models.Model):
    SECTION_CHOICES = [
        ('base', 'Base'),
        ('advanced', 'Advanced'),
    ]

    name = models.CharField(max_length=255)  # Название параметра
    section = models.CharField(max_length=10, choices=SECTION_CHOICES)  # Раздел (base или advanced)
    value = models.PositiveIntegerField(  # Значение параметра от 1 до 100
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='model_values', default=1,null=True)
    def __str__(self):
        return f'{self.name} ({self.get_section_display()})'

class Variant(models.Model):

    name  = models.CharField(max_length=255)  # Название параметра
    model= models.CharField(max_length=255)  # Значение модели
    

    def __str__(self):
        return f'{self.name}'

class Parameter_Variant(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='parameter_values',null=True)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, related_name='variant_values',null=True)
    value = models.FloatField()
    def __str__(self):
        return f"{self.variant.name} - {self.parameter.name}: {self.value}"



