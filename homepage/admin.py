from django.contrib import admin

from .models import Comida
from .models import Imagen
from .models import Transacciones

admin.site.register(Comida)
admin.site.register(Imagen)
admin.site.register(Transacciones)
