from django.contrib import admin
from .models import Parameter, Variant, Model, Parameter_Variant

admin.site.register(Parameter)
admin.site.register(Variant)
admin.site.register(Model)
admin.site.register(Parameter_Variant)



# Register your models here.
