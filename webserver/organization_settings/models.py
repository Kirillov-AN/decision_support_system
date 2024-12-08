from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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

    def __str__(self):
        return f'{self.name} ({self.get_section_display()})'
