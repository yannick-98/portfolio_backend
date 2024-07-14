from django.contrib import admin
from .models import Item, ModeloML, HelloWorld, Chart, House, News

class ItemAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('nombre', 'descripcion')

class ModeloMLAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'archivo_modelo')
    search_fields = ('nombre', 'archivo_modelo')
    list_filter = ('nombre', 'archivo_modelo')

class HelloWorldAdmin(admin.ModelAdmin):
    list_display = ('message')
    search_fields = ('message')
    list_filter = ('message')

class NewsAdmin(admin.ModelAdmin):
    list_display = ('headlines')
    search_fields = ('headlines')
    list_filter = ('headlines')


admin.site.register(Item, ItemAdmin)
admin.site.register(ModeloML, ModeloMLAdmin)
admin.site.register(House)
admin.site.register(News)
