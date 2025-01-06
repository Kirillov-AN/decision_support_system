from django.contrib import admin
from .models import Parameter, Variant, Model, Parameter_Variant, Limit

admin.site.register(Parameter)
admin.site.register(Variant)
admin.site.register(Model)
admin.site.register(Parameter_Variant)
admin.site.register(Limit)



# Register your models here.
